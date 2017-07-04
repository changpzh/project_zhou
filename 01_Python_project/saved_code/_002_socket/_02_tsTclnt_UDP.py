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
    # HOST = 'localhost'    # server's IP
    HOST = '10.0.2.15'   # server's IP
    PORT = 21567
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    udpCliSock = socket(AF_INET, SOCK_DGRAM)


    while True:
        data = raw_input('>')
        if not data:
            break
        udpCliSock.sendto(data, ADDR)
        data = udpCliSock.recvfrom(BUFSIZ)
        if not data:
            break
        print(data)
        # print(udpCliSock.close())

if __name__ == '__main__':
    main()