#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #----------------------------------------------------------------------
# module:
#  Function :add patter name before old name.
#  Data: 2016-01-21
#  Author:changpzh
#  Email:changping.zhou@foxmail.com
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
import os, sys, time

NOTCHANGEFILE = os.path.basename(sys.argv[0]) # 本py文件不用更名

def CreateNameAsTime():
    '''
    # Function: create a file name as time pattern(%Y%m%d%H%M%S).
    # Return：filename as time format.
    # Varible description：None
    '''
    #tt = time.localtime()
    #filename = time.strftime("%Y%m%d%H%M%S")    #output timestring like:20151125143433
    return time.strftime("%Y%m%d%H%M%S")

def file_name_change(Path, LogName, NewNamePattern='_'):
    '''
    change file name by give pattern
    :param Path:
    :param NamePattern:
    :return: None
    '''
    files = os.listdir(Path)
    Flag = 0
    for file in files:
        if not os.path.isdir(file) and not file.startswith(NewNamePattern) and file != NOTCHANGEFILE:
            #NewFile = "00_" + f, LogNameile.split("_")[-1]
            NewFile = NewNamePattern + file
            #os.rename(os.path.join(Path,file), os.path.join(Path, NewFile))
            Flag += 1
            print("%d: change %s ----> %s" % (Flag, file, NewFile))
            save_log(Path,LogName,file,NewFile,Flag)
    return Flag

def save_log(Path,LogName,OldFile,NewFile,Flag):
    #save change log to saveLog
    log_file = os.path.join(Path ,LogName)
    f = open(log_file,"a")
    f.write("%d: ../%s\t====================>\t../%s\n" % (Flag,OldFile,NewFile))
    f.close()

def main():
    # Path = os.path.split(os.path.realpath(sys.argv[0]))[0] # equal to below Path
    Path = os.path.dirname(os.path.realpath(sys.argv[0]))
    LogName = "LogSave_" + CreateNameAsTime() + ".txt"  #保存更名内容的日志
    #(os.path.basename(sys.argv[0]))
    print("START TO CHANGE NAME========================")
    if len(sys.argv) > 1:
        NewNamePattern = sys.argv[1]
        Flag = file_name_change(Path, LogName, NewNamePattern)
    else:
        Flag = file_name_change(Path, LogName)
    print("====================END OF CHANGE FILE NAME!")

    if Flag == 0:
        print("\nNo file changed")
    else:
        print("\nTotal %d files changed" % Flag)

if __name__ == '__main__':
    main()