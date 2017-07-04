#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xmlrpclib import ServerProxy
from os.path import join, isfile
from SimpleXMLRPCServer import SimpleXMLRPCServer
from urlparse import urlparse
import sys

MAX_HISTORY_LENGTH = 6

OK = 1
FAIL = 2
EMPTY = ''

def getPort(url):
    '用URL中提取端口'
    name = urlparse(url)[1]
    parts = name.split(':')
    return int(parts[-1])

class Node:
    """
    P2P网络中的节点
    """
    def __init__(self, url, dirname, secrect):
        self.url = url
        self.dirname = dirname
        self.secrect = secrect
        self.known = set()

    def query(self, query, history=[]):
        """
        查询文件，可能会向其它已知节点请求帮助，将文件作为字符串返回
        :param query:
        :param history:
        :return:
        """
        code,data = self._handle(query)
        if code == OK:
            return code, data
        else:
            history = history + [self.url]
            if len(history) >= MAX_HISTORY_LENGTH:
                return FAIL, EMPTY
            return self._broadcast(query, history)

    def hello(self, other):
        """
        用于将节点介绍给其它节点
        :param other:
        :return:
        """
        self.known.add(other)
        return OK

    def fetch(self, query, secret):
        """
        用于让节点找到文件并下载
        :param query:
        :param secret:
        :return:
        """
        if secret != self.secrect: return FAIL
        code, data = self.query(query)
        if code == OK:
            f = open(join(self.dirname, query), 'w')
            f.write(data)
            f.close()
            return OK
        else:
            return FAIL

    def _start(self):
        """
        内部使用，用于启动XML_RPC服务器
        :return:
        """
        s = SimpleXMLRPCServer(("", getPort(self.url)), logRequests=False)
        s.register_instance(self)
        s.serve_forever()

    def _handle(self, query):
        """
        内部使用，用于处理请求
        :return:
        """
        dir = self.dirname
        name = join(dir, query)
        if not isfile(name): return FAIL, EMPTY
        return OK, open(name).read()

    def _broadcast(self, query, history):
        """
        内部使用，用于查询广播到所有已知的Node
        :param query:
        :param history:
        :return:
        """
        for other in self.known.copy():
            if other in history: continue
            try:
                s = ServerProxy(other)
                code, data = s.query(query, history)
                if code == OK:
                    return code, data
            except:
                self.known.remove(other)
        return FAIL, EMPTY

def main():
    url, directory, secret = sys.argv[1:]
    n = Node(url, directory, secret)
    n._start()

if __name__ == '__main__':
    main()

