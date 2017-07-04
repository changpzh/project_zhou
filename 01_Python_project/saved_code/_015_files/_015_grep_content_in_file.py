__author__ = 'changpzh'
'''
this script used for find out the name you want in file
'''
import os, sys

'NewRelPath = "\\\\10.68.143.208\\rl25\\NewReleaseInfo_RL25.ini"'
CurrentPath = "D:\\Python_project\\test_file\\NewReleaseInfo_RL25.ini"


# *******************this script get all BTS version in files**************
def GetBtsSWRelease():
    if not os.path.isfile(CurrentPath):
        print "File %s does not exists" % (CurrentPath)
        return []
    else:
        try:
            f = open(CurrentPath, 'r')
            # **get a list of file content**
            return [item.split() for item in f.readlines()]
            '''
            # *********this script get all BTS version in files**
            return [item.split()[0] for item in f.readlines()]
            # *********this script get all BTSSM version in files**
            return [item.split()[-1] for item in f.readlines()]
            '''
        finally:
            f.close()

Swverion=GetBtsSWRelease()
print Swverion
print('len= %s lines' % len(Swverion))
print(os.path.isfile(CurrentPath))

# **clone a list of orignal list**
def Clonelist(list):
    temp = list[:]
    return temp

print(Clonelist(Swverion))