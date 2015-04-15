#!/bin/python
#----------------------------------------------------------
# Creates a Docbook XML table from a CSV file
#
# CSV file must be encoded in ASCII or UTF-8
#----------------------------------------------------------

import argparse
import csv
import re
from os import path
from bs4 import BeautifulSoup

#----------------------------------------------------------
# Hack to set the indent for prettify

orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)

def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))

BeautifulSoup.prettify = prettify

#----------------------------------------------------------

def readCSV(infile):
    # reads CSV from file and returns a matrix of rows
    infile = path.realpath(infile)
    matrix = []
    try:
        with open(infile, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                matrix.append(row)
    except IOError as ioerr:
        logging.error('File error (readData): ' + str(ioerr))
    return matrix

def writeXML(outfile, xml):
    # writes an XML string to file
    outfile = path.realpath(outfile)
    try:
        with open(outfile, 'wb') as f:
            f.write(xml)
        print("XML saved to " + outfile)
    except IOError as ioerr:
        logging.error('File error (writeData): ' + str(ioerr))

def createRow(row_list):
    # creates an XML <row> from the entries in row_list
    soup = BeautifulSoup("<row></row>", "xml")
    for cell in row_list:
        entry = soup.new_tag("entry")
        entry.string = cell
        soup.row.append(entry)
    return soup.row

def buildTable(matrix, section):
    # returns an XML <informaltable> built from a matrix of rows
    if section is True:
        soup = BeautifulSoup('''<section>
                                    <title>Insert Title Here</title>
                                    <informaltable>
                                        <tgroup>
                                        </tgroup>
                                    </informaltable>
                                </section>''', "xml")
    else:
        soup = BeautifulSoup('''<informaltable>
                                    <tgroup>
                                    </tgroup>
                                </informaltable>''', "xml")

    # tgroup
    cols = 'cols="' + str(len(matrix[1])) + '"'
    soup.tgroup['cols'] = str(len(matrix[1]))

    # thead
    thead = soup.new_tag("thead")
    soup.tgroup.append(thead)
    header = matrix.pop(0)
    thead.append(createRow(header))

    # tbody
    tbody = soup.new_tag("tbody")
    soup.tgroup.append(tbody)
    for row in matrix:
        tbody.append(createRow(row))

    return soup.prettify()

#----------------------------------------------------------
# main

def main():
    parser = argparse.ArgumentParser(prog="csv2xml", description="Creates a Docbook XML table from a CSV file")
    parser.add_argument('INPUT', type=str, help='CSV file')
    parser.add_argument('OUTPUT', type=str, nargs='?', default=None, help='XML file')
    parser.add_argument('-s', '--section', action='store_true', default=False, help='Add section tags')
    args = parser.parse_args()
    print("Generating table...\n")
    table = buildTable(readCSV(args.INPUT),args.section)
    if args.OUTPUT is not None:
        writeXML(args.OUTPUT, table)
    else:
        print(table + "\nTable complete.")

#===========================================================

if __name__ == '__main__':
        main()