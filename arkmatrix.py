#!/usr/bin/env python
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

import os, sys, argparse

from src import process

parser = argparse.ArgumentParser(description='A tool to process Harris Matrix files.')
parser.add_argument("-i", "--input", help="Choose input format, optional, defaults to infile suffix", choices=['lst', 'csv'])
parser.add_argument("-o", "--output", help="Choose output format, optional, defaults to outfile suffix", choices=['none', 'gv', 'dot', 'gml', 'graphml', 'gxl', 'tgf', 'csv'])
parser.add_argument("-n", "--name", help="Name for Matrix", default='')
parser.add_argument("-t", "--site", help="Site Code for Matrix", default='')
parser.add_argument("-r", "--reduce", help="Apply a transitive reduction to the input graph", action='store_true')
parser.add_argument("-s", "--style", help="Include basic style formatting in output", action='store_true')
parser.add_argument("-p", "--orphans", help="Include orphan units in output (format dependent)", action='store_true')
parser.add_argument("-wn", "--width", help="Width of node if --style is set", type=float, default=50.0)
parser.add_argument("-a", "--sameas", help="Include Same-As relationships in output", action='store_true')
parser.add_argument("-hn", "--height", help="Height of node if --style is set", type=float, default=25.0)
parser.add_argument('infile', help="Source data file", nargs='?', type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('outfile', help="Destination data file", nargs='?', type=argparse.FileType('w'), default=sys.stdout)

args = parser.parse_args()

informat = 'lst'
outformat = 'none'

if args.input:
    informat = args.input
elif args.infile.name != '<stdin>':
    basename, informat = os.path.splitext(args.infile.name)
    informat = informat.strip('.')
informat = informat.lower()

if args.output:
    outformat = args.output
elif args.outfile.name != '<stdout>':
    basename, outformat = os.path.splitext(args.outfile.name)
    outformat = outformat.strip('.')
outformat = outformat.lower()

process.process(args.infile, informat, args.outfile, outformat, args.name, args.site, args.reduce, args.orphans, args.style, args.sameas, args.width, args.height)
