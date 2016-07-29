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
    subgroupMatrix = Matrix()
    _units = {}
    _groups = {}
    _subgroups = {}

    def __init__(self, dataset='', siteCode=''):
        self.dataset = dataset
        self.siteCode = siteCode

    def info(self):
        info = '  Dataset: ' + self.dataset + '\n'
        info = info + '  Site Code: ' + self.siteCode + '\n'
        info = info + '  Number of Units: ' + str(len(self._units)) + '\n'
        orphans = self.orphans()
        info = info + '  Number of Orphan Units: ' + str(len(orphans)) + '\n'
        if orphans:
            info = info + '    ' + str(orphans) + '\n'
        if len(self._subgroups) > 0:
            missing = self.missingSubgroup()
            info = info + '  Number of Units Missing Subgroup: ' + str(len(orphans)) + '\n'
            if missing:
                info = info + '    ' + str(missing) + '\n'
        info = info + '  Number of Groups: ' + str(len(self._groups)) + '\n'
        info = info + '  Number of Subgroups: ' + str(len(self._subgroups)) + '\n\n'
        info = info + self.matrix.info()
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
        groupId = self._makeId(groupId)
        subgroupId = self._makeId(subgroupId)
        if not groupId or not subgroupId:
            return
        if groupId in self._groups:
            self._groups[groupId].add(subgroupId)
        else:
            self._groups[groupId] = set([subgroupId])

    def addSubgrouping(self, subgroupId, unitId):
        subgroupId = self._makeId(subgroupId)
        unitId = self._makeId(unitId)
        if not subgroupId or not unitId:
            return
        if subgroupId in self._subgroups:
            self._subgroups[subgroupId].add(unitId)
        else:
            self._subgroups[subgroupId] = set([unitId])

    def hasUnit(self, unit):
        if isinstance(unit, Unit):
            return unit in self._units.values()
        return unit in self._units or self.makeKey(unit) in self._units

    def missingSubgroup(self):
        units = []
        for unit in self._units.values():
            if not unit.subgroup():
                units.append(unit.unitId())
        return units

    def orphans(self):
        units = []
        for unit in self._units.values():
            if unit.unitId() not in self.matrix:
                units.append(unit.unitId())
        return units

    def removeOrphans(self):
        units = []
        for unit in self._units.values():
            if unit.unitId() not in self.matrix:
                units.append(unit.key())
        for key in units:
            self._units.pop(key)

    def writeFile(self, fileFormat, options):
        formatter = Format.createFormat(fileFormat)
        formatter.write(self, options)

    def writeSubgroupFile(self, fileFormat, options):
        formatter = Format.createFormat(fileFormat)
        formatter.writeSubgroup(self, options)

    def makeKey(self, unitId):
        unitId = self._makeId(unitId)
        if self.siteCode and unitId:
            return self.siteCode + '_' + unitId
        else:
            return unitId

    def _makeId(self, unitId):
        return str(unitId)

    def subgroup(self):
        self.subgroupMatrix.clear()
        if len(self._subgroups) == 0:
            return
        for reln in self.matrix.relationships():
            sg1 = self.unit(reln[0]).subgroup()
            sg2 = self.unit(reln[1]).subgroup()
            if sg1 and sg2 and sg1 != sg2:
                self.subgroupMatrix.addRelationship(sg1, Matrix.Above, sg2)
        self.subgroupMatrix.reduce()
