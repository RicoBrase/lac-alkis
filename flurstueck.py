try:
    from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord
except ImportError:
    from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord

from .kataloge import Bundesland, Regierungsbezirk, KreisRegion, Gemeinde, Gemarkung, Dienststelle, Strassenlage

class FlurstueckNutzung:
    def __init__(self, schluessel: str, bezeichnung: str, flaeche: int):
        self._schluessel = schluessel
        self._bezeichnung = bezeichnung
        self._flaeche = flaeche

    def getExportText(self):
        return f"({self._schluessel.replace(":", "-")}) {self._bezeichnung} {self._flaeche} m²"

class Flurstueck:

    query_fields = [
        "gml_id",
        "gemarkungsnummer",
        "flurnummer",
        "zaehler",
        "nenner",
        "gemeindezugehoerigkeit_land",
        "gemeindezugehoerigkeit_regierungsbezirk",
        "gemeindezugehoerigkeit_kreis",
        "gemeindezugehoerigkeit_gemeinde",
        "zustaendigestelle_land[1]",
        "zustaendigestelle_stelle[1]",
        "amtlicheflaeche",
        "weistAuf[1] as weistAufLageId",
        "to_char(zeitpunktderentstehung, 'DD.MM.YYYY') as zeitpunktderentstehung",
        "to_char(beginnt::timestamp, 'DD.MM.YYYY HH24:MI:SS') as beginnt",
        "to_char(endet::timestamp, 'DD.MM.YYYY HH24:MI:SS') as endet"
        ]
    query_str = u"SELECT {0} FROM ax_flurstueck WHERE endet IS NULL AND gml_id = '{1}' LIMIT 1;"
    geometry_query_str = u"SELECT st_x(point), st_y(point) FROM (SELECT st_centroid(line) as point FROM public.po_lines WHERE gml_id = '{0}');"
    housenumber_query_str = u"SELECT lage, hausnummer FROM ax_lagebezeichnungmithausnummer WHERE gml_id = '{0}';"
    nutzung_query_str = u"SELECT flsnr, nutzsl as schluessel, fl as flaeche, nutzung FROM public.nutz_21 JOIN nutz_shl ON nutz_21.nutzsl = nutz_shl.nutzshl WHERE flsnr = '{0}';"

    def __init__(self, gmlid, db: QSqlDatabase, bundesland: Bundesland, regierungsbezirk: Regierungsbezirk, kreisregion: KreisRegion, gemeinde: Gemeinde, gemarkung: Gemarkung, dienststelle: Dienststelle, strassenlage: Strassenlage):

        self._kat_bundesland = bundesland
        self._kat_regierungsbezirk = regierungsbezirk
        self._kat_kreisregion = kreisregion
        self._kat_gemeinde = gemeinde
        self._kat_gemarkung = gemarkung
        self._kat_dienststelle = dienststelle
        self._kat_strassenlage = strassenlage

        query = QSqlQuery(db)
        query.exec(self.query_str.format(", ".join(self.query_fields), f"{gmlid}"))

        record = query.record()

        if query.next():
            self._gml_id: str = query.value(record.indexOf("gml_id"))
            self._gemarkungsnummer: int = int(query.value(record.indexOf("gemarkungsnummer")))
            self._flurnummer: int = int(query.value(record.indexOf("flurnummer")))
            self._zaehler: int = int(query.value(record.indexOf("zaehler")))
            self._nenner: int = int(query.value(record.indexOf("nenner")))
            self._land: int = int(query.value(record.indexOf("gemeindezugehoerigkeit_land")))
            self._bezirk: int = int(query.value(record.indexOf("gemeindezugehoerigkeit_regierungsbezirk")))
            self._kreisregion: int = int(query.value(record.indexOf("gemeindezugehoerigkeit_kreis")))
            self._gemeinde: int = int(query.value(record.indexOf("gemeindezugehoerigkeit_gemeinde")))
            self._zustaendig_land: int = int(query.value(record.indexOf("zustaendigestelle_land")))
            self._zustaendig_stelle: str = query.value(record.indexOf("zustaendigestelle_stelle"))
            self._amtlicheflaeche: float = float(query.value(record.indexOf("amtlicheflaeche")))
            self._weistAufLageId: str = query.value(record.indexOf("weistAufLageId"))
            self._zeitpunktderentstehung: str = query.value(record.indexOf("zeitpunktderentstehung"))
            self._lebensintervall_beginnt = query.value(record.indexOf("beginnt"))
            self._lebensintervall_endet = query.value(record.indexOf("endet"))

        else:
            print(query.lastQuery())
            print(query.lastError().text())

        # Geokoordinaten
        query.exec(self.geometry_query_str.format(gmlid))
        record = query.record()

        if query.next():
            self._coord_x: float = float(query.value(record.indexOf("st_x")))
            self._coord_y: float = float(query.value(record.indexOf("st_y")))
        else:
            print(query.lastQuery())
            print(query.lastError().text())

        # Hausnummer
        query.exec(self.housenumber_query_str.format(self._weistAufLageId))
        record = query.record()

        if query.next():
            self._lage: str = query.value(record.indexOf("lage"))
            self._hausnr: str = query.value(record.indexOf("hausnummer"))
        else:
            print(query.lastQuery())
            print(query.lastError().text())

        # Nutzung
        query.exec(self.nutzung_query_str.format(self.kennzeichenNutzung()))
        record = query.record()

        self._nutzung: list[FlurstueckNutzung] = []

        while query.next():
            fs_nutz: FlurstueckNutzung = FlurstueckNutzung(
                str(query.value(record.indexOf("schluessel"))).strip(),
                str(query.value(record.indexOf("nutzung"))).strip(),
                int(query.value(record.indexOf("flaeche")))
            )

            self._nutzung.append(fs_nutz)


    def gml_id(self):
        return self._gml_id
    
    def kennzeichenNutzung(self):
        return f"{self._land:02d}{self._gemarkungsnummer:04d}-{self._flurnummer:03d}-{self._zaehler:05d}/{self._nenner:03d}"

    def kennzeichenALB4stl(self):
        return f"{self._land:02d}{self._gemarkungsnummer:04d}-{self._flurnummer:03d}-{self._zaehler:04d}/{self._nenner:04d}.00"
    
    def kennzeichenALK4stl(self):
        return f"FS{self._land:02d}{self._gemarkungsnummer:04d}{self._flurnummer:03d}{self._zaehler:04d}{self._nenner:04d}00"
    
    def kennzeichenALB3stl(self):
        return f""
    
    def kennzeichenALK3stl(self):
        return f""

    def kennzeichenALKIS(self):
        return f"{self._land:02d}{self._gemarkungsnummer:04d}{self._flurnummer:03d}{self._zaehler:04d}{self._nenner:04d}__"
    
    def bundesland(self):
        return f"({self._kat_bundesland.buildSchluessel(self._land)}) {self._kat_bundesland.bezeichnungFromSchluessel(self._land)}"
    
    def regierungsbezirk(self):
        return f"({self._kat_regierungsbezirk.buildSchluessel(self._land, self._bezirk)}) {self._kat_regierungsbezirk.bezeichnungFromSchluessel(self._land, self._bezirk)}"
    
    def kreisregion(self):
        return f"({self._kat_kreisregion.buildSchluessel(self._land, self._bezirk, self._kreisregion)}) {self._kat_kreisregion.bezeichnungFromSchluessel(self._land, self._bezirk, self._kreisregion)}"
    
    def gemeinde(self):
        return f"({self._kat_gemeinde.buildSchluessel(self._land, self._bezirk, self._kreisregion, self._gemeinde)}) {self._kat_gemeinde.bezeichnungFromSchluessel(self._land, self._bezirk, self._kreisregion, self._gemeinde)}"
    
    def gemarkung(self):
        return f"({self._kat_gemarkung.buildSchluessel(self._land, self._gemarkungsnummer)}) {self._kat_gemarkung.bezeichnungFromSchluessel(self._land, self._gemarkungsnummer)}"
    
    def flurnummer(self):
        return f"{self._flurnummer}"
    
    def flurstuecksnummer(self):
        return f"{self._zaehler}/{self._nenner}"
    
    def katasteramt(self):
        amtsbezirk_land = self._kat_gemarkung.amtsbezirk_land(self._land, self._gemarkungsnummer)
        amtsbezirk_stelle = self._kat_gemarkung.amtsbezirk_stelle(self._land, self._gemarkungsnummer)
        return f"({amtsbezirk_land:02d}{amtsbezirk_stelle}) {self._kat_dienststelle.bezeichnungFromSchluessel(amtsbezirk_land, amtsbezirk_stelle)}"
    
    def finanzamt(self):
        return f"({self._zustaendig_land:02d}{self._zustaendig_stelle}) {self._kat_dienststelle.bezeichnungFromSchluessel(self._zustaendig_land, self._zustaendig_stelle)}"
    
    def forstamt(self):
        return f""

    def amtlicheflaeche(self):
        return f"{self._amtlicheflaeche:g}"

    def koordinate_x(self):
        return f"{self._coord_x:.3f}"
    
    def koordinate_y(self):
        return f"{self._coord_y:.3f}"
    
    def unverschluesselte_lagebezeichnung(self):
        return f""

    def strasse_hausnummer(self):
        return f"({self._kat_gemeinde.buildSchluessel(self._land, self._bezirk, self._kreisregion, self._gemeinde)}{self._lage}) {self._kat_strassenlage.bezeichnungFromLage(self._lage)} {self._hausnr}"
    
    def hinweis(self):
        return f""

    def entstehung(self):
        return f"{self._zeitpunktderentstehung}"
    
    def lebenszeitintervall_beginnt(self):
        if f"{self._lebensintervall_beginnt}" == "NULL":
            return f""
        return f"{self._lebensintervall_beginnt}"
    
    def lebenszeitintervall_endet(self):
        if f"{self._lebensintervall_endet}" == "NULL":
            return f""
        return f"{self._lebensintervall_endet}"
    
    def vorgaengerflurstueck(self):
        return f""
    
    def nachfolgerflurstueck(self):
        return f""
    
    def nutzung(self):
        nutz_entries = ""
        for fs_nutz in self._nutzung:
            nutz_entries += fs_nutz.getExportText() + "\n"

        return nutz_entries.strip()
    
    def klassifizierung(self):
        return f""
    
    def bodenschaetzung(self):
        return f""
    
    def bewertung(self):
        return f""
    
    def eigentum(self):
        return f""