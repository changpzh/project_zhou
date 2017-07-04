#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# #----------------------------------------------
#  Copyright: 2015~2025
#  Function :
#  Data: 2016/8/9 17:38
#  Author:changping.zhou@foxmail.com
# #----------------------------------------------
# #----------------------------------------------
'''
import os, subprocess

username = '/user:zcs1'
passwd = ''

cur_path = os.popen(u'echo %path%').read()
target_path = "C:\Python35\;C:\Python35\Scripts;"

n_path = target_path

cmd =u'setx Path "%s"' % target_path
os.system(cmd)

#subprocess.call(['runas', '/user:changpzh', 'your command'])
# proc = subprocess.Popen(['runas', username, cmd], stdin= subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# proc.stdin.write('ZCSzcs001')
# proc.communicate()
