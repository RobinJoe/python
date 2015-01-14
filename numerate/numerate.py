#!/bin/python
#----------------------------------------------------------
# Takes doc text from a file or directly from the errata tool
# and reorders the bugs numerically for each component.
#----------------------------------------------------------

import argparse
import logging
import requests
import re
from bs4 import BeautifulSoup
from kb import KerberosTicket # there is a requests-kerberos pip package that probably does this better, but I was getting errors installing it on CSB

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

#def fetchText(errata):
#    url = 'https://errata.devel.redhat.com'
#
#    # kerberos stuff
#
#    docurl = url + '/docs/draft_release_notes_xml/' + errata
#
#    r = requests.get(docurl, verify=False)
#    soup = BeautifulSoup(r.text, from_encoding='utf-8').textarea
#    print soup

def reorder(infile, outfile, replace):  # reorder bugs numerically then print the result or write to file
    soup = BeautifulSoup(readData(infile), 'html.parser')
    temp = []

    for variablelist in soup('variablelist'):
        temp.append('<variablelist>' + str(variablelist.title))
        subtemp = []
        for varlistentry in variablelist('varlistentry'):
            subtemp.append(str(varlistentry))
        subtemp.sort()
        for bug in subtemp:
            temp.append(bug)
        temp.append('</variablelist>')

    outputstring = ''
    for item in temp:
        outputstring = outputstring + item
    outputstring = re.sub('\n+', '\n', outputstring)

    newsoup = BeautifulSoup(outputstring, 'html.parser')

    if outfile:
        writeData(outfile, newsoup.prettify(formatter=None, indent_width=2))
    elif replace:
        writeData(infile, newsoup.prettify(formatter=None, indent_width=2))
    else:
        print newsoup.prettify(formatter=None, indent_width=2)

#----------------------------------------------------------
# main

def main():
    logConfig()
    parser = argparse.ArgumentParser(prog="numerate", description="Order errata bugs numerically.")
    parser.add_argument('INPUT', type=str, help='input file')
    parser.add_argument('OUTPUT', type=str, nargs='?', default=None, help='output file')
    parser.add_argument('-r', '--replace', action='store_true', default=False, help='reorder bugs in input file')
    args = parser.parse_args()
    #fetchText('19347')
    reorder(args.INPUT, args.OUTPUT, args.replace)

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