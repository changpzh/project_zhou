#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# #----------------------------------------------
#  Copyright: 2015~2025
#  Function :
#  Data: 2016/5/18 15:45
#  Author:changping.zhou@foxmail.com
# #----------------------------------------------
# #----------------------------------------------
'''

import urllib.request
import argparse
import os,re
import stat

build = {'details': '0',
         'baselines': '1',
         'tasks': '2',
         'build_conf': '3',
         'content': '4',
         'assign': '5',
         'release': '6',
         'download': '7'}
def FileWrite(FilePath, NewContent,Mode):
    if not os.path.isdir(os.path.dirname(FilePath)):
        os.makedirs(r'%s' % os.path.dirname(FilePath))  # create new dir path if none exist.

    try:
        f = open(FilePath,Mode) # open a file, create new one if not exist.
        f.write(NewContent + '\n')
    finally:
        f.close()

def reg_grep(data, patt):
    m = []
    m = patt.search(data)
    if m: return m.group(1)
    else: return ''

def argsParser():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-n', '--name', dest='packageName', help='This is baseline')
    parser.add_argument('-u', '--url', dest='wfturl', default='https://wft.inside.nsn.com/', help='This is WFT main page link')
    parser.add_argument('-a', '--api', dest='urlapi', default='ext/build_content/', help='This is WFT xml api')
    args = parser.parse_args()

    if not args.packageName:
        print('packageName is must be need')
        exit(1)
    else:
        packageName = args.packageName

    url_wft = args.wfturl
    url_api = args.urlapi

    return (packageName, url_wft, url_api)

def main():

    packageName, url_wft, url_api = argsParser()
    fragment = "#build=" + build['baselines']+"&tab_releases=0"
    url_xml = url_wft + url_api + packageName + fragment

    om_patt = re.compile(r'<baseline.+?title="BTSOM">(.*)</baseline>')
    cpri_patt = re.compile(r'<baseline.+?title="TDDCPRI">(.*)</baseline>')
    meta_patt = re.compile(r'/.+/(meta@\d+)')

    f = urllib.request.urlopen(url_xml)
    url_content = f.read().decode('utf-8') # f.read()文件流，相当于buffer，读一次便释放了
    om_pakg = reg_grep(url_content, om_patt)
    cpri_pakg = reg_grep(url_content, cpri_patt)

    if om_pakg:
        print('om_pakg='+om_pakg)
        f = urllib.request.urlopen(url_wft + url_api + om_pakg)
        om_meta = reg_grep(f.read().decode('utf-8'), meta_patt)
        print(om_meta)
    if cpri_pakg:
        print('cpri_pakg='+cpri_pakg)
        f = urllib.request.urlopen(url_wft + url_api + cpri_pakg + '#build='+  build['baselines'])
        cpri_content = f.read().decode('utf-8')
        cpri_meta = reg_grep(cpri_content, meta_patt)
        print(cpri_meta)

    # write the information to file, format as bellow.
    global ROOT_PATH
    ROOT_PATH = os.getcwd().replace("\\","/")

    BASELINE = "BASELINE=" + packageName
    TDDCPRI = "TDDCPRI=" + cpri_pakg + '.' + cpri_meta
    BTSOM = "BTSOM=" + om_pakg + '.' + om_meta

    sc_ver = [BASELINE, BTSOM, TDDCPRI]
    fileName = packageName + ".txt"
    FilePath = os.path.join(ROOT_PATH, fileName)

    nscs = range(len(sc_ver))
    for i in nscs:
        if i == 0:
            FileWrite(FilePath, sc_ver[i], 'w')
        else:
            FileWrite(FilePath, sc_ver[i], 'a+')

if __name__ == '__main__':
    main()