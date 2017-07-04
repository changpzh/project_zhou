
# xrange ---range的差异
#
# # cache wrapper
# def cache(func):
#     cached = {}
#     def _f(*args):
#         if args not in cached:
#             result = func(*args)
#             cached[args] = result
#         else:
#             print 'cache hint!'
#         return cached[args]
#     return _f
#
# ###考虑到缓存。装饰器
# @cache
# def sum_(*args):
#     return sum(args)
#
# print sum_(1,2,3)
# print sum_(1,2,3)
# #=============================================================
#
#Decorator
# cache wrapper for function，时间大于给定时间，超时，缓存释放
import time

def cache(timeout):
    def _wrapped(func):
        cached_start = {}
        cached = {}
        def _f(*args):
            if args not in cached or ((time.time() - cached_start[args]) > timeout):
                result = func(*args)
                cached[args] = result
                cached_start[args] = time.time()
            else:
                print 'cache hint!'
            return cached[args]
        return _f
    return _wrapped


#----
#@cache(2)
def sum_(*nums):
    return sum(nums)
f= cache(2)(sum_)
print(f(1,2,3))
print(f(1,2,3))
#----和下面一样的效果，

@cache(2)
def sum_(*nums):
    return sum(nums)

print sum_(1,2,3)
print sum_(1,2,3)
from time import sleep
sleep(2)
print sum_(1,2,3)
# ##==========================================

# # functools.partial
# import functools
#
# def echo(name, city, country):
#     print '%s live in %s, %s' % (name, city, country)
#
# f = functools.partial(echo, city='Hangzhou', country='China')
#
# f('Tom and Jerry')


##===============================================================

#
# ##==============================
# unit testing
#
# if --> 1
# while ---> 多
# for ----> 多
#
# <<how google tests software>>
#
# ###+============iterator and generator================
# iterator----xrange
# xrange()
# fp = open('acess.log')
# fp.next() # next line,比用readlines更好，内存考虑，或者用xreadelines
# fp.close()
#
# generator----yield
# def series(length):
#     for e in xrange(length):
#         yield e ** 2 ## cannot use it with return at same time.but can use multiple times yield in one fuction.

##==========================================================
def fibonacci_new(n):
    a, b = 1, 1
    yield a
    yield b
    while True:
        a,b = b,b+a
        yield b

==================
多线程，多进程，线程进程池，
# fetch content size from a series of web sites
import urllib

urls = ['http://hztdltev01.china.nsn-net.net',
        'http://10.56.117.81/coci/',
        'http://coop.china.nsn-net.net']

for url in urls:
    print len(urllib.urlopen(url, proxies={}).read())


# introduce thread
from threading import Thread
import urllib

urls = ['http://hztdltev01.china.nsn-net.net',
        'http://10.56.117.81/coci/',
        'http://coop.china.nsn-net.net']

class UrlFetchThread(Thread):
    def __init__(self, url, *args):
        super(UrlFetchThread, self).__init__(*args)
        self._url = url

    def run(self):
        print len(urllib.urlopen(self._url).read())

threads = map(UrlFetchThread, urls)
for t in threads:
    t.start()
    t.join()

# introduce multi process
from multiprocessing import Process
import urllib

urls = ['http://hztdltev01.china.nsn-net.net',
        'http://10.56.117.81/coci/',
        'http://coop.china.nsn-net.net']

class UrlFetchProcess(Process):
    def __init__(self, url, *args):
        super(UrlFetchProcess, self).__init__(*args)
        self._url = url

    def run(self):
        print len(urllib.urlopen(self._url).read())

processes = map(UrlFetchProcess, urls)
for p in processes:
    p.start()
    p.join()

# use Pool
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

urls = ['http://hztdltev01.china.nsn-net.net',
        'http://10.56.117.81/coci/',
        'http://coop.china.nsn-net.net']

def fetch_content(url):
    print len(urllib.urlopen(url).read())

pool = Pool()
pool.map(fetch_content, urls)
pool.close()
pool.join()

# -----------------------------------------
thread_pool = ThreadPool()
thread_pool.map(fetch_content, urls)
thread_pool.close()
thread_pool.join()

# introduce gevent（并发问题）
import gevent
from gevent import monkey
monkey.patch_all()

urls = ['http://hztdltev01.china.nsn-net.net',
        'http://10.56.117.81/coci/',
        'http://coop.china.nsn-net.net']

def fetch_content(url):
    print len(urllib.urlopen(url).read())

[gevent.spawn(fetch_content, url) for url in urls]

gevent.wait()

#=========================================
web development
# mongodb
import pymongo

# create connection
client = pymongo.MongoClient()
# select database
db = client.user
# select collection
collection = db.userinfo
# insert record
collection.insert_one({'id': 123, 'name': 'python'})
collection.insert_one({'id': 124, 'alias': 'python'})
# query
print [e for e in collection.find()]


# sqlite3
import sqlite3 as sqlite

conn = sqlite.connect('user.db')
# create a table
conn.execute('create table user (id, name)')
# insert one record
conn.execute('insert into user values (123, "python")')
# query
cursor = conn.execute('select * from user')
try:
    print cursor.fetchall()
finally:
    cursor.close()


###==========================================
Reference
http://www.diveintopython.net/power_of_introspection/
https://docs.python.org/2/library/inspect.html
https://docs.python.org/2/howto/functional.html
https://en.wikipedia.org/wiki/Functional_programming
https://docs.python.org/2/library/functions.html#iter
http://butunclebob.com/files/downloads/Prime%20Factors%20Kata.ppt
https://blog.8thlight.com/uncle-bob/2013/05/27/TheTransformationPriorityPremise.html
https://wiki.python.org/moin/Generators
https://docs.python.org/2/library/threading.html
https://docs.python.org/2/library/multiprocessing.html
http://www.gevent.org/intro.html
http://bottlepy.org/docs/dev/index.html
http://api.mongodb.org/python/current/tutorial.html
https://docs.python.org/2/library/simplehttpserver.html

##===========================================
1：log的存取，解压缩，web
2：邮件的自动回复

