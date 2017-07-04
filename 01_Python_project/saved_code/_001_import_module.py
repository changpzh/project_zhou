# -*- coding: utf-8 -*-

'''
This script teach us how to import another module file in different directory
##=============================
# 如果模块名会变化，怎么import
#可以变量化，
# module_name = "give_name"
# m = __import__(module_name)
#
# 注意import 之后 如果原模块有改动，要用reload（module.py）
'''
# ***************import zone start
import sys, os
sys.path.append(os.path.join(os.getcwd(),"ENV_file"))
print(sys.path)
module_name = "EnvVar1"
m = __import__(module_name)
#from EnvVar1 import *
# ***************import zone end

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

# ***************Print EnvVar infomation
print("VarEnvPath=%s" % m.VarEnvPathGet())
print(m.LOCAL_VAR['a1'])
print(m.LOCAL_VAR['b2'])




