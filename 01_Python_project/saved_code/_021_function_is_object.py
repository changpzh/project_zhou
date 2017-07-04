#021_function_is_object
# -*- coding: utf-8 -*-
__author__ = 'changpzh'
'''
##=============================
# 1:语法糖syntax sugar
# 2:wrapper, 封装
#
#
#
##=============================
'''
import logging

logging.basicConfig(level=logging.INFO)

def checkParams(fn):
    def wrapper(a, b):
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return fn(a, b)

        logging.warning("variable 'a' and 'b' cannot be added")
        return
    return wrapper

@checkParams
def add(a, b):
    return a + b

if __name__ == '__main__':
    # add = checkParams(add)
    print(add(4,'hello word'))
    print(add(4, 8))
    # print(add(4,8.9))

## 如果有人觉得add = checkParams(add)这样的写法未免太过麻烦，
## 于是python提供了一种更优雅的写法，被称为语法糖syntax sugar
# @checkParams
# def add(a, b):
#     return a + b

# 这只是一种写法上的优化，解释器仍然会将它转化为add = checkParams(add)来执行。
