#!/bin/python3
"""
Convert RST grid tables to list-tables.

Basic usage:

    1. Copy the grid table into a file, e.g. 'input.rst'
    2. Convert the grid table to a list-table. The result is output to stdout:

       $ python table.py input.rst

Options:

    -o [FILE]   Write the converted table to [FILE]
    -t [TITLE]  Use [TITLE] as the table title

Important:

    Always build your document and compare the rendered list-table to the
    original rendered grid table. It is very possible that some errors may
    occur that require manual fixes, especially when converting complex tables.

Warning:

    This script does not handle cells that span multiple rows or columns. If
    you convert a table with these types of cells you may receive a parsing
    error when running sphinx-build

    Example:

        ERROR: Error parsing content block for the "list-table" directive:
               uniform two-level bullet list expected, but row 2 does not
               contain the same number of items as row 1 (4 vs 3)

    This indicates that the list-table needs manual clean-up. Look for a lines
    like this in the source:

       * - Alarms
         - Acknowledge an alarm    * - hello
         -
         - Yes

    Compare with the original table to determine the correct structure of the
    broken row.

Notes:

    The script sets all columns to the same width: 100 / col_num. After
    conversion, you may want to manually edit :width:

    The script automatically uses the first row of the table as a header.
    After covervsion, you may want to manually edit :header-rows:
"""

import argparse
import logging
from os import path

home = path.expanduser("~")
script_dir = path.dirname(path.realpath(__file__))

# ----------------------------------------------------------


def readfile(infile):
    """Read data from file and return string."""
    infile = path.realpath(infile)
    try:
        with open(infile, 'r') as f:
            data = f.read()
    except IOError as ioerr:
        logging.error('File error (readData): ' + str(ioerr))
    return(data)


def writefile(outfile, data):
    """Write data to file."""
    outfile = path.realpath(outfile)
    try:
        with open(outfile, 'w') as f:
            f.write(data)
    except IOError as ioerr:
        logging.error('File error (writeData): ' + str(ioerr))


def adjustRow(row, col_num):
    """Convert a grid row to a list-table row."""
    if row.startswith('+') is True:
        return('\n')
    row = row.split('|')
    new_row = []
    for entry in row:
        new_row.append(entry)
        try:
            new_row.pop(new_row.index(''))
        except:
            pass
    convert = []
    convert.append('  * - ' + new_row[0].strip())
    for entry in new_row[1:]:
        convert.append('\n     - ' + entry.strip())
    result = ' '.join(convert)
    return(result)


def buildTable(infile, outfile, title):
    """Build an RST list-table."""
    data = readfile(infile)
    data = data.splitlines()
    if title is None:
        title = ''
    col_num = data[0].count('+') - 1
    col_width = str(int(100 / col_num))
    col_width = (col_width + ' ') * col_num

    output = []
    for line in data:
        row = adjustRow(line, col_num)
        output.append(row)
    result = ' '.join(output)

    list_table = """.. list-table:: %s
   :widths: %s
   :header-rows: 1
   %s""" % (title, col_width, result)

    if outfile:
        writefile(outfile, list_table)
    else:
        print(list_table)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="table",
                                     description='''Convert RST grid table
                                     to list-table.''')
    parser.add_argument('INPUT', type=str, help='''input RST file containing a
                        single table''')
    parser.add_argument('-o', type=str, dest='file', default=None,
                        help='write the converted table to [FILE]')
    parser.add_argument('-t', type=str, dest='title', default=None,
                        help='use [TITLE] as the table title')
    args = parser.parse_args()
    buildTable(args.INPUT, args.file, args.title)
