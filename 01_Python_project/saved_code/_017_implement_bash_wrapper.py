# -*- coding:utf-8 -*-
#!/usr/bin/python
'''
##========================================================
# 1. implement a bash wrapper, so that I can call bash command like a class attribute
#
#     bash = BashWrapper()
#     bash.ping('10.69.69.124')
#     bash.ls('-l', '~')
#
# 2. what about a bash wrapper module, so that I can call bash command like a module import
#     from bashwrapper import ping
#     ping('10.69.69.124')
#     from bashwrapper import ls
#     ls('-l', '~')
##========================================================
'''
import subprocess,sys

# class BashWrapper_1:
#     __metaclass__ = type #确保使用新式类.
#     def __getattr__(self,attr):
#         def _exec_bash(*args):
#             print("=======start===========")
#             print(subprocess.check_output([attr] + list(args), stderr=subprocess.STDOUT))
#             print([attr])
#             print('list=%s' % list(args))
#             print("attr+list=%s" % ([attr] + list(args)))
#             print(attr)
#             print("========end=============")
#         return _exec_bash
#
# bash = BashWrapper_1()
# # print('bash_ls_result=%s' % bash.ls("-l","/"))
# #print('bash_ping_result=%s' % bash.ping("10.69.65.57"))

#2.
class BashWrapper_2(object):
    __metaclass__ = type #确保使用新式类.
    def __init__(self, wrapped):
        self.wrapped  = wrapped

    def __getattr__(self,name):
        print hasattr(self.wrapped, name)
        if hasattr(self.wrapped, name):
            print(getattr(self.wrapped, name))
            return getattr(self.wrapped, name)

        def _exec_bash(*args):
            return subprocess.check_output([attr] + list(args))
        return _exec_bash

sys.modules[__name__] = BashWrapper_2(sys.modules[__name__])

# from BashWrapper_2 import ls
# ls('-l', '/')