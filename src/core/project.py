# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Matrix
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2016-02-29
        git sha              : $Format:%H$
        copyright            : 2016 by John Layt
        email                : john@layt.net
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from unit import Unit
from matrix import Matrix
from format import Format

class Project():

    dataset = ''
    siteCode = ''
    matrix = Matrix()
    _units = {}
    _groups = set()

    def __init__(self, dataset='', siteCode=''):
        self.dataset = dataset
        self.siteCode = siteCode

    def info(self):
        info = '\nDataset: ' + self.dataset + '\n'
        info = info + 'Site Code: ' + self.siteCode + '\n'
        info = info + 'Number of Units: ' + str(len(self._units)) + '\n\n'
        info = info + self.matrix.info() + '\n\n'
        return info

    def unit(self, key):
        return self._units[key]

    def units(self):
        return sorted(self._units.values())

    def readFile(self, infile, fileFormat):
        formatter = Format.createFormat(fileFormat)
        formatter.read(infile, self)

    def addUnit(self, unit):
        self._units[unit.key()] = unit

    def addGroup(self, unitId):
        self._groups.add(unitId)

    def addRelationship(self, fromUnit, reln, toUnit):
        self.matrix.addRelationship(fromUnit, reln, toUnit)

    def hasUnit(self, unit):
        return unit in self._units

    def removeOrphans(self):
        for key in self._units:
            if key not in self.matrix:
                self._units.pop(key)

    def writeFile(self, fileFormat, style, sameas, width, height):
        formatter = Format.createFormat(fileFormat)
        formatter.write(self, style, sameas, width, height)
