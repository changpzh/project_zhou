#!/usr/bin/env python
# encoding: utf-8
'''
# #----------------------------------------------------------------------
#  Copyright: 2015~2025
#  module:_017_Wrapper.py
#  Function :
#  Data: 2016/3/29 16:25
#  Author:changpzh
#  Email:changping.zhou@foxmail.com
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
'''
import time
def timer(fn):
    def wrapper(*args,**kwargs):
        start = time.time()
        print(args)
        print(kwargs)
        fn(*args,**kwargs)
        print('cost: %s' % (time.time() - start))
    return wrapper
    # return

@timer
def mul(row,column):
    for i in xrange(row):
        for j in xrange(column):
            print(i,j,i*j)

if __name__ == '__main__':
    #mul = timer(mul)
    mul(10,100)

## example1 ---------------------------------------------------------------
# import logging
#
# logging.basicConfig(level = logging.INFO)
#
# def checkParams(fn):
#     def wrapper(a,b):
#         if isinstance(a,(int,float)) and isinstance(b,(int,float)):
#             return fn(a,b)
#
#         logging.warning("variable 'a' and 'b' cannot be added")
#         return
#     return wrapper
#
# @checkParams
# def add(a,b):
#     return a + b
#
# if __name__ == '__main__':
#     add(4,'sfsdsa')
