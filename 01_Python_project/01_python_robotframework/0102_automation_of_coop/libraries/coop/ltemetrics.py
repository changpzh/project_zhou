'''
@author: chaojwan
'''
import os
import urllib2
urllib2.getproxies = lambda: {} # unset http_proxy
import json
import time,datetime

errors = []
def get_data_from_coop(url):
    try:
        req = urllib2.Request(url)
        res = urllib2.urlopen(req).read().decode('utf-8')
        decode_res = json.loads(res)
    except urllib2.HTTPError as err:
        print err, 'message:', err.read()
    except Exception,err:
        errors.append(['url is:\n', url, '\n\nerr:\n', err.read()])
        if errors:
            print "got errors:\n"
            for error in errors:
                print '\n ', error        
    return decode_res

def time_string_2_timestamp(time_str, format):
    return int(time.mktime(time.strptime(time_str, '%Y-%m')))

def get_comparison_status(title, lteList, key, value2):
    if (lteList[key] == ''):
        lteList[key] = 0
    if (str(lteList[key]) == str(value2)):
        print title, '| ', 'ltemetrics: ', str(lteList[key]), ' | ', 'coop: ', str(value2)
        return "PASS"
    else:
        print title, '| ', 'ltemetrics: ', str(lteList[key]), ' | ', 'coop: ', str(value2)
        return "FAIL"

def get_comparison_status_special(date, title, lteList, key, coopList, coopKey):
    if (date > time.strftime("%Y-%m")):
        coopList[coopKey] = 0
    if (lteList[key] == ''):
        lteList[key] = 0
    if (str(lteList[key]) == str(coopList[coopKey])):
        print title, '| ', 'ltemetrics: ', str(lteList[key]), ' | ', 'coop: ', str(coopList[coopKey])
        return "PASS"
    else:
        print title, '| ', 'ltemetrics: ', str(lteList[key]), ' | ', 'coop: ', str(coopList[coopKey])
        return "FAIL"
    

def list_to_Dict(inList):
    tmpDict = {}
    for item in inList:
        print item['name'], " | ", item['num']
        tmpDict[item['name']] = str(item['num'])
    return tmpDict


def print_info(date, ltemetrics_url, coop_url, **options):
    lte_key = "lte"
    coop_key = "coop"
    print "Failed on %s:" % date
    print "Ltemetrics url: %s" % ltemetrics_url
    print "Coop url: %s" % coop_url
    print "Name         | ltemetrics | coop"
    if options.get("ncdr"):
        print "NCDR(A&B)    |   %s  | %s" % (str(options["ncdr"][lte_key]) if options["ncdr"][lte_key] != "" else 0, str(options["ncdr"][coop_key]))
    if options.get("a_status"):
        print "A-Critical   |   %s  | %s" % (str(options["a_status"][lte_key]) if options["a_status"][lte_key] != "" else 0, str(options["a_status"][coop_key]))
    if options.get("b_status"):
        print "B-Major      |   %s  | %s" % (str(options["b_status"][lte_key]) if options["b_status"][lte_key] != "" else 0, str(options["b_status"][coop_key]))
    if options.get("c_status"):
        print "C-Minor      |   %s  | %s" % (str(options["c_status"][lte_key]) if options["c_status"][lte_key] != "" else 0, str(options["c_status"][coop_key]))
    if options.get("baseline"):
        print "Baseline     |   %s  | %s" % (str(options["baseline"][lte_key]) if options["baseline"][lte_key] != "" else 0, str(options["baseline"][coop_key]))
