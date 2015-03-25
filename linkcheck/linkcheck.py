#!/bin/python
#----------------------------------------------------------
# Takes DocBook XML a file or directory and checks ulinks.
#
# Note this only checks for a 200 response, it does not
# check that the destination contains the correct content.
#----------------------------------------------------------

import argparse
import logging
import requests
from os import path
from glob import iglob
from bs4 import BeautifulSoup

#----------------------------------------------------------
# Text color codes

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDCOLOR = '\033[0m'

#----------------------------------------------------------

def readData(infile):  # reads XML from file
    infile = path.realpath(infile)
    try:
        with open(infile, 'rb') as f:
            xml = f.read()
    except IOError as ioerr:
        logging.error('File error (readData): ' + str(ioerr))
    return xml

def checklinks(infile, count, total, verbose):
    # check links and either display invalid links or display
    # count of valid and invalid links

    soup = BeautifulSoup(readData(infile), 'html.parser')
    badlinks = []
    allcount, goodcount, badcount = 0, 0, 0

    for ulink in soup('ulink'):
        allcount += 1
        url = str(ulink).split('"')[1]
        if verbose: print("Checking link: " + url)
        try:
            status = requests.head(url).status_code
            if status == requests.codes.ok:
                status = OKGREEN + str(status)
                goodcount += 1
            else:
                status = FAIL + str(status)
                badlinks.append(status + ENDCOLOR + ": " + url)
                badcount += 1
            if verbose: print("Status: " + status + ENDCOLOR)
        except Exception as e:
            print(e)
    if count:
        if allcount > 0:
            print(HEADER + path.basename(infile) + ENDCOLOR)
            print("Total links: %s\n%sGood links: %s\n%sBad links: %s%s\n" % (allcount,OKGREEN,goodcount,FAIL,badcount,ENDCOLOR))
    elif total:
        pass
    elif badcount > 0:
        print(HEADER + path.basename(infile) + ENDCOLOR)
        for badlink in badlinks: print badlink
    return badcount

#----------------------------------------------------------
# main

def main():
    logConfig()
    parser = argparse.ArgumentParser(prog="linkcheck", description="Check ulinks in DocBook XML.")
    parser.add_argument('INPUT', type=str, help='input XML file or directory containing XML files')
    parser.add_argument('-c', '--count', action='store_true', default=False, help='Print count of invalid links per file')
    parser.add_argument('-t', '--total', action='store_true', default=False, help='Print the total number of invalid links')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output')
    args = parser.parse_args()
    badtotal = 0
    if path.isfile(args.INPUT):
        badtotal = checklinks(args.INPUT, args.count, args.total, args.verbose)
    else:
        for filename in iglob(args.INPUT + '*.xml'):
            badtotal += checklinks(filename, args.count, args.total, args.verbose)
    print("Total of all broken links: " + str(badtotal))

#===========================================================
# Logging Configuration

def logConfig():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='/home/bmoss/scripts/python/linkcheck/debug.log',
                        filemode='w')

#===========================================================

if __name__ == '__main__':
        main()