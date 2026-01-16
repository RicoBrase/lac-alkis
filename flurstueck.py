try:
    from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord
except ImportError:
    from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord

from .kataloge import Bundesland, Regierungsbezirk, KreisRegion, Gemeinde, Gemarkung, Dienststelle

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
        ]
    query_str = u"SELECT {0} FROM ax_flurstueck WHERE endet IS NULL AND gml_id = {1} LIMIT 1;"

    def __init__(self, gmlid, db: QSqlDatabase, bundesland: Bundesland, regierungsbezirk: Regierungsbezirk, kreisregion: KreisRegion, gemeinde: Gemeinde, gemarkung: Gemarkung, dienststelle: Dienststelle):

        self._kat_bundesland = bundesland
        self._kat_regierungsbezirk = regierungsbezirk
        self._kat_kreisregion = kreisregion
        self._kat_gemeinde = gemeinde
        self._kat_gemarkung = gemarkung
        self._kat_dienststelle = dienststelle

        query = QSqlQuery(db)
        query.exec(self.query_str.format(", ".join(self.query_fields), f"'{gmlid}'"))

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

        else:
            print(query.lastQuery())
            print(query.lastError().text())


    def gml_id(self):
        return self._gml_id
    
    def kennzeichenALB4stl(self):
        return f"{self._land:02d}{self._gemarkungsnummer:04d}-{self._flurnummer:03d}-{self._zaehler:04d}/{self._nenner:04d}.00"
    
    def kennzeichenALK4stl(self):
        return f"FS{self._land:02d}{self._gemarkungsnummer:04d}{self._flurnummer:03d}{self._zaehler:04d}{self._nenner:04d}00"
    
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