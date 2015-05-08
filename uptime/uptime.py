#!/bin/python

# Display status of sites monitored by Uptimerobot

import logging
import requests
import json
from os import path

HOST = 'http://api.uptimerobot.com/getMonitors?apiKey='
FORMAT = '&format=json&noJsonCallback=1'
KEYFILE = path.expanduser('~/scripts/python/uptime/pass.key')
LOGFILE = path.expanduser('~/scripts/python/uptime/output.log')
status_code = {'0': '\033[94mpaused', '1': 'not checked yet', '2': '\033[92mup', '8': '\033[93mseems down', '9': '\033[91mdown'}

#----------------------------------------------------------
# CLI colours:
#    HEADER = '\033[95m'
#    OKBLUE = '\033[94m'
#    OKGREEN = '\033[92m'
#    WARNING = '\033[93m'
#    FAIL = '\033[91m'
#    ENDCOLOR = '\033[0m'
#----------------------------------------------------------

def fetchKey():  # fetch API key from file
    try:
        with open(KEYFILE, 'rb') as f:
            logging.debug('Open ' + KEYFILE)
            key = f.read()
            logging.info('Key fetched')
    except IOError as ioerr:
        logging.error('File error (fetchKey): ' + str(ioerr))
    return key
    
#----------------------------------------------------------
# main

def main():
    logConfig()
    key = fetchKey()
    url = HOST + key + FORMAT
    try:
        r = requests.get(url)
        logging.debug('Content of request: ' + r.text)
    except Exception as e:
        logging.error(e)
        response = raw_input('\nWebsite error\nRetry? (y/n): ')
        if response == 'y': main()
        else: exit(0)
    logging.debug('Attempting to load json')
    data = (json.loads(r.text))
    print ''
    for monitor in data['monitors']['monitor']:
        print status_code[monitor['status']] + ' ' + monitor['alltimeuptimeratio'] + '%\033[0m ' + monitor['friendlyname']
    print ''
    
#===========================================================
# Logging Configuration

def logConfig():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=LOGFILE,
                        filemode='w')

#===========================================================

if __name__ == '__main__':
	main()