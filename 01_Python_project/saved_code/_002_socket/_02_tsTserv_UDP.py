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
    udpSerSock = socket(AF_INET, SOCK_DGRAM)
    udpSerSock.bind(ADDR)

    while True:
        print('Waiting for message...')
        data, addr = udpSerSock.recvfrom(BUFSIZ)
        print(addr)
        udpSerSock.sendto('[%s] %s' % (ctime(), data), addr)
        print('...received from and returned to:', addr)

    # udpSerSock.close()

if __name__ == '__main__':
    main()