#!/usr/bin/env python
# encoding: utf-8
'''
# #----------------------------------------------------------------------
#  Copyright: 2015~2025
#  module:_01_my_email_smaple_for_html.py
#  Function :
#  Data: 2016/4/20 10:31
#  Author:changpzh
#  Email:changping.zhou@foxmail.com
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
'''
import smtplib, os
from email.mime.text import MIMEText
from email.header import Header

smtpserver = 'mail.emea.nsn-intra.net'
sender = 'changping.zhou@foxmail.com'
receiver = 'changping.zhou@nokia.com'

subject ='python email test'

#中文需参数‘utf-8’，单字节字符不需要
msg = MIMEText('你好!','text','utf-8')
msg['Subject'] = Header(subject, 'utf-8')

smtp = smtplib.SMTP()
smtp.connect(smtpserver)
smtp.set_debuglevel(1) #这一步其实可以不用要，只是消息打印
#smtp.login(username, password) #公司的邮件不需要这个
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()
