#!/usr/bin/env python
# encoding: utf-8
'''
# #----------------------------------------------------------------------
#  Copyright: 2015~2025
#  module:_017_Fibonacci_sequence.py
#  Function :求给定num的Fibonacci sequence，并计算一共花的时间。
#  Data: 2016/3/30 15:17
#  Author:changpzh
#  Email:changping.zhou@foxmail.com
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
'''
import time
import unittest

def memorize(fn):
    Return = {}
    def decorator(*args):
        if args not in Return:
            Return[args] = fn(*args)
            print("number of %s is: %s" % (args, Return[args]))
        return Return[args]
    return decorator

@memorize
def fib(n):
    if n == 0: return 0
    elif n == 1: return 1
    else:
        return fib(n-2) + fib(n-1) # 一定要n-2在前面，不然先返回fib(1)的值，再返回fib(0)


def timer(fn):
    def decorator(*args, **kwargs):
        start = time.time()
        Return = fn(*args, **kwargs)
        print('Total cost %s seconds' % (time.time() - start))
        return Return
    return decorator

@timer
def cal(n):
    return fib(n)

# class MyTestCase(unittest.TestCase):
#     def test_zero(self):
#         self.assertEqual(cal(0), 0)
#
#     def test_one(self):
#         self.assertEqual(cal(1), 1)
#
#     def test_two(self):
#         self.assertEqual(cal(2), 1)
#
#     def test_Mtwo(self):
#         self.assertEqual(cal(10), 55)


if __name__ == '__main__':
    # unittest.main()
    print(cal(10))
