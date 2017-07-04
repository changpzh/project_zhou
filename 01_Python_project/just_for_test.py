#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep,ctime
import threading

loops = [4, 3, 5]

class ThreadFunc(object):

    def __init__(self,func, args, name=''):
        self.name = name
        self.func = func
        self.args = args
        print('name=',name)
        print('func=',func)
        print('args=',args)

    def __call__(self):
        self.res = self.func(*self.args)

def loop(nloop, nsec):
    print('start loop', nloop, 'at:', ctime())
    sleep(nsec)
    print('end loop', nloop, 'at:', ctime())


def main():
    print('starting at:', ctime());
    threads = []
    nloops = range(len(loops))

    for i in nloops: # create all threads
        print('i=',i)
        t = threading.Thread(target=ThreadFunc(loop, (i, loops[i]), loop.__name__))
        threads.append(t)

    for i in nloops: # start all threads
        threads[i].start()

    for i in nloops: # wait for completion
        threads[i].join()

    print('all done at:', ctime())

if __name__ == '__main__':
    main()