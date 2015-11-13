#!/bin/python

# Fetch lastest reviews from watched projects

import logging
import requests
import json
from os import path

HOST = 'https://review.openstack.org/a/'
ENDPOINT = 'changes/'
QUERY = '?q=status:open+is:watched&n=10'
FORMAT = 'Accept: application/json'
KEYFILE = path.expanduser('~/scripts/python/grit/pass.key')
LOGFILE = path.expanduser('~/scripts/python/grit/output.log')

# ----------------------------------------------------------
# CLI colours:
#    HEADER = '\033[95m'
#    OKBLUE = '\033[94m'
#    OKGREEN = '\033[92m'
#    WARNING = '\033[93m'
#    FAIL = '\033[91m'
#    ENDCOLOR = '\033[0m'
# ----------------------------------------------------------


def fetchKey():  # fetch key from file
    try:
        with open(KEYFILE, 'rb') as f:
            logging.debug('Open ' + KEYFILE)
            key = f.read()
            logging.info('Key fetched')
    except IOError as ioerr:
        logging.error('File error (fetchKey): ' + str(ioerr))
    return key

# ----------------------------------------------------------
# main


def main():
    logConfig()
    user, key = fetchKey().split(':')
    url = HOST + ENDPOINT + QUERY  # + ' ' + FORMAT
    try:
        r = requests.get(url, verify=True,
                         auth=requests.auth.HTTPDigestAuth(user, key))
        logging.debug('Content of request: ' + r.text)
    except Exception as e:
        logging.error(e)
        response = raw_input('\nWebsite error\nRetry? (y/n): ')
        if response == 'y':
            main()
        else:
            exit(0)
    logging.info('Loading json')
    try:
        text = r.text[4:]
        print text
        data = (json.loads(text))
        print data
    except Exception as e:
        logging.error(e)
        print('JSON decode error. See log.')
        exit(0)
    # do something with the decoded json here

# ===========================================================
# Logging Configuration


def logConfig():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=LOGFILE,
                        filemode='w')
    logging.captureWarnings(True)

# ===========================================================

if __name__ == '__main__':
    main()
