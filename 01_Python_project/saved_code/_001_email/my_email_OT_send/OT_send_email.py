#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
# #----------------------------------------------
#  Copyright: 2015~2025
#  Function :
#  Data: 2016/5/23 17:07
#  Author:changping.zhou@foxmail.com
# #----------------------------------------------
# #----------------------------------------------
'''
import smtplib
import os, time
from config.ot_config import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailOperation():
    def __init__(self, sender="", to_list="", cc_list="", subject="", content=[]):
        self.sender = sender
        self.to_list = to_list
        self.cc_list = cc_list
        self.subject = subject
        self.content = content

    def send_mail(self):
        contents = MIMEMultipart('related')
        contents['from'] = self.sender or MAIL['SENDER']
        contents['to'] = self.to_list
        contents['cc'] = self.cc_list
        contents['Subject'] = self.subject
        contents.preamble = 'This is a multi-part message in MIME format.'

        msg = MIMEText(self.format_content(),'html','utf-8')
        contents.attach(msg) #这句不要，则内容会为空
        try:
            smtp = smtplib.SMTP()
            smtp.connect(MAIL_HOST)
            # smtp.set_debuglevel(1)
            if self.to_list:
                smtp.sendmail(contents['from'],self.to_list,contents.as_string())
            if self.cc_list:
                smtp.sendmail(contents['from'],self.cc_list,contents.as_string())
            smtp.quit()
        except:
            sys.exit(1)

    def format_content(self):
        message = ""
        for content in self.content:
            message += "%s<br>" % content.decode('utf-8') #保证输出和源文件一样
        return message

def Func_ReadFile(fullPathFile, ReadMode):
    if not os.path.isfile(fullPathFile):
        print("File %s does not exists" % (fullPathFile))
        return []
    try:
        with open(fullPathFile, ReadMode) as f:
            return f.readlines()
    except IOError:
        print("Open %s failed!" % (fullPathFile))
        return []


def ot_Notification_email_send(subject, contents, mail_to, mail_cc):
    mail_operator = MailOperation()
    mail_operator.subject = subject
    mail_operator.content = contents
    mail_operator.to_list = mail_to
    mail_operator.cc_list = mail_cc

    mail_operator.send_mail()

def main():
    ot_FilePath = os.path.join(os.getcwd(), 'ot_content.txt')
    print(ot_FilePath)
    sub_title = ' TL16A晚上值班需要注意事项'
    subject = time.strftime("%Y/%m/%d") + sub_title
    # subject ='Please pay attention on branch TL16A at ' +   time.strftime("%Y/%m/%d") + ' night'
    contents = Func_ReadFile(ot_FilePath, "rb") #要读取中文字符，加‘b’模式
    ot_Notification_email_send(subject, contents, MAIL['TO'], MAIL['CC'])

if __name__ == '__main__':
    main()