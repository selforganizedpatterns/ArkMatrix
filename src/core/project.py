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
    _groups = {}
    _subgroups = {}

    def __init__(self, dataset='', siteCode=''):
        self.dataset = dataset
        self.siteCode = siteCode

    def info(self):
        info = '\nDataset: ' + self.dataset + '\n'
        info = info + 'Site Code: ' + self.siteCode + '\n'
        info = info + 'Number of Units: ' + str(len(self._units)) + '\n'
        info = info + 'Number of Groups: ' + str(len(self._groups)) + '\n'
        info = info + 'Number of Subgroups: ' + str(len(self._subgroups)) + '\n\n'
        info = info + self.matrix.info() + '\n\n'
        return info

    def unit(self, key):
        if str(key) in self._units:
            return self._units[key]
        else:
            key = self.makeKey(key)
            if key in self._units:
                return self._units[key]
        return Unit()

    def units(self):
        return sorted(self._units.values())

    def readFile(self, infile, fileFormat):
        formatter = Format.createFormat(fileFormat)
        formatter.read(infile, self)

    def addUnit(self, unit):
        self._units[unit.key()] = unit

    def addRelationship(self, fromUnit, reln, toUnit):
        self.matrix.addRelationship(fromUnit, reln, toUnit)

    def addGrouping(self, groupId, subgroupId):
        groupKey =self.makeKey(groupId);
        subgroupKey =self.makeKey(subgroupId);
        if groupKey in self._groups:
            self._groups[groupKey].add(subgroupKey)
        else:
            self._groups[groupKey] = set([subgroupKey])

    def addSubgrouping(self, subgroupId, unitId):
        if subgroupId in self._subgroups:
            self._subgroups[subgroupId].add(unitId)
        else:
            self._subgroups[subgroupId] = set([unitId])

    def hasUnit(self, unit):
        if isinstance(unit, Unit):
            return unit in self._units.values()
        return unit in self._units or self.makeKey(unit) in self._units

    def removeOrphans(self):
        for key in self._units.keys():
            if key not in self.matrix:
                self._units.pop(key)

    def writeFile(self, fileFormat, style, sameas, width, height):
        formatter = Format.createFormat(fileFormat)
        formatter.write(self, style, sameas, width, height)

    def makeKey(self, unitId):
        if self.siteCode:
            return self.siteCode + '_' + str(unitId)
        else:
            return str(unitId)

