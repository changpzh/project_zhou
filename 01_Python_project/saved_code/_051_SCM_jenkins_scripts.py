#!/usr/bin/env python
''' monitor PCI SCM data,
and if data is lost in mongoBD,
notification email should be sent to SCM&I_EXT_MBB_COMMON_CI_DEV_GMS DG
'''
import logging
import os
import sys
import re
import urllib2
import time,datetime
urllib2.getproxies = lambda: {} # unset http_proxy
import gevent
from gevent import sleep
from gevent import subprocess
from gevent.lock import RLock
import json
import ast
from pymongo import MongoClient

# URLs to monitor
BUILDS = {'macrotdd': 'http://hzling23.china.nsn-net.net:8080/job/LTE_eNB_FSM3_TDD_trunk/'}

COLLECTIONS = {'macrotdd': ''}

LAST_MONITOR_DUMP = os.path.join(os.path.dirname(__file__), 'scm_data.json')

_LOCK = RLock() # lock when updating last_revisions

if os.path.exists(LAST_MONITOR_DUMP):
    with open(LAST_MONITOR_DUMP) as fp:
        last_build_numbers = json.load(fp)
else:
    last_build_numbers = {}

errors = []

def log(filename='scmDataMonitor.log',level="DEBUG"):
    """logging function"""
    logging.basicConfig(filename=filename, level=logging.DEBUG, format='%(asctime)-6s: %(name)s - %(levelname)s - %(message)s')
    console = logging.StreamHandler(stream=sys.stdout)
    console.setLevel(level)
    console.setFormatter(logging.Formatter('%(message)s'))
    logger = logging.getLogger()
    logger.addHandler(console)

class MongoDBOperation():
    def __init__(self, product = 'macrotdd'):
        self.product = product
        self.ConnectionToDB()

    def ConnectionToDB(self):
        self.conn = MongoClient('127.0.0.1',27017)
        self.db = self.conn['pipeline']
        self.collection = self.db[self.product+'_trunkbuild']

    def SaveADoc(self):
        logging.info("Saving docs...")
        mydata = {"author": "John",
                "text": "My first post!",
                "tags": ["python", "pymongo", "mongoDB", "arangoDB"]
        }
        self.collection.insert(mydata)

    def QuerySingleDoc(self, arg):
        logging.info("First matching...")
        logging.info(self.collection.find_one(arg))

    def QueryDoc(self, arg):
        for doc in self.collection.find(arg):
            pass
            #logging.info(doc)
        return self.collection.find(arg).count()

def _get_buildid(url, number):
    url = url + str(number) + "/api/python?tree=actions[parameters[value]]"
    try:
        apiOriginData = urllib2.urlopen(url).read().decode('utf-8')
        apiDataDict = ast.literal_eval(apiOriginData)
        buildid = apiDataDict['actions'][0]['parameters'][0]['value']
        return buildid
    except Exception as err:
        if err:
            errors.append("failed to query buildid,and url is:" + url + "and error is:"+ str(err))

def _get_last_build_number(product):
    build_number = last_build_numbers.get(product, None)
    if build_number:
        return build_number.get('number', None)
    return None

def complication_is_finished(url, number):
    url = url + str(number) + "/api/python?tree=result"
    try:
        apiOriginData = urllib2.urlopen(url).read().decode('utf-8')
        apiDataDict = ast.literal_eval(apiOriginData)
        result = apiDataDict['result']
        return result
    except Exception as err:
        if err:
            errors.append("failed to get complication status,and url is:" + url + "and error is:"+ str(err))


def _get_all_builds(url):
    url = url+"api/python?tree=builds[number]"
    try:
        apiOriginData = urllib2.urlopen(url).read().decode('utf-8')
        apiDataDict = ast.literal_eval(apiOriginData)
        logging.info("*************jenkins builds list******************")
        logging.info(apiDataDict)
        return apiDataDict
    except Exception as err:
        if err:
            errors.append("failed to query builds number,and url is:" + url + "and error is:"+ str(err))

def exist_in_mongoDB(buildid, number, product):
    m = MongoDBOperation()
    m.product = product
    existinmongoDB = m.QueryDoc({"buildid" : buildid, "product": product})
    if not existinmongoDB:
        errors.append("failed to find the build:" + buildid + " build number: " + str(number) +" in mongoDB")
    return existinmongoDB

def _filter_all_builds(url, all_builds):
    new_list = []
    for build in  all_builds['builds']:
        if complication_is_finished(url, build['number']):
            new_list.append({'number': build['number']})
        else:
            logging.info("build " + str(build['number']) + " is going on...")
    return {'builds': new_list}

def save_last_build_numbers(builds, product):
    with _LOCK:
        last_build_numbers[product] = {
                'number': builds['builds'][0]['number'],
                'buildid': builds['builds'][0]['buildid']}
    logging.info("********the last build info************")
    logging.info(last_build_numbers)

def data_monitor(product, url):
    logging.info("the product is:" + product)
    builds = []
    #all_builds = {"builds":[{"number":3173},{"number":3166},{"number":3165},{"number":3164}]}
    all_builds = _get_all_builds(url)
    filter_all_builds = _filter_all_builds(url, all_builds)

    last_build_number = _get_last_build_number(product)
    logging.info("last build number is:" + str(last_build_number))

    if last_build_number:
        for build in filter_all_builds['builds']:
            if build['number'] > last_build_number:
                number = build['number']
                buildid = _get_buildid(url, number)
                existinmongodb = exist_in_mongoDB(buildid, number, product)
                builds.append({"number": number,
                    "buildid": buildid,
                    "existinmongodb": existinmongodb})
    else:
        number = filter_all_builds['builds'][0]['number']
        buildid = _get_buildid(url, number)
        existinmongodb = exist_in_mongoDB(buildid, number, product)
        builds.append({"number": number,
            "buildid": buildid,
            "existinmongodb": existinmongodb})

    new_builds = {'builds': builds}
    logging.debug("*****************new build list***************")
    logging.info(new_builds)
    if builds:
        save_last_build_numbers(new_builds, product)
    else:
        logging.info('no new builds for "%s"' % product)

def main():
    log()
    logging.info("we start...")
    for product,url in BUILDS.iteritems():
        gevent.spawn(data_monitor, product, url)
    gevent.wait()
    with open(LAST_MONITOR_DUMP, 'w+b') as fp:
        json.dump(last_build_numbers, fp)
    if errors:
        logging.debug("we got errors:\n%s" % '\n'.join(errors))
    sys.exit(len(errors))

if __name__ == '__main__':
    main()