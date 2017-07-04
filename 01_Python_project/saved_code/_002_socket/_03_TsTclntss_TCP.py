#!/usr/bin/env python
# encoding: utf-8
'''
# #----------------------------------------------------------------------
#  Copyright: 2015~2025
#  module:_03_TsTclntss_TCP.py
#  Function :
#  Data: 2016/2/4 15:46
#  Author:changpzh
#  Email:changping.zhou@foxmail.com
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
'''
from socket import *

# HOST = 'localhost'    # server's IP
HOST = '10.140.26.43'   # server's IP
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

def main():
    while True:
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        data = raw_input('>')
        if not data:
            break
        tcpCliSock.send('%s\r\n' % data)
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        print(data.strip())
        # tcpCliSock.close()


if __name__ == '__main__':
    main()