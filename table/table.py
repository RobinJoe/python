#!/bin/python3

# Script for converting RST grid tables into list-tables

import logging
import re
import argparse
from os import path

home = path.expanduser("~")
script_dir = path.dirname(path.realpath(__file__))

# ----------------------------------------------------------


def readRST(infile):
    """Read RST data from file and return array."""
    infile = path.realpath(infile)
    try:
        with open(infile, 'rb') as f:
            data = f.read()
    except IOError as ioerr:
        logging.error('File error (readData): ' + str(ioerr))
    data = data.decode("utf-8")
    return(data)


def writeRST(outfile, data):
    """Write RST list-table to stdout or (optional) file."""
    outfile = path.realpath(outfile)
    try:
        with open(outfile, 'wb') as f:
            f.write(data)
    except IOError as ioerr:
        logging.error('File error (writeData): ' + str(ioerr))


def adjustRow(row, col_num):
    if row.startswith('+') is True:
        firstline = '  * '
    else:
        firstline = ''
    col = row.split('|')
    new_col = []
    for entry in col:
        new_col.append(entry) # stip this, but while leaving blank strings where required.
        try:
            new_col.pop(new_col.index(''))
        except:
            pass

    print(new_col)
    # new_row = firstline + '\n'
    # return(new_row)


def buildTable(infile, outfile, title):
    """
    Build the RST list-table.

    * - Category
      - Privilege
      - Available?
    * - Alarms
      - Acknowledge an alarm
      - Yes
    """
    data = readRST(infile)
    data = data.splitlines()
    if title is None:
        title = ''
    col_num = data[0].count('+') -1
    col_width = int(100 / col_num)

    output = []
    for line in data:
        row = adjustRow(line, col_num)
        output.append(row)
    result = ' '.join(output)

    list_table =""".. list-table:: %s
   :widths: %s
   :header-rows: 1

 %s""" % (title, col_width, result)

    if outfile:
        writeRST(outfile, list_table)
    else:
        print(list_table)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="table",
                                     description='''Convert RST grid table
                                     to list-table''')
    parser.add_argument('INPUT', type=str, help='''input RST file containing a
                        single table''')
    parser.add_argument('-o', type=str, nargs='?', default=None,
                        help='output RST file')
    parser.add_argument('-t', type=str, nargs='?', default=None,
                        help='table title')
    args = parser.parse_args()
    buildTable(args.INPUT, args.o, args.t)
