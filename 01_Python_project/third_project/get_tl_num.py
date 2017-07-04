#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# #----------------------------------------------
#  Copyright: 2015~2025
#  Function : auto get QT1 testline number from testline.txt
#  Data: 2016/5/9 16:01
#  Author:changping.zhou@foxmail.com
# #----------------------------------------------
# #----------------------------------------------
'''

import argparse

def get_tl_num(envConfig):
    testline_number = 0
    QT1_patt = "TRUNK|1|"
    f = open(envConfig,'r')
    for line in f.readlines():
        line = line.strip()
        if not line.startswith('#') and line != '':
            if QT1_patt in line:
                testline_number += 1
    f.close()
    return testline_number

def wirte_tlnum2f(tl_number, tl_num_file):
    try:
        f = open(tl_num_file,"w")
        f.write(str(tl_number))
        f.close()
    except:
        print("write testline number in file failed!")

def argsParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--TLconfig',action='store', dest='testLine', default='testline.txt' ,help='This is test line file')
    parser.add_argument('-f', '--Numfile',action='store', dest='numFile', default='num_testline' ,help='This is test line number file')
    parser.add_argument('-d', '--directory', action='store', dest='resultDir', default='D:\\Project_Zhou\\01_Python_project\\third_project', help='This is test line file parent')
    # parser.add_argument('-d', '--directory', action='store', dest='resultDir', default='/build/home/citdlte/CPD/QTResult/', help='This is test line file parent')
    args = parser.parse_args()

    testline_file = args.resultDir +'/'+ args.testLine
    testline_num_file = args.resultDir +'/' + args.numFile
    return testline_file, testline_num_file

def main():
    tl_file, tl_num_file = argsParser()
    tl_num = get_tl_num(tl_file)
    wirte_tlnum2f(tl_num, tl_num_file)

if __name__ == '__main__':
    main()