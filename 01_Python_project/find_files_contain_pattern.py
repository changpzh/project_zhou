#!/usr/bin/python
# -*- coding: utf-8 -*-
# #----------------------------------------------------------------------
# Name: find_files_contain_pattern.py
#  Function :
#   1: find all files if contains Pattern(ignore case sensitivity) in file
#   2: save found file path to LogSave file.
#  Description: you can start this script by \
#  "python find_files_contain_pattern.py [find_path] [Pattern]"
#  then it will find all files matched pattern.
#  [find_path] = "D:\root\location"; [Pattern]= "error"
#  Data: 2016-01-26
#  Author:changpzh
#  Email:changping.zhou@foxmail.com
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
import os, sys, time
import re
from os import path

def save_parent_dir(Path, LogName, NamePattern):
    """
    save parent directory to log file
    :return: None
    """
    f = open(path.join(Path ,LogName),"a") # 保存查询文件夹的起始位置到log
    f.write("*******************************************************************************\n"\
            "Find all files contains '%s' in the directory:\t%s\n"\
            "*******************************************************************************\n"\
            % (NamePattern,Path))
    f.close()

def create_name_as_time():
    """
    Function: create a file name as time pattern(%Y%m%d%H%M%S).
    :return:filename as time format.
    """
    #tt = time.localtime()
    #filename = time.strftime("%Y%m%d%H%M%S")    #output timestring like:20151125143433
    return time.strftime("%Y%m%d%H%M%S")

def iscontain_pattern(File, NamePattern):
    """
    find file whether contains NamePattern
    :param File:
    :param NamePattern:
    :return: True/False
    """
    Flag = False
    patt = re.compile(r'%s' % NamePattern)
    with open(File, "rb") as f:
        for eachLine in f:
            m = re.search(patt, format(eachLine).lower())
            if m is not None: #文件里面包含关键字
                Flag = True
                break
    f.close()
    return Flag

def find_files(Path, LogName, NamePattern):
    """
    find all files from Path by give NamePattern
    :param Path:
    :param LogName:
    :param NewNamePattern:
    :return: None
    """
    Numbers = 0
    for parent, dirnames, files in os.walk(Path): #遍历Path下面所有的文件
        for file in files:
            file = path.join(parent,file)
            if path.isfile(file) and iscontain_pattern(file, NamePattern):
                Numbers += 1
                print("%-4d: find \t%s" % (Numbers, file))
                file_abs = path.abspath(file)
                save_log(Path,LogName,file_abs,Numbers)
    return Numbers

def save_log(Path,LogName,FindFile,Numbers):
    """
    save change log to saveLog
    :return:
    """
    log_file = path.join(Path ,LogName)
    f = open(log_file,"a")
    f.write("%-4d: find file: \t%s\n" % (Numbers,FindFile))
    f.close()

def main():
    Path = os.path.realpath(sys.argv[1])
    print("find files from path=%s" % Path)
    if not path.isdir(Path):
        print("Cannot find your typed directory:%s\nPlease double check your input!" % Path)
        print("\nYou should type like:python %s [find_path] [Pattern]" % sys.argv[0])
    else:
        print("START TO FIND FILES==================")
        if len(sys.argv) <= 2:
            NamePattern = 'error' # default is "error"
        else:
            NamePattern = format(sys.argv[2]).lower()
        LogName = "LogSave_" + NamePattern + "_"+ create_name_as_time() + "." +"log"  #保存日志
        save_parent_dir(Path, LogName, NamePattern)
        Numbers = find_files(Path, LogName, NamePattern)
        print("====================END OF FIND FILES!")

        if Numbers == 0:
            print("\nNo file find")
        else:
            print("\nTotal %d files find" % Numbers)
            print("\nYou can see the details from saved log: %s" % os.path.join(Path,LogName))

if __name__ == '__main__':
    main()