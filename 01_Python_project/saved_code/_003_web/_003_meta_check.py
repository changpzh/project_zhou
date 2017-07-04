#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# #----------------------------------------------
#  Copyright: 2015~2025
#  Function :
#  Data: 2016/5/30 10:00
#  Author:changping.zhou@foxmail.com
# #----------------------------------------------
# #----------------------------------------------
'''

import urllib.request
import argparse
import os,re
import stat
def Func_ReadFile(fullPathFile, ReadMode):
    if not os.path.isfile(fullPathFile):
        print("File %s does not exists" % (fullPathFile))
        return []
    try:
        with open(fullPathFile, ReadMode) as f:
            return f.readlines()
    except IOError:
        print("Open %s failed!" % (fullPathFile))
        return []


def FileRead(fullPathFile,ReadMode):
    if not os.path.isfile(fullPathFile):
        print("File %s does not exists" % (fullPathFile))
        return []
    try:
        with open(fullPathFile, ReadMode) as f:
            return f.readlines()
    except IOError:
        print("Open %s failed!" % (fullPathFile))
        return []

def reg_grep(data, patt):
    m = []
    m = patt.search(data)
    if m: return m.group(1)
    else: return ''

def argsParser():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-n', '--name', dest='packageName', help='This is baseline')
    args = parser.parse_args()

    if not args.packageName:
        print('packageName is must be need')
        exit(1)
    else:
        packageName = args.packageName

    return packageName

def main():

    packageName = argsParser()
    # write the information to file, format as bellow.
    global ROOT_PATH
    ROOT_PATH = os.getcwd().replace("\\","/")
    fileName = packageName + ".txt"
    FilePath = os.path.join(ROOT_PATH, fileName)

    contents = FileRead(FilePath,'r')
    if (contents[1].split('@')[-1]) == (contents[2].split('@')[-1]):
        print("OAM and TDDCPRI's meta aligned")
        exit(0)
    else:
        print("OAM and TDDCPRI's meta not aligned")
        exit(1)

if __name__ == '__main__':
    main()