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

def get_comparison_status(title, value1, value2):
    if (value1 == ''):
        value1 = 0    
    if (str(value1) == str(value2)):
        print title, '| ', 'ltemetrics: ', str(value1), ' | ', 'coop: ', str(value2)
        return "PASS"
    else:
        print title, '| ', 'ltemetrics: ', str(value1), ' | ', 'coop: ', str(value2)
        return "FAIL"
    

