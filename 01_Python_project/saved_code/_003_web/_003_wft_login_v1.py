#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# #----------------------------------------------
#  Copyright: 2015~2025
#  Function :
#  Data: 2016/5/20 10:20
#  Author:changping.zhou@foxmail.com
# #----------------------------------------------
# #----------------------------------------------
'''
import urllib.request

import os
def main():
    url_path = "https://wam.inside.nsn.com/siteminderagent/forms/login.fcc"
    FilePath = "D:\\Project_Zhou\\test folder\\test.html"
    # Create an OpenerDirector with support for Basic HTTP Authentication..
    #
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