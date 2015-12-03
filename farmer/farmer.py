#!/usr/bin/env python

import argparse
import logging
import json
import time
import sys
import re

from copy import deepcopy
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

def processScanResult(scan, stream):
    for line in iter(stream.readline, b''):
        try:
            # {   "ip": "192.168.1.114",   "ports": [ {"port": 80, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 63} ] },
            if 'finished' in line:
                stats = json.loads(line)
                scan['elapsed'] = stats['elapsed']
                scan['found'] = stats['up']
                continue
            elif 'ip' not in line:
                continue
            parsed = json.loads(line[:-2])
            parsed['tstamp'] = datetime.utcnow()
            parsed['scan_id'] = scan['_id']
            host = mongo.obgs.hosts.find_one({"scan_id": parsed['scan_id'], "ip": parsed['ip']})
            if host is None:
                host = deepcopy(parsed)
            for p in parsed['ports']:
                port = next((x for x in host['ports'] if p['port'] == x['port']), None)
                service = p.pop('service', None)
                if port is None:
                    host['ports'].append(p)
                elif service is None:
                    pass
                else:
                    if 'services' not in port:
                        port['services'] = []
                    port['services'].append(service)
            mongo.obgs.hosts.replace_one({"scan_id": parsed['scan_id'], "ip": parsed['ip']}, host, True)
        except Exception as e:
            logger.error("%s %s" % (type(e), e))

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
                    logger.info('\tscan %s %s%% done, %s remaining, %s found' % (scan['_id'], m.group(1), m.group(2), m.group(3)))
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
                    if dirty:
                        logger.info('\tscan %s %s%% done, waiting %s' % (scan['_id'], m.group(1), m.group(2)))
                        mongo.obgs.scans.update_one({"_id": scan['_id']}, {"$set": {"progress": scan['progress'], "remaining": scan['remaining'], "found": scan['found']}})
                line = ''
            else:
                line += c
    p.wait()

    code = p.returncode
    if code is 0:
        logger.info("Completed scan, processing results...")
        with open('/tmp/tmpscan.json', 'r') as f:
            processScanResult(scan, f)
        logger.info("Results processed correctly")
    else:
        logger.error("Error in scan with code %d" % code)
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
    parser.add_argument('--json', help='parse from JSON file')

    # parse arguments
    args = parser.parse_args()

    # set verbose level
    if args.v >= 2:
        logger.setLevel(logging.DEBUG)
    elif args.v == 1:
        logger.setLevel(logging.INFO)

    # init
    logger.info("listening for scans on queue")

    # parse from JSON file
    if args.json:
        logger.info("parsing masscan results from JSON file")
        scan = {"finished": True, "error": False, "remaining":0, "progress":100.0, "target":"file"}
        scan['_id'] = mongo.obgs.scans.insert_one(scan).inserted_id
        with open(args.json) as f:
            processScanResult(scan, f)
        return

    # loop!
    while True:
        processQueue('scans')
        time.sleep(2)

if __name__ == "__main__":
    main()
