#!/usr/bin/env python
# encoding: utf-8
'''
# #----------------------------------------------------------------------
#  Copyright: 2015~2025
#  module:Newfile.py
#  Function :
#  Data: 2016/4/21 14:23
#  Author:changpzh
#  Email:changping.zhou@foxmail.com
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
'''

import os,datetime,time
result_dir = 'D:\\test_zhou'
lists=os.listdir(result_dir)
#按照getmtime进行排序，如果是文件夹，就为0值，是文件，就获取getmtime，最新的文件，值最大，再反序排列。
lists.sort(key=lambda fn: os.path.getmtime(result_dir+"\\"+fn) if not os.path.isdir(result_dir+"\\"+fn) else 0, reverse=True)
print ('最新的文件为： '+lists[0])
file = os.path.join(result_dir,lists[0])
print file

