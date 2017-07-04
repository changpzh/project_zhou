#!/usr/bin/env python
# encoding: utf-8
'''
# #----------------------------------------------------------------------
#  Copyright: 2015~2025
#  module:_015_get_latest_changed_file.py
#  Function :
#  Data: 2016/4/21 15:10
#  Author:changpzh
#  Email:changping.zhou@foxmail.com
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
'''
import os,time


TIMEFORMAT="%Y%m%d%H%M%S"

def get_latestMfile1(filePath):
    '''
    :return Latest modified file in given path
    '''
    if not os.path.isdir(filePath):
        print("your given path '%s' is not exist" % filePath)
        return None
    else:
        #按修改时间排序
        files = os.listdir(filePath)
        files.sort(key=lambda fn: os.path.getmtime(os.path.join(filePath, fn)) if not os.path.isdir(os.path.join(filePath, fn)) else 0)
        return os.path.join(filePath, files[-1])

def get_latestMfile2(filePath):
    if not os.path.isdir(filePath):
        print("your given path '%s' is not exist" % filePath)
        return None
    else:
        #按修改时间排序
        files = os.listdir(filePath)
        #files.sort(key=lambda fn: os.path.getmtime(os.path.join(filePath, fn)) if not os.path.isdir(os.path.join(filePath, fn)) else 0)
        filelist = {}
        for file in files:
            filepath = os.path.join(filePath,file)
            if os.path.isfile(filepath):
                filelist[file] = os.path.getmtime(filepath) # 创建文件字典列表key=文件名， value=时间

                '''
                # tt1 = os.path.getmtime(filename) # Return the last modification time of a file, reported by os.stat()
                # tt2 = os.path.getatime(filename) # Return the last access time of a file, reported by os.stat().
                # tt3 = os.path.getctime(filename) # Return the metadata change time of a file, reported by os.stat().
                {'NewFile.txt': 1464160830.417339, 'NewFile.xml': 1463738066.1433022, 'test.html': 1463738066.1428022}
                '''
        #Return a new list containing all items from the iterable in descending order.
        # filelist[1]：表示按照vlue排序;如果是filelist[0],则表示按照key进行排序, reverse=True 表示反序
        f_sort = sorted(filelist.items(), key=lambda filelist : filelist[1], reverse=True)
        latestmodifiedfile = os.path.join(filePath,f_sort[0][0])
        return latestmodifiedfile

def main():
    latestMfile1 = get_latestMfile1(os.getcwd())
    print("the lastest modified file is: " + latestMfile1)

    latestMfile2 = get_latestMfile2(os.getcwd())
    print("最新文件修改是: " + latestMfile2)

# file_dir = os.getcwd()
# files = os.listdir(file_dir)
# files.sort(key=lambda fn: os.path.getmtime(os.path.join(filePath, fn)) if not os.path.isdir(os.path.join(filePath, fn)) else 0)
# print ('最新的文件为： '+files[-1])
# file = os.path.join(file_dir,files[-1])
# print(file)
if __name__ == '__main__':
    main()