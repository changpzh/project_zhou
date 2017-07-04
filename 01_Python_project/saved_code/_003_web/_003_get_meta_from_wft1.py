#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# #----------------------------------------------
#  Copyright: 2015~2025
#  Function :
#  Data: 2016/5/18 10:26
#  Author:changping.zhou@foxmail.com
# #----------------------------------------------
# #----------------------------------------------
'''

import urllib.request

import os
import stat

def open_url(url_path):
    """
    open URL, return content
    """
    filehandle = urllib.request.urlopen(url_path)
    return filehandle.readline()

def FileWrite(FilePath, NewContent):
    """
    write NewContent to FilePath file
    """
    if not os.path.isdir(os.path.dirname(FilePath)):
        os.makedirs(r'%s' % os.path.dirname(FilePath))  # create new dir path if none exist.

    try:
        f = open(FilePath, 'w') # open a file, create new one if not exist.
        f.write(NewContent + '\n')
    finally:
        f.close()

def FileOpen(FilePath):
    """
    open CurrentPath fle
    """
    if not os.path.isfile(FilePath):
        print("File %s does not exists" % (FilePath))
        return []
    else:
        try:
            f = open(FilePath, 'r')
            # **get a content of file**
            return f.readline()
        finally:
            f.close()

def main():
    url_path = "https://wft.inside.nsn.com/ALL/builds/TL16A_OM_0000_COMMON_366513_000000#build=0"
    FilePath = "D:\\Project_Zhou\\test folder\\test.html"
    # Create an OpenerDirector with support for Basic HTTP Authentication..
    # 由于WFT是SSO认证，所以用basic认证是不行的。需要另外想办法实现.
    auth_handler = urllib.request.HTTPBasicAuthHandler()
    auth_handler.add_password(realm=None,
                              uri=url_path,
                              user='changpzh',
                              passwd='ZCSzcs016')

    opener = urllib.request.build_opener(auth_handler)

    # ...and install it globally so it can be used with urlopen.
    urllib.request.install_opener(opener)
    #format url_content to str, so that can FileWrite.
    url_content = opener.open(url_path).read().decode('utf8')
    print(url_content)
    FileWrite(FilePath, url_content)

if __name__ == '__main__':
    main()