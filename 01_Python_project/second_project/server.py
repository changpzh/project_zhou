#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xmlrpclib import ServerProxy, Fault
from os.path import join, abspath, isfile, exists
from SimpleXMLRPCServer import SimpleXMLRPCServer
from urlparse import urlparse
import sys

SimpleXMLRPCServer.allow_reuse_address = 1

MAX_HISTORY_LENGTH = 6

UNHANDLED       = 100
ACCESS_DENIED   = 200

class UnhandledQuery(Fault):
    """
    表示无法处理的查询异常
    """
    def __init__(self, message="Couldn't handle the query"):
        Fault.__init__(self, UNHANDLED, message)

class AccessDenied(Fault):
    """
    用户试图访问未被授权的资源时引发的异常
    """
    def __init__(self, message="Access denied"):
        Fault.__init__(self, ACCESS_DENIED, message)

def inside(dir, name):
    """
    检查给定的目录是否有给定的文件
    :param dir:
    :param name:
    :return:
    """
    dir = abspath(dir)
    name = abspath(name)
    return exists(join(dir, name))

def getPort(url):
    """
    从url中提取port
    :param url:
    :return:
    """
    name = urlparse(url)[1]
    parts = name.split(":")
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
        try:
            return self._handle(query)
        except UnhandledQuery:
            history = history + [self.url]
            if len(history) >= MAX_HISTORY_LENGTH: raise
            return self._broadcast(query, history)

    def hello(self, other):
        """
        用于将节点介绍给其它节点
        :param other:
        :return:
        """
        self.known.add(other)
        return 0

    def fetch(self, query, secret):
        """
        用于让节点找到文件并下载
        :param query:
        :param secret:
        :return:
        """
        if secret != self.secrect: return AccessDenied
        result = self.query(query)
        f = open(join(self.dirname, query), 'w')
        f.write(result)
        f.close()
        return 0

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
        if not isfile(name): raise UnhandledQuery
        if not inside(dir, name): raise AccessDenied
        return open(name).read()

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
                return s.query(query, history)

            except Fault, f:
                if f.faultCode == UNHANDLED: pass
                else: self.known.remove(other)
        return UnhandledQuery

def main():
    url, directory, secret = sys.argv[1:]
    n = Node(url, directory, secret)
    n._start()

if __name__ == '__main__':
    main()

