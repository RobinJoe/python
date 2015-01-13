#!/bin/python

import argparse
import logging
import re
from bs4 import BeautifulSoup

#----------------------------------------------------------
# hack to set the indent for prettify
orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)

def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))

BeautifulSoup.prettify = prettify
#----------------------------------------------------------

def readData(infile):  # reads XML from file
    try:
        with open(infile, 'rb') as f:
            xml = f.read()
    except IOError as ioerr:
        logging.error('File error (readData): ' + str(ioerr))
    return xml

def writeData(outfile, xml):  # writes XML to file
    try:
        with open(outfile, 'wb') as f:
            f.write(xml)
    except IOError as ioerr:
        logging.error('File error (writeData): ' + str(ioerr))

def reorder(infile, outfile):
    soup = BeautifulSoup(readData(infile), 'html.parser')
    temp = {}

    #can this not be accomplished more efficiently using arrays in place of dicts?  This would also have the benefit of keeping the titles in order.  Although perhaps those should be sorted alphabetically.

    for variablelist in soup('variablelist'):
        subtemp = {}
        for varlistentry in variablelist('varlistentry'):
            subtemp[str(varlistentry.term)] = varlistentry
        temp[variablelist.title] = subtemp

    newsoup = BeautifulSoup('', 'html.parser')
    order = []

    for item in temp:
        order.append('<variablelist>')
        order.append(item)
        for key in sorted(temp[item]):
            order.append(temp[item][key])
        order.append('</variablelist>')

    for item in order:
        newsoup.append(item)

    outputstring = str(newsoup).strip()
    outputstring = outputstring.replace("\n","")

    newsoup = BeautifulSoup(outputstring, 'html.parser')

    writeData(outfile, newsoup.prettify(formatter=None, indent_width=2))

#----------------------------------------------------------
# main

def main():
    parser = argparse.ArgumentParser(prog="numerate", description="Order errata bugs numerically.")
    parser.add_argument('INPUT', type=str, help='input file')
    parser.add_argument('OUTPUT', type=str, help='output file')
    args = parser.parse_args()
    reorder(args.INPUT, args.OUTPUT)

#===========================================================
# Logging Configuration

def logConfig():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'),
                        #filename='/home/bmoss/code/python/cricket/output.log',
                        #filemode='w')

#===========================================================

if __name__ == '__main__':
	main()