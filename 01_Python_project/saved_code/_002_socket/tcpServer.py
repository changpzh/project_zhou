#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# #-------------------------------------
#  Copyright: 2015~2025
#  Function :
#  Data: 2016/11/4 10:46
#  Author:changping.zhou@foxmail.com
# #--------------------------------------
# #--------------------------------------
'''
import socket

def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)

    c, addr = s.accept()
    print("Connection from: " + str(addr))

    while True:
        data = c.recv(1024)
        if not data:
            break
        print("from connected user: " + str(data))
        data = str(data).upper()
        print("sending: " + str(data))
        c.send(data)
    c.close()

if __name__ == '__main__':
    Main()
