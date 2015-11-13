#!/bin/python
# ----------------------------------------------------------
# Script for building RST tables from CSV lists that
# narrows the table to the width of the headers.
#
# To adjust column width, add additional characters to
# the header of the relevant column.
# ----------------------------------------------------------

import argparse
import logging
import csv
from os import path
from tabulate import tabulate

home = path.expanduser("~")
script_dir = path.dirname(path.realpath(__file__))

# ----------------------------------------------------------


def readCSV(infile):  # reads CSV data from file and returns array
    infile = path.realpath(infile)
    array = []
    try:
        with open(infile, 'rb') as f:
            data = csv.reader(f)
            for row in data:
                array.append(row)
    except IOError as ioerr:
        logging.error('File error (readData): ' + str(ioerr))
    return array


def writeRST(outfile, data):  # writes RST table to file
    outfile = path.realpath(outfile)
    try:
        with open(outfile, 'wb') as f:
            f.write(data)
    except IOError as ioerr:
        logging.error('File error (writeData): ' + str(ioerr))


def adjustRow(row, hw):
    counter = 0
    next_row = []
    for entry in row:
        if len(entry) > hw[counter]:
            if entry[hw[counter]] != " " and entry[hw[counter]-1] != " ":
                row[counter] = entry[:hw[counter]] + "\\"
            else:
                row[counter] = entry[:hw[counter]]
            next_row.append(entry[hw[counter]:])
        else:
            row[counter] = entry
            next_row.append(" " * hw[counter])
        counter += 1
    return row, next_row


def adjustTable(array):
    hw = []  # width of each column based on the headers
    for header in array[0]:
        hw.append(len(header)+2)
    new_array = []
    for row in array:
        row, next_row = adjustRow(row, hw)
        new_array.append(row)
        row, next_row = adjustRow(next_row, hw)
        new_array.append(row)
        row, next_row = adjustRow(next_row, hw)
        new_array.append(row)
        row, next_row = adjustRow(next_row, hw)
        new_array.append(row)
        row, next_row = adjustRow(next_row, hw)
        new_array.append(row)
        row, next_row = adjustRow(next_row, hw)
        new_array.append(row)
    return new_array


def buildTable(infile, outfile, manual):
    array = readCSV(infile)
    if manual is False:
        array = adjustTable(array)
    rst_table = tabulate(array, headers="firstrow", tablefmt="grid")
    # , stralign=None)
    if outfile:
        writeRST(outfile, rst_table)
    else:
        print rst_table

# ----------------------------------------------------------
# main


def main():
    logConfig()
    parser = argparse.ArgumentParser(prog="table",
                                     description='''Creates RST tables for
                                     set widths.''')
    parser.add_argument('INPUT', type=str, help='input CSV file')
    parser.add_argument('OUTPUT', type=str, nargs='?', default=None,
                        help='output RST file')
    parser.add_argument('-m', '--manual', action='store_true', default=False,
                        help='reflow cells manually')
    args = parser.parse_args()
    buildTable(args.INPUT, args.OUTPUT, args.manual)

# ===========================================================
# Logging Configuration


def logConfig():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=script_dir + '/debug.log',
                        filemode='w')

# ===========================================================

if __name__ == '__main__':
    main()
