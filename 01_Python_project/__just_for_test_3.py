# -*- coding:utf-8 -*-

#small server
import socket

s = socket.socket()

host = socket.gethostbyname()
port = 1234
s.bind(host, port)

s.listen(50)
while True:
    c, addr = s.accept()
    print('Got Connection from ', addr)
    c.send('Thank you for connecting')
    c.close()


##small client
import socket
s = socket.socket(socket.AF_INET)

host = socket.gethostname()


port = 1234

s.connect(host, port)
print(s.recv(1234))
