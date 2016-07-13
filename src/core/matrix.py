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

import networkx as nx

from unit import Unit

# Create a key, if a Unit then use the internal key
def _key(unit):
    if isinstance(unit, Unit):
        return unit.key()
    return unit

def _keys(units):
    keys = []
    for unit in units:
        set.append(_key(unit))
    return sorted(keys)

def _sortedKeys(units):
    keys = set()
    for unit in units:
        keys.add(_key(unit))
    return sorted(keys)

"""
A class to store, query, and manipulate a Harris Matrix.

This class is designed for speed rather than correctness, i.e. it is possible
to add cycles and self-cycles. Matrices must be validated and reduced after
new edges have been added.
"""

class Matrix():

    Above = 0
    Below = 1
    SameAs = 2
    ContemporaryWith = 3

    _strat = None # DiGraph()
    _same = None # Graph()
    _contemp = None # Graph()

    def __init__(self):
        self._strat = nx.DiGraph()
        self._same = nx.Graph()
        self._contemp = nx.Graph()

    def __contains__(self, unit):
        key = _key(unit)
        return key in self._strat or key in self._same or key in self._contemp

    def info(self):
        info = 'Strat Units: ' + str(self._strat.number_of_nodes()) + '\n'
        info = info + 'Strat Relationships: ' + str(self._strat.number_of_edges()) + '\n'
        info = info + 'Same As Relationships: ' + str(self._same.number_of_edges()) + '\n'
        info = info + 'Contemporary Relationships: ' + str(self._contemp.number_of_edges()) + '\n'
        info = info + 'Is Valid: ' + str(self.isValid()) + '\n'
        if self.isValid():
            info = info + 'Longest Path: ' + str(nx.dag_longest_path_length(self._strat)) + '\n'
        return info

    def isValid(self):
        """Return True if this Matrix, i.e. a Directed Acyclic Graph"""
        return nx.is_directed_acyclic_graph(self._strat)

    def clear(self):
        """Clears the matrix"""
        self._strat.clear()
        self._same.clear()
        self._contemp.clear()

    def addRelationship(self, fromUnit, reln, toUnit):
        """
        Add a relationship between two stratigraphic units.

        No validation is performed other than for self-cycles.

        A unit may be any hashable type such as string, number, or hashable class.
        """
        fromUnit = _key(fromUnit)
        toUnit = _key(toUnit)
        if fromUnit == toUnit:
            return False
        if reln == Matrix.Above:
            self._strat.add_edge(fromUnit, toUnit)
            return True
        elif reln == Matrix.Below:
            self._strat.add_edge(toUnit, fromUnit)
            return True
        elif reln == Matrix.SameAs:
            try:
                self._contemp.remove_edge(fromUnit, toUnit)
            except:
                pass
            self._same.add_edge(fromUnit, toUnit)
            return True
        elif reln == Matrix.ContemporaryWith:
            try:
                self._same.remove_edge(fromUnit, toUnit)
            except:
                pass
            self._contemp.add_edge(fromUnit, toUnit)
            return True
        return False

    def addRelationships(self, fromUnit, reln, toUnits):
        """
        Add a relationship between a source unit and a group of destination units.

        The destination group may be any iterable collection.
        """
        fromUnit = _key(fromUnit)
        toUnits = _sortedKeys(toUnits)
        if reln == Matrix.Above:
            toUnits.insert(0, fromUnit)
            self._strat.add_star(toUnits)
        elif reln == Matrix.Below:
            for toUnit in toUnits:
                self._strat.add_edge(toUnit, fromUnit)
        elif reln == Matrix.SameAs:
            for toUnit in toUnits:
                try:
                    self._contemp.remove_edge(fromUnit, toUnit)
                except nx.NetworkXError:
                    pass
            toUnits.insert(0, fromUnit)
            self._same.add_star(toUnits)
        elif reln == Matrix.ContemporaryWith:
            for toUnit in toUnits:
                try:
                    self._same.remove_edge(fromUnit, toUnit)
                except nx.NetworkXError:
                    pass
            toUnits.insert(0, fromUnit)
            self._contemp.add_star(toUnits)

    def addRelationshipChain(self, unitsChain):
        """Add a chain of Above/Below relationships in the order of the input list."""
        self._strat.add_path(_keys(unitsChain))

    def removeRelationship(self, fromUnit, reln, toUnit):
        """Remove a relationship from the Matrix if it exists."""
        fromUnit = _key(fromUnit)
        toUnit = _key(toUnit)
        if reln == Matrix.Above:
            try:
                self._strat.remove_edge(fromUnit, toUnit)
                return True
            except nx.NetworkXError:
                return False
        elif reln == Matrix.Below:
            try:
                self._strat.remove_edge(toUnit, fromUnit)
                return True
            except nx.NetworkXError:
                return False
        elif reln == Matrix.SameAs:
            try:
                self._same.remove_edge(fromUnit, toUnit)
                return True
            except nx.NetworkXError:
                return False
        elif reln == Matrix.ContemporaryWith:
            try:
                self._same.remove_edge(fromUnit, toUnit)
                return True
            except nx.NetworkXError:
                return False
        return False

    def hasRelationship(self, fromUnit, reln, toUnit):
        """Return True if a relationship type exists between two units."""
        fromUnit = _key(fromUnit)
        toUnit = _key(toUnit)
        if reln == Matrix.Above:
            return self._strat.has_edge(fromUnit, toUnit)
        elif reln == Matrix.Below:
            return self._strat.has_edge(toUnit, fromUnit)
        elif reln == Matrix.SameAs:
            return self._same.has_edge(fromUnit, toUnit)
        elif reln == Matrix.ContemporaryWith:
            return self._contemp.has_edge(fromUnit, toUnit)
        return False

    def relationships(self, unit, reln):
        """Returns a list of all units with a relationship of a certain type to a unit."""
        unit = _key(unit)
        if reln == Matrix.Above:
            return self._strat.predecessors(unit)
        elif reln == Matrix.Below:
            return self._strat.successors(unit)
        elif reln == Matrix.SameAs:
            return self._same.neighbours(unit)
        elif reln == Matrix.ContemporaryWith:
            return self._contemp.neighbours(unit)
        return []

    def predecessors(self, unit):
        """Returns a list of all units immediately above a given unit in the matrix"""
        return self._strat.predecessors(_key(unit))

    def successors(self, unit):
        """Returns a list of all units immediately below a given unit in the matrix"""
        return self._strat.successors(_key(unit))

    def sameAs(self, unit):
        """Returns a list of all units the same as a given unit in the matrix"""
        return self._same.neighbours(_key(unit))

    def contemporaryWith(self, unit):
        """Returns a list of all units contemporary with a given unit in the matrix"""
        return self._contemp.neighbours(_key(unit))

    def ancestors(self, unit):
        """Returns a list of all units above a given unit in the matrix"""
        return nx.ancestors(self._strat, _key(unit))

    def descendents(self, unit):
        """Returns a list of all units below a given unit in the matrix"""
        return nx.descendents(self._strat, _key(unit))

    def hasUnit(self, unit):
        """Returns True if the matrix contains the given unit."""
        return self.__contains__(_key(unit))

    def cycles(self):
        """Returns a list of any cycles in the matrix."""
        return nx.simple_cycles(self._strat)

    def reduce(self, remove=True):
        """Reduces a valid matrix by removing redundant edges. This transforms the matrix in place."""
        edges = []
        # Can only uniquely reduce the matrix if it is a DAG, i.e. no cycles or self-cycles
        if not self.isValid():
            return edges
        # Transitive reduction algorithm found on StackOverflow, algorithm originally from GraphViz tred
        # http://stackoverflow.com/questions/17078696/im-trying-to-perform-the-transitive-reduction-of-directed-graph-in-python
        for root in self._strat.nodes_iter():
            for gen1 in self._strat.successors(root):
                # Skip the direct children, look at every grandchild instead
                for gen2 in self._strat.successors(gen1):
                    # For the grandchild and all its decendents, remove any direct links back to the original unit
                    for toUnit in nx.dfs_preorder_nodes(self._strat, gen2):
                        if self._strat.has_edge(root, toUnit):
                            edges.append((root, toUnit))
                            if remove:
                                self._strat.remove_edge(root, toUnit)
        return edges

    def redundant(self):
        """Returns a list of any redundant edges without removing them."""
        return self.reduce(False)

    def weight(self, fromUnit, toUnit):
        return self._strat[_key(fromUnit)][_key(toUnit)]['weight']

    def weightForDegree(self):
        for edge in self._strat.edges_iter():
            weight = 1
            if self._strat.out_degree(edge[0]) == 1:
                weight += 2
            if self._strat.in_degree(edge[1]) == 1:
                weight += 2
            self._strat[edge[0]][edge[1]]['weight'] = weight
