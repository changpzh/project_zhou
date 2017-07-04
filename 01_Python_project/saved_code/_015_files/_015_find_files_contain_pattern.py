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
def handle_input(argv, NamePattern = "error",f_Name_Patt = "txt"):
    """
    dealing with not correct input.
    :return:Path, NamePattern, f_Name_Patt
    """
    help_pattern = "--help"
    Path = None
    argv_len = len(argv)
    if argv_len <= 1: #No arguments.
        print("ERROR")
        print("\t[find_path] is None, Please type directory")
        print("\tSee help info. please use:'python %s --help'" % argv[0])
    elif argv_len == 2: #Don;t have NamePattern and f_Name_Patt arguments.
        if argv[1] == help_pattern:
            my_help_info(argv[0])
        else:
            if not path.isdir(argv[1]):
                print("[find_path]='%s' is not correct or cannot find the path of it" % argv[1])
                print("See help info. please use:'python %s --help'" % argv[0])
            else:
                Path = path.abspath(argv[1])

    elif argv_len == 3: # Don't have f_Name_Patt argument.
        Path = path.abspath(argv[1])
        NamePattern = argv[2]

    elif argv_len > 3:
        Path = path.abspath(argv[1])
        NamePattern = argv[2]
        f_Name_Patt = argv[3]

    return Path, NamePattern, f_Name_Patt

def create_name_as_time():
    """
    Function: create a file name as time pattern(%Y%m%d%H%M%S).
    :return:filename as time format.
    """
    #tt = time.localtime()
    #filename = time.strftime("%Y%m%d%H%M%S")    #output timestring like:20151125143433
    return time.strftime("%Y%m%d%H%M%S")

def save_parent_dir(Path, LogName, NamePattern, f_Name_Patt):
    """
    save parent directory to log file
    :return: None
    """
    f = open(path.join(Path ,LogName),"a") # 保存查询文件夹的起始位置到log
    f.write("*******************************************************************************\n"\
            "Find all external name is '%s' and files contains '%s' in the directory:\t%s\n"\
            "*******************************************************************************\n"\
            % (f_Name_Patt, NamePattern,Path))
    f.close()

def is_extname_contains_patt(File, Patt):
    """
    find file external name is Patt
    :param File:
    :param NamePattern:
    :return: True/False
    """
    Flag = False
    if File.endswith(Patt): #文件里面包含关键字
        Flag = True
    return Flag

def isfile_contains_patt(File, NamePattern):
    """
    find file whether contains NamePattern
    :param File:
    :param NamePattern:
    :return: True/False
    """
    Flag = False
    patt = re.compile(r'%s' % NamePattern)
    try:
        with open(File, "rb") as f:
            for eachLine in f:
                m = re.search(patt, format(eachLine).lower())
                if m is not None: #文件里面包含关键字
                    Flag = True
                    break
        f.close()
    except IOError,e:
        print("Could not open file:%s" % File, e)

    return Flag

def find_files(Path, LogName, NamePattern, f_NamePatt):
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
            if path.isfile(file) \
            and is_extname_contains_patt(file, f_NamePatt) \
            and isfile_contains_patt(file, NamePattern) \
            and path.split(file)[-1] != LogName:
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

def my_help_info(name_argv):
    print("\nHELP===============================================================\n"\
                  "Welcome to use this script %s\n"\
                  "\nFUNCTIONS\n"\
                  "\t1: Find external file name is [f_Name_Patt] and contains [NamePattern] in [find_path],\n"\
                  "\t2: Save the real path of file to SaveLog in [find_path]\n"\
                  "\nDESCRIPTION\n"\
                  "\t[find_path]:    Must need to type it, relative and absolute path are ok, like 'D:\Project\Python_project',\n"\
                  "\t\t\tany 'blank' in [find_path] is illegal!\n"\
                  "\t[NamePattern]:  Default is 'error', so you can leave it blank,\n"\
                  "\t\t\tignor case sensitive!\n"\
                  "\t[f_Name_Patt]:  Default file exteranl name is 'txt', so you can leave it blank,\n"\
                  "\t\t\tignor case sensitive!\n"\
                  "\nDEFAULT VALUE\n"\
                  "\t[NamePattern]=error\n"
                  "\t[f_Name_Patt]=txt\n"
                  "\nUSAGE\n"\
                  "\tYou must type cmd like below:\n"\
                  "\t  python %s [find_path] [NamePattern] [f_Name_Patt]\n"\
                  "\tor\n"\
                  "\t  python %s [find_path]\n"\
                  "\tor\n"\
                  "\t  python %s . [NamePattern]\n"\
                  "\tor\n"\
                  "\t  python %s . [NamePattern] [f_Name_Patt]\n"\
                  "================================================================HELP"\
                  % (name_argv, name_argv, name_argv, name_argv, name_argv))

def handle_blanks_inDir(Path, DirPattern):
    """
    replace blank in Directory to given pattern,
    :param Path:
    :return:
    """
    pass

def main():
    Path, NamePattern, f_NamePatt = handle_input(sys.argv)
    NamePattern = format(NamePattern).lower() # ignore case sensitive
    f_NamePatt = format(f_NamePatt).lower()   # ignore case sensitive
    if Path is not None:
        print("START TO FIND FILES=================================================================")
        print("To find file [f_Name_Patt]='%s' and [NamePatther]='%s' in [find_path]='%s'" % (f_NamePatt,NamePattern, Path))
        LogName = "LogSave_" + NamePattern + "_"+ create_name_as_time() + "." +"log"  #保存日志
        save_parent_dir(Path, LogName, NamePattern, f_NamePatt)
        Numbers = find_files(Path, LogName, NamePattern, f_NamePatt)
        print("To find file [f_Name_Patt]='%s' and [NamePatther]='%s' in [find_path]='%s'" % (f_NamePatt,NamePattern, Path))
        print("=================================================================END OF FIND FILES!")
        if Numbers == 0:
            print("\nNo file find")
        else:
            print("Total %d files find" % Numbers)
            print("You can see the details from saved log: %s" % os.path.join(Path,LogName))

if __name__ == '__main__':
    main()