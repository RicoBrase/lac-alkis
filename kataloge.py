try:
    from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
except ImportError:
    from PyQt5.QtSql import QSqlDatabase, QSqlQuery

def firstFromCharacterVaryingArray(input: str) -> str:
    pass

class Bundesland:

    query_str = u"SELECT schluesselgesamt, bezeichnung FROM ax_bundesland;"

    def __init__(self, db: QSqlDatabase):
        query = QSqlQuery(db)
        query.exec(self.query_str)

        record = query.record()

        self._bundesland_map = {}

        while query.next():
            schluessel = int(query.value(record.indexOf("schluesselgesamt")))
            bezeichnung = query.value(record.indexOf("bezeichnung"))
            self._bundesland_map.update({self.buildSchluessel(schluessel): bezeichnung})

    def bezeichnungFromSchluessel(self, schluessel: int):
        bezeichnung: str = self._bundesland_map.get(self.buildSchluessel(schluessel))
        if bezeichnung == None:
            return "Undefiniertes Bundesland"
        return bezeichnung
    
    @staticmethod
    def buildSchluessel(schluessel: int):
        return f"{schluessel:02d}"
    
class Regierungsbezirk:

    query_str = u"SELECT land, regierungsbezirk, bezeichnung FROM ax_regierungsbezirk;"

    def __init__(self, db: QSqlDatabase):
        query = QSqlQuery(db)
        query.exec(self.query_str)

        record = query.record()

        self._regierungsbezirk_map = {}

        while query.next():
            landesschluessel = int(query.value(record.indexOf("land")))
            bezirksschluessel = int(query.value(record.indexOf("regierungsbezirk")))
            bezeichnung = query.value(record.indexOf("bezeichnung"))
            self._regierungsbezirk_map.update({self.buildSchluessel(landesschluessel, bezirksschluessel): bezeichnung})

    @staticmethod
    def buildSchluessel(landesschluessel: int, bezirksschluessel: int):
        return f"{landesschluessel:02d}{bezirksschluessel}"

    def bezeichnungFromSchluessel(self, landesschluessel: int, bezirksschluessel: int):
        bezeichnung: str = self._regierungsbezirk_map.get(self.buildSchluessel(landesschluessel, bezirksschluessel))
        if bezeichnung == None:
            return "Undefinierter Regierungsbezirk"
        return bezeichnung
    
class KreisRegion:

    query_str = u"SELECT land, regierungsbezirk, kreis, bezeichnung FROM ax_kreisregion;"

    def __init__(self, db: QSqlDatabase):
        query = QSqlQuery(db)
        query.exec(self.query_str)

        record = query.record()

        self._kreisregion_map = {}

        while query.next():
            landesschluessel = int(query.value(record.indexOf("land")))
            bezirksschluessel = int(query.value(record.indexOf("regierungsbezirk")))
            kreis = int(query.value(record.indexOf("kreis")))
            bezeichnung = query.value(record.indexOf("bezeichnung"))
            self._kreisregion_map.update({self.buildSchluessel(landesschluessel, bezirksschluessel, kreis): bezeichnung})

    @staticmethod
    def buildSchluessel(landesschluessel: int, bezirksschluessel: int, kreisregion: int):
        return f"{landesschluessel:02d}{bezirksschluessel}{kreisregion:02d}"

    def bezeichnungFromSchluessel(self, landesschluessel: int, bezirksschluessel: int, kreisregion: int):
        bezeichnung: str = self._kreisregion_map.get(self.buildSchluessel(landesschluessel, bezirksschluessel, kreisregion))
        if bezeichnung == None:
            return "Undefinierter Kreis oder Undefinierte Region"
        return bezeichnung
    
class Gemeinde:

    query_str = u"SELECT land, regierungsbezirk, kreis, gemeinde, bezeichnung FROM ax_gemeinde;"

    def __init__(self, db: QSqlDatabase):
        query = QSqlQuery(db)
        query.exec(self.query_str)

        record = query.record()

        self._gemeinde_map = {}

        while query.next():
            landesschluessel = int(query.value(record.indexOf("land")))
            bezirksschluessel = int(query.value(record.indexOf("regierungsbezirk")))
            kreis = int(query.value(record.indexOf("kreis")))
            gemeinde = int(query.value(record.indexOf("gemeinde")))
            bezeichnung = query.value(record.indexOf("bezeichnung"))
            self._gemeinde_map.update({self.buildSchluessel(landesschluessel, bezirksschluessel, kreis, gemeinde): bezeichnung})

    @staticmethod
    def buildSchluessel(landesschluessel: int, bezirksschluessel: int, kreisregion: int, gemeinde: int):
        return f"{landesschluessel:02d}{bezirksschluessel}{kreisregion:02d}{gemeinde:03d}"

    def bezeichnungFromSchluessel(self, landesschluessel: int, bezirksschluessel: int, kreisregion: int, gemeinde: int):
        bezeichnung: str = self._gemeinde_map.get(self.buildSchluessel(landesschluessel, bezirksschluessel, kreisregion, gemeinde))
        if bezeichnung == None:
            return "Undefinierte Gemeinde"
        return bezeichnung
    
