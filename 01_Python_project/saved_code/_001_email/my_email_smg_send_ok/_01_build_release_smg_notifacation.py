#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# #----------------------------------------------
#  Copyright: 2015~2025
#  Function : send message
#  Data: 2016/5/16 16:02
#  Author:changping.zhou@foxmail.com
# #----------------------------------------------
# #----------------------------------------------
'''

from __future__ import with_statement
import smtplib
import os, time
import argparse
from config.default_settings import HANDLE_SMS, MAIL_SENDER, MAIL_HOST
from email.mime.multipart import MIMEMultipart

class MailOperation():
    def __init__(self, sender="", to_list=[], cc_list=[], subject="", subject="", packageName="", jobName=""):
        self.sender = sender
        self.to_list = to_list
        self.cc_list = cc_list
        self.subject = subject
        self.content = content
        self.packageName = packageName
        self.jobName = jobName

    def send_sms(self):
        contents = MIMEMultipart('related')
        contents['from'] = self.sender or MAIL_SENDER
        contents['to'] = ";".join(self.to_list)
        contents['cc'] = ";".join(self.cc_list)
        contents['Subject'] = self.subject
        contents.preamble = 'This is a multi-part message in MIME format.'

        # msg = MIMEText(self.content,'html','utf-8')
        # contents.attach(msg)
        try:
            smtp = smtplib.SMTP()
            smtp.connect(MAIL_HOST)
            smtp.set_debuglevel(1)
            if self.to_list:
                smtp.sendmail(contents['from'],self.to_list,contents.as_string())
            if self.cc_list:
                smtp.sendmail(contents['from'],self.cc_list,contents.as_string())
            smtp.quit()
        except:
            sys.exit(1)

    def format_content(self):
        pass

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

def Sms_ListGet(jobName): #return smg_to/cc_list
    envFile = ROOT_PATH + '/config/' + jobName + '.txt'
    smg_to_list=[]
    smg_cc_list=[]
    smg_to_str=jobName+'_to'
    smg_cc_str=jobName+'_cc'
    smg_to_flag=False
    smg_cc_flag=False
    f_LineList = Func_ReadFile(envFile,'r')
    for line in f_LineList:
        line = line.replace('\t','').replace('\n','').replace('\r','').replace(' ','')
        if smg_to_flag:
            if (not line.startswith('#')) and (len(line) > 0) and ('smsgw' in line):
                smg_to_list.append(line)
            elif not len(line):
                smg_to_flag = False
        if smg_cc_flag:
            if (not line.startswith('#')) and (len(line) > 0) and ('smsgw' in line):
                smg_cc_list.append(line)
            elif not len(line):
                smg_cc_flag = False

        if smg_to_str in line:
            smg_to_flag = True
        if smg_cc_str in line:
            smg_cc_flag = True

    print("******smg_to_list are:")
    for item in smg_to_list:
        print(item)
    print("******smg_cc_list are:")
    for item in smg_cc_list:
        print(item)

    return (smg_to_list, smg_cc_list)

def Pass_sms_send(packageName, jobName, subject, smg_to_list, smg_cc_list):
    smg_operator = MailOperation()
    smg_operator.sender = MAIL_SENDER
    smg_operator.packageName = packageName
    smg_operator.jobName = jobName
    # smg_operator.subject = packageName + " released for QT at " + time.strftime("%m/%d %H:%M")
    smg_operator.subject = subject
    smg_operator.to_list = smg_to_list
    smg_operator.cc_list = smg_cc_list

    smg_operator.send_sms()

def argsParser():
    parser = argparse.ArgumentParser(description='This is used to send email')
    parser.add_argument('-n', '--name', action='store', dest='packageName', default='PACKNAME', help='This is package name')
    parser.add_argument('-j', '--job', action='store', dest='jobName', default='job_name', help='This is job name')
    parser.add_argument('-s', '--subject', dest='subject', default='SUBJECT', help='This is subject')
    args = parser.parse_args()

    global ROOT_PATH
    ROOT_PATH = os.getcwd().replace("\\","/")
    if args.packageName:
        packageName = args.packageName
        print("package name is:" + packageName)
    if args.jobName:
        jobName = args.jobName
        print("package name is:" + jobName)
    subject = args.subject

    return (packageName, jobName, subject)

def main():
    (packageName, jobName,subject) = argsParser()
    (smg_to_list, smg_cc_list) = Sms_ListGet(jobName)

    if HANDLE_SMS == 'TRUE':
        Pass_sms_send(packageName,jobName, subject, smg_to_list, smg_cc_list)

if __name__ == '__main__':
    main()