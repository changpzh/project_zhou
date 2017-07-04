#!/usr/bin/env python
# encoding: utf-8
'''
# #----------------------------------------------------------------------
#  Copyright: 2015~2025
#  module:tsTclnt.py
#  Function :
#  Data: 2016/2/3 17:07
#  Author:changpzh
#  Email:changping.zhou@foxmail.com
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
'''
from socket import *

def main():
    # HOST = 'localhost'    # server's name
    HOST = '10.140.26.43'   # server's name
    PORT = 21567            # server's port
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)

    while True:
        data = raw_input('>')
        if not data:
            break
        tcpCliSock.send(data)
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        print(data)

    tcpCliSock.close()

if __name__ == '__main__':
    main()