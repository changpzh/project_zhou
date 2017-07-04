#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# #----------------------------------------------
#  Copyright: 2015~2025
#  Function :
#  Data: 2016/5/19 11:12
#  Author:changping.zhou@foxmail.com
# #----------------------------------------------
# #----------------------------------------------
'''

from __future__ import with_statement
import smtplib
import os, time
import argparse
from config.default_settings import HANDLE_SMS, HANDLE_META, MAIL_SENDER, MAIL_HOST, MSG_SENDER, TDDCPRI_CI_TO, TDDCPRI_CI_CC
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MailOperation():
    def __init__(self, sender="", to_list=[], cc_list=[], subject="", content="", om_meta="",cprit_meta="", packageName="", jobName=""):
        self.sender = sender
        self.to_list = to_list
        self.cc_list = cc_list
        self.subject = subject
        self.content = content
        self.packageName = packageName
        self.jobName = jobName
        self.omMeta = om_meta
        self.cpriMeta = cprit_meta

    def send_mail(self):
        contents = MIMEMultipart('related')
        contents['from'] = self.sender or MAIL_SENDER
        contents['to'] = ";".join(self.to_list)
        contents['cc'] = ";".join(self.cc_list)
        contents['Subject'] = self.subject
        # contents.preamble = 'This is a multi-part message in MIME format.'

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

    def send_sms(self):
        contents = MIMEMultipart('related')
        contents['from'] = self.sender or MAIL_SENDER
        contents['to'] = ";".join(self.to_list)
        contents['cc'] = ";".join(self.cc_list)
        contents['Subject'] = self.subject
        contents.preamble = 'This is a multi-part message in MIME format.'

        msg = MIMEText(self.format_content(),'html','utf-8')
        contents.attach(msg)
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

        message = "Hi,<br><br>TL16A build meta check. Please do meta alignment<br>"
        message += "<br>%s<br>" % self.content
        message += "%s<br>%s<br>" % ( self.omMeta, self.cpriMeta)
        message += "Mail Need send to:<br>%s;%s" % (TDDCPRI_CI_TO, TDDCPRI_CI_CC)

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

def getMailList(jobName):
    envFile = ROOT_PATH + '/config/' + jobName + '.txt'
    to_list=[]
    cc_list=[]
    to_flag=False
    cc_flag=False
    to_str=jobName+'_to'
    cc_str=jobName+'_cc'
    if os.path.isfile(envFile):
        print("we found needed file")
        p_mailListLines=Func_ReadFile(envFile,'r')
        for line in p_mailListLines:
            line = line.replace('\t','').replace('\n','').replace('\r','').replace(' ','')
            if to_flag:
                if (not line.startswith('#')) and (len(line) > 0) and ('+' not in line):
                    to_list.append(line)
                elif not len(line):
                    to_flag=False
            elif cc_flag:
                if (not line.startswith('#')) and (len(line) > 0) and ('+' not in line):
                    cc_list.append(line)
                    print(cc_list)
                elif not len(line):
                    cc_flag=False
            if to_str in line:
                to_flag=True
            if cc_str in line:
                cc_flag=True
    print("******to_list are:")
    for item in to_list:
        print(item)
    print("******cc_list are:")
    for item in cc_list:
        print(item)
    return(to_list, cc_list)

def Sms_ListGet(jobName): #return smg_to/cc_list
    envFile = ROOT_PATH + '/config/' + jobName + '.txt'
    smg_to_list=[]
    smg_cc_list=[]
    smg_to_str=jobName+'_to'
    smg_cc_str=jobName+'_cc'
    smg_to_flag=False
    smg_cc_flag=False
    if os.path.isfile(envFile):
        print("we found needed file")
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

def meta_compaire_email_send(packageName, jobName, subject, contents, mail_to_list, mail_cc_list):
    mail_operator = MailOperation()
    mail_operator.sender = MAIL_SENDER
    mail_operator.packageName = packageName
    mail_operator.jobName = jobName
    mail_operator.subject = subject
    mail_operator.content = contents[0]
    mail_operator.to_list = mail_to_list
    mail_operator.cc_list = mail_cc_list
    mail_operator.omMeta = contents[1]
    mail_operator.cpriMeta = contents[2]

    mail_operator.send_mail()

def Pass_sms_send(packageName, jobName, subject, smg_to_list, smg_cc_list):
    smg_operator = MailOperation()
    smg_operator.sender = MSG_SENDER
    smg_operator.packageName = packageName
    smg_operator.jobName = jobName
    # smg_operator.subject = packageName + " released for QT at " + time.strftime("%m/%d %H:%M")
    smg_operator.subject = subject
    smg_operator.to_list = smg_to_list
    smg_operator.cc_list = smg_cc_list

    smg_operator.send_sms()

def meta_compaire_smg_send(packageName, jobName, subject, contents, smg_to_list, smg_cc_list):
    smg_operator = MailOperation()
    smg_operator.sender = MSG_SENDER
    smg_operator.packageName = packageName
    smg_operator.jobName = jobName
    smg_operator.subject = subject
    smg_operator.content = contents[0]
    smg_operator.to_list = smg_to_list
    smg_operator.cc_list = smg_cc_list
    smg_operator.omMeta = contents[1]
    smg_operator.cpriMeta = contents[2]

    smg_operator.send_sms()

def argsParser():
    parser = argparse.ArgumentParser(description='This is used to send email')
    parser.add_argument('-n', '--name', action='store', dest='packageName', default='PACKNAME', help='This is package name')
    parser.add_argument('-j', '--job', action='store', dest='jobName', default='job_name', help='This is job name')
    parser.add_argument('-s', '--subject', dest='subject', default='SUBJECT', help='This is subject of msg')
    parser.add_argument('-f', '--file', dest='fileName', default='./emta_file.txt', help='This is file contains meta info')

    args = parser.parse_args()

    global ROOT_PATH
    ROOT_PATH = os.getcwd().replace("\\","/")
    if args.packageName:
        packageName = args.packageName
        print("package name is:" + packageName)
    if args.jobName:
        jobName = args.jobName
        print("Job name is:" + jobName)
    subject = args.subject

    FileName = args.fileName

    return (packageName, jobName, subject, FileName)

def main():
    (packageName, jobName, subject, FileName) = argsParser()
    
    (mail_to_list, mail_cc_list) = getMailList(jobName)
    (smg_to_list, smg_cc_list) = Sms_ListGet(jobName)

    # if HANDLE_SMS == 'TRUE':
    #    Pass_sms_send(packageName,jobName, subject, smg_to_list, smg_cc_list)

    meta_FilePath = os.path.join(ROOT_PATH, FileName)
    contents = Func_ReadFile(meta_FilePath, "r")
    if HANDLE_META == 'TRUE':
        meta_compaire_smg_send(packageName, jobName, subject, contents, smg_to_list, smg_cc_list)

        if (contents[1].split('@')[-1]) == (contents[2].split('@')[-1]): subject = "Meta Aligned on " + packageName
        else: subject = "Meta not Aligned on " + packageName
        meta_compaire_email_send(packageName, jobName, subject, contents, mail_to_list, mail_cc_list)


    # send email to cpri team if om_meta newer than cpri_meta, else send it to myslef.
    # if (contents[1].split('@')[-1]) > (contents[2].split('@')[-1]):
    #     meta_compaire_email_send(packageName, jobName, subject, contents, mail_to_list[:-1], mail_cc_list)
    # else:
    #     meta_compaire_email_send(packageName, jobName, subject, contents, mail_to_list[1:], mail_cc_list)

if __name__ == '__main__':
    main()