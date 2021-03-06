#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# #-------------------------------------
#  Copyright: 2015~2025
#  Function :
#  Data: 2016/11/4 10:49
#  Author:changping.zhou@foxmail.com
# #--------------------------------------
# #--------------------------------------
'''
import socket

def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.connect((host, port))

    message = raw_input("-> ")
    while message != 'q':
        s.send(message)
        data = s.recv(1024)
        print("Recieved from server: " + str(data))
        message = raw_input("-> ")
    s.close()

if __name__ == '__main__':
    Main()
