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

def process(infile, outfile, subgroupfile, groupfile, options):
    project = Project(options['name'], options['site'])
    project.readFile(infile, options['input'])

    sys.stdout.write('\nOriginal Matrix:\n\n')
    sys.stdout.write(project.info())

    if not options['orphans']:
        project.removeOrphans()

    sys.stdout.write('\n\nProcessed Matrix:\n\n')
    if not project.matrix.isValid():
        sys.stdout.write('Invalid Matrix\n')
        for cycle in project.matrix.cycles():
            sys.stdout.write('Cycle: ' + str(cycle) + '\n')
    else:
        if options['reduce']:
            edges = project.matrix.reduce()
            sys.stdout.write('  Removed Relationships: ' + str(len(edges)) + '\n')
            for edge in edges:
                sys.stdout.write('    ' + str(edge[0]) + ' above ' + str(edge[1]) + '\n')
            sys.stdout.write('\n')
            sys.stdout.write(project.info())
        else:
            edges = project.matrix.redundant()
            sys.stdout.write('  Redundant Relationships: ' + str(len(edges)) + '\n')
            for edge in edges:
                sys.stdout.write('    ' + str(edge[0]) + ' above ' + str(edge[1]) + '\n')
        if options['group']:
            sys.stdout.write('\n\nSubgroup Matrix:\n\n')
            project.subgroup()
            if project.subgroupMatrix.count() > 0:
                sys.stdout.write(project.subgroupMatrix.info())
                sys.stdout.write('\n\nGroup Matrix:\n\n')
                project.group()
                if project.groupMatrix.count() > 0:
                    sys.stdout.write(project.groupMatrix.info())
                else:
                    sys.stdout.write('  No Group Matrix generated\n\n')
            else:
                sys.stdout.write('  No Subgroup Matrix generated\n\n')

    if outfile and options['output'] != 'none':
        old_stdout = sys.stdout
        sys.stdout = outfile
        project.writeFile(options['output'], options)
        if options['group']:
            if subgroupfile and options['subgroupoutput'] != 'none':
                sys.stdout = subgroupfile
                project.writeSubgroupFile(options['subgroupoutput'], options)
            if groupfile and options['groupoutput'] != 'none':
                sys.stdout = groupfile
                project.writeGroupFile(options['groupoutput'], options)
        sys.stdout = old_stdout

    sys.stdout.write('\n')
