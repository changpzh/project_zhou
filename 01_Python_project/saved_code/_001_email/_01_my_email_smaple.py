#!/usr/bin/env python
# encoding: utf-8
'''
# #----------------------------------------------------------------------
#  Copyright: 2015~2025
#  module:_01_my_email_smaple.py
#  Function :
#  Data: 2016/4/21 13:59
#  Author:changpzh
#  Email:changping.zhou@foxmail.com
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
'''
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def func():
    pass
#邮件信息配置
sender = 'changping.zhou@foxmail.com'
to_receiver = 'changping.zhou@nokia.com'
cc_receiver = 'zzzzhou@163.com'
subject = 'python email test'

smtpserver = 'mail.emea.nsn-intra.net'
# username = ''
# passward = ''

#HTML形式的文件内容
msg = MIMEText('<html><h1>你好！</h1></html>', 'html', 'utf-8')
msg['Subject'] = subject
msg['to'] = to_receiver
msg['cc'] = cc_receiver

smtp = smtplib.SMTP()
smtp.connect(smtpserver)
# smtp.login(username, password)
smtp.sendmail(sender, to_receiver, msg.as_string())
smtp.quit()
