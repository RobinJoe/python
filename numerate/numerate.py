#!/bin/python
#----------------------------------------------------------
# Takes doc text from a file or directly from the errata
# tool, cleans the tags and invalid characters, and
# reorders the bugs numerically for each component.
#----------------------------------------------------------

import argparse
import logging
import requests
import re
from os import getcwd, path
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
    infile = path.realpath(infile)
    try:
        with open(infile, 'rb') as f:
            xml = f.read()
    except IOError as ioerr:
        logging.error('File error (readData): ' + str(ioerr))
    return xml

def writeData(outfile, xml):  # writes XML to file
    outfile = path.realpath(outfile)
    try:
        with open(outfile, 'wb') as f:
            f.write(xml)
    except IOError as ioerr:
        logging.error('File error (writeData): ' + str(ioerr))

def isInt(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def precleanXML(string):
    # removes extra spaces
    string = re.sub(' +', ' ', string)
    return string

def postcleanXML(string):
    # swaps invalid characters for valid XML codes and removes extra whitespace in <screen> tags
    string = re.sub("`", "'", string)
    string = re.sub('C&U;', 'C&amp;U', string)
    string = re.sub(' & ', ' and ', string)
    string = re.sub('\r', '', string)
    string = re.sub('\t', '', string)
    string = re.sub('\n+', '\n', string)
    string = re.sub('\n ', '\n', string)
    string = re.sub('<screen>\s*', '<screen>', string)
    string = re.sub('\s*</screen>', '</screen>', string)
    return string

def stringFromList(array):
    outputstring = ''
    for item in array:
        outputstring = outputstring + item
    return outputstring

def fetchText(errata): # fetches doc text from the errata tool
    kbsource = 'HTTP@errata.devel.redhat.com'
    url = 'https://errata.devel.redhat.com/docs/draft_release_notes_xml/' + errata
    krb = KerberosTicket(kbsource)
    headers = {"Authorization": krb.auth_header}
    r = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser').find(id="publican_xml_snippet")
    return soup

def reorder(infile, outfile, replace):
    # reorder bugs numerically then print the result or write to file
    if isInt(infile):
        soup = fetchText(infile)
    else:
        soup = BeautifulSoup(readData(infile), 'html.parser')
    logging.debug(soup)

    temp = []

    for variablelist in soup('variablelist'):
        temp.append(str(variablelist))
    temp.sort()
    soup = BeautifulSoup(stringFromList(temp), 'html.parser')

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

    newsoup = BeautifulSoup(precleanXML(stringFromList(temp)), 'html.parser')
    outputstring = postcleanXML(newsoup.prettify(formatter=None, indent_width=2))

    if outfile:
        writeData(outfile, outputstring)
    elif replace:
        writeData(infile, outputstring)
    else:
        print outputstring

    # For testing
    return outputstring

#----------------------------------------------------------
# main

def main():
    logConfig()
    parser = argparse.ArgumentParser(prog="numerate", description="Clean tags and invalid characters, then order errata bugs numerically.")
    parser.add_argument('INPUT', type=str, help='input XML file or errata number')
    parser.add_argument('OUTPUT', type=str, nargs='?', default=None, help='output file')
    parser.add_argument('-r', '--replace', action='store_true', default=False, help='reorder bugs in input XML file')
    args = parser.parse_args()
    reorder(args.INPUT, args.OUTPUT, args.replace)

#===========================================================
# Logging Configuration

def logConfig():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='/home/bmoss/scripts/python/numerate/debug.log',
                        filemode='w')

#===========================================================

if __name__ == '__main__':
        main()