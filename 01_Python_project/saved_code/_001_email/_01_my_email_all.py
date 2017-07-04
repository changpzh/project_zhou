#!/usr/bin/env python
# encoding: utf-8
'''
# #----------------------------------------------------------------------
#  Copyright: 2015~2025
#  module:_01_my_email_all.py
#  Function :
#  Data: 2016/4/21 15:45
#  Author:changpzh
#  Email:changping.zhou@foxmail.com
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
'''
import unittest
# import HTMLTestRunner
import smtplib
import os,time,datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def sendmail(file_new):
    # smtpsever = 'mail.emea.nsn-intra.net'
    smtpsever = 'smtp.163.com'
    mail_from = 'zhouhanxin2008@163.com'
    mail_to   = 'changping.zhou@foxmail.com'
    f = open(file_new,'rb')
    mail_body = f.read()
    f.close()
    msg = MIMEText(mail_body,_subtype='html', _charset='utf-8')
    msg['Subject'] = u'python邮件测试'
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
    msg['to'] = mail_to

    username = "zhouhanxin2008@163.com"
    password = "password"
    smtp = smtplib.SMTP()
    smtp.connect(smtpsever)
    smtp.login(username, password)
    smtp.sendmail(mail_from, mail_to, msg.as_string())
    smtp.quit()
    print('mail has been send out!')

def sendreport():
    result_dir = 'D:\\test_zhou'
    lists = os.listdir(result_dir)
    # find the latest modified file in give path.
    lists.sort(key=lambda fn: os.path.getmtime(result_dir+"\\"+fn) if not os.path.isdir(result_dir+"\\"+fn) else 0, reverse=True)
    print(u'最新测试生成报告：'+lists[0])
    file_new = os.path.join(result_dir, lists[0])
    sendmail(file_new)


if __name__ == '__main__':
    # runner.run(alltestnames)
    sendreport()