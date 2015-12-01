#!/usr/bin/env python

import argparse
import logging
import json
import time
import sys
import re

from pymongo import MongoClient
from subprocess import Popen, PIPE
from datetime import datetime
from functools import partial

__version__ = 'v1.0.0-alpha'

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logger = logging.getLogger('obgs/farmer')

mongo = MongoClient('mongodb://localhost:27017/')

def ip2int(s):
    "Convert dotted IPv4 address to integer."
    return reduce(lambda a,b: a<<8 | b, map(int, s.split(".")))

def int2ip(i):
    "Convert 32-bit integer to dotted IPv4 address."
    return ".".join(map(lambda n: str(i>>n & 0xFF), [24,16,8,0]))

def processScan(scan):
    """
    Scan target with masscan for open ports, grabbing their banners
    """
    logger.info("processing target: %s" % scan['target'])
    scan['error'] = False
    p = Popen([ 'masscan',
                '--banners',
                '-oJ', '/tmp/tmpscan.json',
                '-p', '22,80,443',
                '--source-port', '60000', # TODO: config this as settings
                scan['target']], stdout=PIPE, stderr=PIPE)
    with p.stderr:
        # example: rate:  0.10-kpps, 19.14% done,   0:00:25 remaining, found=4
        # example: rate:  0.00-kpps, 100.00% done, waiting 7-secs, found=21
        reProgress = re.compile(r'([\d\.]+)% done, [\s]*([\d:]+) remaining, found=([\d]+)')
        reWaiting = re.compile(r'([\d\.]+)% done, [\s]*waiting (.+), found=([\d]+)')
        line = ''
        for c in iter(partial(p.stderr.read, 1), b''):
            if ord(c) == 0x0d or ord(c) == 0x0a:
                # process line
                m = reProgress.search(line)
                if m is not None:
                    logger.info('percentage found! %s%% done, %s remaining, %s found' % (m.group(1), m.group(2), m.group(3)))
                    # update scan status
                    scan['progress'] = float(m.group(1))
                    scan['remaining'] = m.group(2)
                    scan['found'] = int(m.group(3))
                    mongo.obgs.scans.update_one({"_id": scan['_id']}, {"$set": {"progress": scan['progress'], "remaining": scan['remaining'], "found": scan['found']}})
                m = reWaiting.search(line)
                if m is not None:
                    # update scan status only if remaining has changed
                    dirty = scan['remaining'] != m.group(2)
                    scan['progress'] = float(m.group(1))
                    scan['remaining'] = m.group(2)
                    scan['found'] = int(m.group(3))
                    if dirty:
                        logger.info('waiting found! %s%% done, waiting %s' % (m.group(1), m.group(2)))
                        mongo.obgs.scans.update_one({"_id": scan['_id']}, {"$set": {"progress": scan['progress'], "remaining": scan['remaining'], "found": scan['found']}})
                line = ''
            else:
                line += c
    p.wait()

    code = p.returncode
    if code is 0:
        print("Completed scan")
        with open('/tmp/tmpscan.json', 'r') as f:
            for line in iter(f.readline, b''):
                try:
                    # {   "ip": "192.168.1.114",   "ports": [ {"port": 80, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 63} ] },
                    if 'ip' not in line:
                        continue
                    host = json.loads(line[:-2])
                    host['tstamp'] = datetime.utcnow()
                    host['scan_id'] = scan['_id']
                    h = mongo.obgs.hosts.find_one({"scan_id": host['scan_id'], "ip": host['ip'], "tstamp": {"$gt": scan['tstamp']}})
                    if h is not None:
                        mongo.obgs.hosts.update_one({"_id": h['_id']}, {"$push": {"ports": {"$each": host['ports']}}})
                    else:
                        mongo.obgs.hosts.replace_one({"scan_id": host['scan_id'], "ip": host['ip']}, host, True)
                except Exception as e:
                    logger.error(e)
    else:
        print("Error in scan with code %d" % code)
        scan['error'] = True
    scan['finished'] = True
    mongo.obgs.scans.update_one({"_id": scan['_id']}, {"$set": {"finished": scan['finished'], "error": scan['error']}})

def processQueue(name):
    """
    Process scans queue
    """
    pendingQuery = {"launched": False, "finished": False}
    processedFirst = False
    count = mongo.obgs.scans.find(pendingQuery).count()
    while count > 0:
        if not processedFirst:
            logger.info('processing %d items from queue %s', count, name)
            processedFirst = True
        scan = mongo.obgs.scans.find_one_and_update(pendingQuery, {'$set': { 'launched': True }})
        processScan(scan)
        count = mongo.obgs.scans.find(pendingQuery).count()
    if not processedFirst:
        logger.debug('no items to process for queue %s', name)

# entry point
def main():
    # define cli program
    parser = argparse.ArgumentParser(prog='farmer')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-v', action='count', help='set verbosity level')

    # parse arguments
    args = parser.parse_args()

    # set verbose level
    if args.v >= 2:
        logger.setLevel(logging.DEBUG)
    elif args.v == 1:
        logger.setLevel(logging.INFO)

    # init
    logger.info("listening for scans on queue")

    # loop!
    while True:
        processQueue('scans')
        time.sleep(10)

if __name__ == "__main__":
    main()
