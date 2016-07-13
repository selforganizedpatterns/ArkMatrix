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

import sys

from src.core.project import Project

def process(infile, informat, outfile, outformat, dataset='', site='', reduceMatrix=False, orphans=False, style=False, sameas=False, width=None, height=None):
    project = Project(dataset, site)
    project.readFile(infile, informat)

    sys.stdout.write('Original Matrix\n')
    sys.stdout.write(project.info())

    if not project.matrix.isValid():
        sys.stdout.write('Invalid Matrix\n')
        for cycle in project.matrix.cycles():
            sys.stdout.write('Cycle: ' + str(cycle) + '\n')
    elif reduceMatrix:
        edges = project.matrix.reduce()
        sys.stdout.write('Reduced Matrix:\n')
        sys.stdout.write('Removed Relationships: ' + str(len(edges)) + '\n')
        for edge in edges:
            sys.stdout.write('    ' + str(edge[0]) + ' above ' + str(edge[1]) + '\n')
        sys.stdout.write(project.info())
    else:
        edges = project.matrix.redundant()
        sys.stdout.write('Redundant Relationships: ' + str(len(edges)) + '\n')
        for edge in edges:
            sys.stdout.write('    ' + str(edge[0]) + ' above ' + str(edge[1]) + '\n')

    if not orphans:
        project.removeOrphans()

    if outfile and outformat and outformat != 'none':
        old_stdout = sys.stdout
        sys.stdout = outfile
        project.writeFile(outformat, style, sameas, width, height)
        sys.stdout = old_stdout
