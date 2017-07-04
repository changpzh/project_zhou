#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# #----------------------------------------------
#  Copyright: 2015~2025
#  Function :
#  Data: 2016/5/11 17:14
#  Author:changping.zhou@foxmail.com
# #----------------------------------------------
# #----------------------------------------------
'''
from random import randint
from time import sleep
from Queue import Queue
from myThread import MyThread

def writeQ(queue):
    print('producing object for Q...')
    queue.put('xxx',1)
    print('size now', queue.qsize())

def readQ(queue):
    val = queue.get(1)
    print('consumed object from Q... size now', queue.qsize())

def writer(queue, loops):
    for i in range(loops):
        writeQ(queue)
        sleep(randint(1,4))

def reader(queue, loops):
    for i in range(loops):
        readQ(queue)
        sleep(randint(2,5))

funcs = [writer, reader]
nfuncs = range(len(funcs))

def main():
    nloops = randint(2, 5)
    q = Queue(32)

    threads = []
    for i in nfuncs:
        t = MyThread(funcs[i], (q, nloops), funcs[i].__name__) # funcs 必须是函数名才有name属性

    for i in nfuncs:
        threads[i].start()

    for i in nfuncs:
        threads[i].join()

    print("all done")

if __name__ == '__main__':
    main()



def func():
    pass


class test():
    def __init__(self):
        pass


def main():
    pass


if __name__ == '__main__':
    main()