# -*- coding: utf-8 -*-
# #----------------------------------------------------------------------
# module:
#  Function : auto install file in directory
#  Data: 2015-11-20
#  Author:changpzh
#  Email:
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
import os
import glob

def File_Installation(f_path):
    '''
    #install all pakages in the f_path
    #>>>f_path:"D:\Project_Zhou\01_Python_project\test_folder"
    '''
    FileNames=os.listdir(f_path)  # dynamic get the package name.
    print("FileNames=%s" % FileNames)
    for pck in FileNames:
        pkg_path = glob.glob(os.path.join(f_path,'%s' % pck))[0]
        print(pkg_path)
        cmd = "%s" % pkg_path
        print("Install file '%s' in the directiory '%s'" % (pck,f_path))
        #os.system(cmd) # this will not take effect if file path contain spaces
        os.startfile(cmd) # this can works when spaces in file path.

def get_path():
    '''
    #get the current *.py path.
    #>>>print("os.path.dirname=%s" %os.path.dirname(__file__))
    #os.path.dirname=D:/Project_Zhou/01_Python_project
    '''
    path = os.path.abspath(os.getcwd())
    # print("abspath=%s" % path)
    print("os.path.dirname=%s" %os.path.dirname(path)) # get the dir as: "D:/Project_Zhou/01_Python_project"
    return path

if __name__ == "__main__":
    pkgs_path = os.path.join(get_path(), 'test folder')
    print(pkgs_path)
    # FileNames=os.listdir(pkgs)  # dynamic get the package name.
    # print("FileNames=%s" % FileNames)
    File_Installation(pkgs_path)

    #update_lib_path()
    



