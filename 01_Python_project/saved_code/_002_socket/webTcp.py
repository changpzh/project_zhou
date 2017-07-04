#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# #-------------------------------------
#  Copyright: 2015~2025
#  Function :
#  Data: 2016/11/4 10:41
#  Author:changping.zhou@foxmail.com
# #--------------------------------------
# #--------------------------------------
'''
import socket
def handle_request(client):
    buf = client.recv(1024)
    client.send("HTTP/1.1 200 OK\r\n")
    client.send("Content-Type:text/html\r\n\r\n")
    client.send("<h2> Hello World </h2>")

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8080))
    sock.listen(5)

    while True:
        connection, address = sock.accept()
        handle_request(connection)
        connection.close()

if __name__ == '__main__':
    main()
