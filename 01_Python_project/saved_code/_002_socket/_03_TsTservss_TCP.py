#!/usr/bin/env python
# encoding: utf-8
'''
# #----------------------------------------------------------------------
#  Copyright: 2015~2025
#  module:_03_TsTservss_TCP.py
#  Function :
#  Data: 2016/2/4 15:35
#  Author:changpzh
#  Email:changping.zhou@foxmail.com
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
'''

from SocketServer import (TCPServer as TCP,
      StreamRequestHandler as SRH)
from time import ctime


class MyRequestHandler(SRH):
    def handle(self):
        print('...connected from:', self.client_address)
        self.wfile.write('[%s] %s' % (ctime(), self.rfile.readline()))


def main():
    HOST = ""
    PORT = 21567
    ADDR = (HOST, PORT)
    tcpServ = TCP(ADDR, MyRequestHandler)
    print('waiting for connection...')
    tcpServ.serve_forever()

if __name__ == '__main__':
    main()