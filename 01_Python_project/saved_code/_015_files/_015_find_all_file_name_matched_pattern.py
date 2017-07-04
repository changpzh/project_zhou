#!/usr/bin/python
# -*- coding: utf-8 -*-
# #----------------------------------------------------------------------
# module:
#  Function :
#   1: find files which match given pattern in given path.
#   2: save found file path to LogSave file.
#  Description: you can start this script by "python this_script_name.py log [Pattern]"
#               then it will find all files matched pattern.
#  Data: 2016-01-21
#  Author:changpzh
#  Email:changping.zhou@foxmail.com
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
import os, sys, time
from os import path

def save_parent_dir(Path, LogName, NamePattern):
    """
    save parent directory to log file
    :return: None
    """
    f = open(path.join(Path ,LogName),"a") # 保存查询文件夹的起始位置到log
    f.write("*******************************************************************************\n"\
            "Find all files which name match '%s' in the directory:\t%s\n"\
            "*******************************************************************************\n"\
            % (NamePattern,Path))
    f.close()

def CreateNameAsTime():
    """
    Function: create a file name as time pattern(%Y%m%d%H%M%S).
    :return:filename as time format.
    """
    #tt = time.localtime()
    #filename = time.strftime("%Y%m%d%H%M%S")    #output timestring like:20151125143433
    return time.strftime("%Y%m%d%H%M%S")

def find_files(Path, LogName, NamePattern):
    """
    find all files from Path by give NamePattern
    :param Path:
    :param LogName:
    :param NewNamePattern:
    :return: None
    """
    Flag = 0
    for parent, dirnames, files in os.walk(Path): #遍历Path下面所有的文件
        for file in files:
            file = os.path.join(parent,file)
            if os.path.isfile(file) and file.endswith(NamePattern):
                Flag += 1
                print("%-4d: find \t%s" % (Flag, file))
                file_abs = path.abspath(file)
                save_log(Path,LogName,file_abs,Flag)
    return Flag

def save_log(Path,LogName,FindFile,Flag):
    """
    save change log to saveLog
    :return:
    """
    log_file = os.path.join(Path ,LogName)
    f = open(log_file,"a")
    f.write("%-4d: find file: \t%s\n" % (Flag,FindFile))
    f.close()
    #return Path + '/' + log_file

def main():
    # Path = os.path.split(os.path.realpath(sys.argv[0]))[0] # equal to below Path
    Path = os.path.dirname(os.path.realpath(sys.argv[0]))
    # Path = "D:\\Project_Zhou\\test_folder\\"
    LogName = "LogSave_" + CreateNameAsTime() + "." +"log"  #保存日志
    #(os.path.basename(sys.argv[0]))

    print("START TO FIND FILE===================")
    if len(sys.argv) > 1:
        NamePattern = sys.argv[1]

    else:
        NamePattern = "txt"
    save_parent_dir(Path,LogName, NamePattern)
    Flag = find_files(Path, LogName, NamePattern)
    print("====================END OF FIND FILE!")
    if Flag == 0:
        print("\nNo file Find")
    else:
        print("\nTotal %d files Find" % Flag)
        print("You can find the details from saved log: %s\n" % os.path.join(Path,LogName))

if __name__ == '__main__':
    main()