#!/usr/bin/env python
#encoding: utf-8
#模块文档说明
"""
##=============================================================
# Copyright:
# Function:change latest modified file name in given path
# Date:2015-11-22
# Author:changping.zhou@foxmail.com
##==============================================================
"""

#模块导入
import os, time

#函数模块
def CreateNameAsTime():
    '''
    # Function: create a file name as time pattern(%Y%m%d%H%M%S).
    '''
    #tt = time.localtime()
    #filename = time.strftime("%Y%m%d%H%M%S")    #output timestring like:20151125143433
    return time.strftime("%Y%m%d%H%M%S")

def ChangeName(oldfile,newfname,logname):
    '''
    # Function: change oldfnmae to newfname, and save it to log.
    # Return: [NewFile path, LogFile path]
    '''
    if not os.path.isfile(oldfile):
        print("(文件)路径打开失败")
        return False
    else:
        lists = os.path.split(oldfile) #分割出目录与文件的二元数组
        file = lists[1].split('.') #分割出文件与文件扩展名
        file_ext = file[-1] #取出后缀名(列表切片操作)
        #img_ext = ['bmp','dav','mp4']
        #if file_ext in img_ext:
        newfile = os.path.join(lists[0],(newfname+'.'+file_ext))
        print(newfile)
        if not os.path.isfile(newfile):
            os.rename(oldfile,lists[0]+'/'+newfname+'.'+file_ext)
            #save change log to saveLog
            log_file = os.path.join(lists[0],logname)
            f = open(log_file,"w")
            f.write("%s=======>%s\n" % (os.path.basename(oldfile),os.path.basename(newfile)))
            f.close()
            return [newfile,log_file]
        else:
            print("new file '%s'already exist.\nplease rename new filename" % os.path.join(lists[0],newfile))
            return False

def GetLaModFile(path):
    '''
    # Function: get the latest modified file
    '''

    if os.path.isdir(path):
        files = os.listdir(path)
        filelist = {}
        for file in files:
            filepath = os.path.join(path,file)
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
        latestmodifiedfile = os.path.join(path,f_sort[0][0])
        return latestmodifiedfile

    else:
        print("the given '%s' path cannot find!" % path)
        return False

#主程序
def test():
    #os.path.abspath(os.path.dirname(__file__) #获取当前file的绝对路径 also can use os.getcwd()。
    #path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"test_folder")
    path = os.path.join(os.getcwd(),"test_folder")
    newfname = 'NewFiles' #需要重命名的文件名
    logname = "logSave_" + CreateNameAsTime() + ".txt"  #保存更名内容的日志

    latestmfile = GetLaModFile(path)
    if latestmfile:
        filedata = ChangeName(latestmfile,newfname,logname)
        print(filedata)

if __name__ == '__main__':
    test()