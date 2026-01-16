# -*- coding: utf-8 -*-

"""
***************************************************************************
    __init__.py
    ---------------------
    Date                 : September 2012
    Copyright            : (C) 2012-2025 by Jürgen Fischer
    Email                : jef at norbit dot de

    Modifications:
    ---------------------
    Date                 : January 2026
    Copyright            : (C) 2026 by Rico Brase
    Email                : rico dot brase at lachendorf dot de
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
from __future__ import absolute_import

def name():
    return u"ALKIS-Einbindung"

def description():
    return u"Dies Plugin dient zur Einbindung von ALKIS-Layern."

def version():
    return "Version 0.1"

def qgisMinimumVersion():
    return "3.0"

def authorName():
    return u"Rico Brase <rico.brase@lachendorf.de>"

def icon():
    return ":/plugins/alkis/logo.png"

def classFactory(iface):
    from .alkisplugin import alkisplugin
    return alkisplugin(iface)