class Gemarkung:

    query_str = u"SELECT land, gemarkungsnummer, bezeichnung, istamtsbezirkvon_land[1], istamtsbezirkvon_stelle[1] FROM ax_gemarkung;"

    def __init__(self, db: QSqlDatabase):
        query = QSqlQuery(db)
        query.exec(self.query_str)

        record = query.record()

        self._map = {}
        self._map_amtsbezirke = {}

        while query.next():
            landesschluessel = int(query.value(record.indexOf("land")))
            gemarkungsnummer = int(query.value(record.indexOf("gemarkungsnummer")))
            bezeichnung = query.value(record.indexOf("bezeichnung"))
            self._map.update({self.buildSchluessel(landesschluessel, gemarkungsnummer): bezeichnung})

            amtsbezirk_land = int(query.value(record.indexOf("istamtsbezirkvon_land")))
            amtsbezirk_stelle = query.value(record.indexOf("istamtsbezirkvon_stelle"))
            self._map_amtsbezirke.update({self.buildSchluessel(landesschluessel, gemarkungsnummer): {"land": amtsbezirk_land, "stelle": amtsbezirk_stelle}})

    @staticmethod
    def buildSchluessel(landesschluessel: int, gemarkungsnummer: int):
        return f"{landesschluessel:02d}{gemarkungsnummer:04d}"

    def bezeichnungFromSchluessel(self, landesschluessel: int, gemarkungsnummer: int):
        bezeichnung: str = self._map.get(self.buildSchluessel(landesschluessel, gemarkungsnummer))
        if bezeichnung == None:
            return "Undefinierte Gemarkung"
        return bezeichnung    
    
    def amtsbezirk_land(self, landesschluessel: int, gemarkungsnummer: int) -> int:
        return self._map_amtsbezirke.get(self.buildSchluessel(landesschluessel, gemarkungsnummer)).get("land")
    
    def amtsbezirk_stelle(self, landesschluessel: int, gemarkungsnummer: int) -> str:
        return self._map_amtsbezirke.get(self.buildSchluessel(landesschluessel, gemarkungsnummer)).get("stelle")
    
class Dienststelle:

    query_str = u"SELECT land, stelle, bezeichnung FROM ax_dienststelle;"

    def __init__(self, db: QSqlDatabase):
        query = QSqlQuery(db)
        query.exec(self.query_str)

        record = query.record()

        self._map = {}

        while query.next():
            landesschluessel = int(query.value(record.indexOf("land")))
            stelle = query.value(record.indexOf("stelle"))
            bezeichnung = query.value(record.indexOf("bezeichnung"))
            self._map.update({self.buildSchluessel(landesschluessel, stelle): bezeichnung})

    @staticmethod
    def buildSchluessel(landesschluessel: int, stelle: str):
        return f"{landesschluessel:02d}{stelle}"

    def bezeichnungFromSchluessel(self, landesschluessel: int, stelle: str):
        bezeichnung: str = self._map.get(self.buildSchluessel(landesschluessel, stelle))
        if bezeichnung == None:
            return "Undefinierte Dienststelle"
        return bezeichnung    
    
class Strassenlage:

    query_str = u"SELECT lage, bezeichnung FROM ax_lagebezeichnungkatalogeintrag;"

    def __init__(self, db: QSqlDatabase):
        query = QSqlQuery(db)
        query.exec(self.query_str)

        record = query.record()

        self._map = {}

        while query.next():
            lage = query.value(record.indexOf("lage"))
            bezeichnung = query.value(record.indexOf("bezeichnung"))
            self._map.update({lage: bezeichnung})

    def bezeichnungFromLage(self, lage: str):
        bezeichnung: str = self._map.get(lage)
        if bezeichnung == None:
            return "Undefinierte Strassenlage"
        return bezeichnung    
    