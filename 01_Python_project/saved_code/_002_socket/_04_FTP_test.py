#!/usr/bin/env python
# encoding: utf-8
'''
# #----------------------------------------------------------------------
#  Copyright: 2015~2025
#  module:_04_FTP_test.py
#  Function :
#  Data: 2016/3/31 15:10
#  Author:changpzh
#  Email:changping.zhou@foxmail.com
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
'''
# 例：FTP编程
from ftplib import FTP

ftp = FTP()
timeout = 3000
port = 21

def main():
    ftp.set_debuglevel(2)
    ftp.connect('10.69.65.21',port,timeout) # 连接FTP服务器
    ftp.login('btstest','btstest') # 登录
    print ftp.getwelcome()  # 获得欢迎信息
    ftp.cwd('/pstool/')    # 设置FTP路径
    list = ftp.nlst()       # 获得目录列表
    for name in list:
        print(name)             # 打印文件名字
    # path = 'd:/data/' + name    # 文件保存路径
    # f = open(path,'wb')         # 打开要保存文件
    # filename = 'RETR ' + name   # 保存FTP文件
    # ftp.retrbinary(filename,f.write) # 保存FTP上的文件
    # ftp.delete(name)            # 删除FTP文件
    # ftp.storbinary('STOR '+filename, open(path, 'rb')) # 上传FTP文件
    ftp.quit()                  # 退出FTP服务器


if __name__ == '__main__':
    main()