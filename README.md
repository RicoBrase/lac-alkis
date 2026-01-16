# ALKIS-Plugin

Das QGIS-Plugin alkisplugin dient zur Einbindung von ALKIS-Daten aus durch
[norGIS ALKIS-Import](http://www.norbit.de/68/) (über [GDAL/OGR](http://gdal.org))
erzeugten PostgreSQL/PostGIS-Datenbanken.

Funktion:
* Einbindung der von ALKIS-Import vorbereiteten Layer mit Klassifizierungen inkl. SVG-Symbolen
* Erzeugung von UMN-Mapfiles (erfordert python-mapscript)
* Flurstückseigentümerabfrage
* Anbindung an [norGIS Liegenschaftbuchfachschale](http://www.norbit.de/78/) (proprietär)

[Homepage](http://www.norbit.de/75/), Lizenz: [GPLv2](http://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

## Installation
### Windows
1. Vor der ersten Nutzung muss im QGIS-Installationsverzeichnis die `OSGeo4W.bat` mit Adminrechten gestartet werden.
2. Folgenden Befehl ausführen: `python3 -m pip install XlsxWriter`