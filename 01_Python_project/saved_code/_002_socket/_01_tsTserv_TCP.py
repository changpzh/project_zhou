#!/usr/bin/env python
# encoding: utf-8
'''
# #----------------------------------------------------------------------
#  Copyright: 2015~2025
#  module:tsTserv.py
#  Function :
#  Data: 2016/2/3 16:34
#  Author:changpzh
#  Email:changping.zhou@foxmail.com
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
'''

from socket import *
from time import ctime

def main():
    HOST = ""
    PORT = 21567
    BUFSIZ = 10240
    ADDR = (HOST, PORT)

    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)    #允许多少个连接同时连接进来

    while True:
        print('Waiting for connection...')
        tcpCliSock, addr = tcpSerSock.accept()
        print('...connected from:', addr)

        while True:
            data = tcpCliSock.recv(BUFSIZ)
            if not data:
                break
            tcpCliSock.send('[%s] %s' % (ctime(), data))

            # tcpCliSock.close()  #这行不要，提醒结束时，要用close().
    # tcpSerSock.close()

if __name__ == '__main__':
    main()