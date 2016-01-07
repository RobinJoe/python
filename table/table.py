#!/bin/python3

# Script for converting RST grid tables into list-tables

import logging
import argparse
from os import path

home = path.expanduser("~")
script_dir = path.dirname(path.realpath(__file__))

# ----------------------------------------------------------


def readRST(infile):  # reads RST data from file and returns array
    infile = path.realpath(infile)
    array = []
    try:
        with open(infile, 'rb') as f:
            data = f.read()
            for row in data:
                array.append(row)
    except IOError as ioerr:
        logging.error('File error (readData): ' + str(ioerr))
    return(array)


def writeRST(outfile, data):  # writes RST list-table to file
    outfile = path.realpath(outfile)
    try:
        with open(outfile, 'wb') as f:
            f.write(data)
    except IOError as ioerr:
        logging.error('File error (writeData): ' + str(ioerr))


def adjustRow(row, hw):
    # logic here
    # if line starts with '+' return new row '*' in list-table
    return(row)


def adjustTable(array):
    hw = []  # number of columns based on the headers
    for header in array[0]:
        hw.append(len(header)+2)
    new_array = []
    for row in array:
        # logic here
        pass
    return(new_array)


def buildTable(infile, outfile, manual):
    array = readCSV(infile)
    # logic here
    if outfile:
        writeRST(outfile, list_table)
    else:
        print(rst_table)


def menu():
    parser = argparse.ArgumentParser(prog="table",
                                     description='''Convert RST grid table
                                     to list-table''')
    parser.add_argument('INPUT', type=str, help='''input RST file containing a
                        single table''')
    parser.add_argument('OUTPUT', type=str, nargs='?', default=None,
                        help='output RST file')
    parser.add_argument('--head', action='store_false',
                        help='use first line as header')
    parser.add_argument('-t', type=str, nargs='?', default=None,
                        help='table title')
    parser.add_argument('-w', type=str, nargs='?', default=None,
                        help='width of columns')
    args = parser.parse_args()
    # buildTable(args.INPUT, args.OUTPUT, args.title, args.head, args.width)


if __name__ == '__main__':
    menu()
