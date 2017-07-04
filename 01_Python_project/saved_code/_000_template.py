# -*- coding:utf-8 -*-
#!/usr/bin/env python

#模块文档说明
"this is a test module"

#模块导入
import os

#全局变量
debug = True

#类定义区域（若有）
class Fooclass(object):
    "Foo class"
    pass

#函数定义
def test():
    "test function"
    foo = Fooclass()

    if debug:
        print("run test()")

#主程序
if __name__ == '__main__':
    test()