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

import itertools

class Unit():

    # Unit.Status enum
    Unassigned = 0
    Assigned = 1
    Void = 2
    Status = ['unassigned', 'assigned', 'void'];

    # Unit.Class enum
    Unknown = 0
    Deposit = 1
    Fill = 2
    Cut = 3
    Masonry = 4
    Skeleton = 5
    Class = ['unknown', 'deposit', 'fill', 'cut', 'masonry', 'skeleton'];

    _counter = itertools.count()
    _nid = 0
    _key = ''
    _siteCode = ''
    _id = ''
    _subgroup = ''
    _status = Unassigned # Unit.Status
    _class = Unknown # Unit.Type

    def __init__(self, siteCode, unitId, groupId='', status=Unassigned, unitType=Unknown):
        self._nid = Unit._counter.next()
        if siteCode:
            self._key = siteCode + '_' + str(unitId)
        else:
            self._key = str(unitId)
        self._siteCode = siteCode
        self._id = unitId
        self._group = groupId
        self._class = unitType

    def __str__(self):
        return self._key

    def __hash__(self):
        return hash(self._key)

    def __lt__(self, other):
        if not isinstance(other, Unit):
            return False
        elif self._siteCode == other._siteCode:
            return self._id < other._id
        else:
            return self._siteCode < other._siteCode and self._id < other._id

    def key(self):
        return self._key

    def siteCode(self):
        return self._siteCode

    def unitId(self):
        return self._id

    def setStatus(self, status):
        self._status = status

    def status(self):
        return self._status

    def setClass(self, unitClass):
        self._class = unitClass

    def unitClass(self):
        return self._class

    def setSubgroup(self, subgroupId):
        self._subgroup = subgroupId

    def subgroup(self):
        return self._subgroup
