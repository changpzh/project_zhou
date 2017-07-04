#!/usr/bin/env python
# encoding: utf-8
'''
# #----------------------------------------------------------------------
#  Copyright: 2015~2025
#  module:_01_Email_Smg_Notification.py
#  Function :   1: arguments parse
#               2: get mail(to,cc) list
#               3: mail send
#  Data: 2016/4/21 16:38
#  Author:changpzh
#  Email:changping.zhou@foxmail.com
# #----------------------------------------------------------------------
# #----------------------------------------------------------------------
'''
from __future__ import with_statement #短信时需要
import argparse
import os
from config.default_settings import HANDLE_EMAIL, HANDLE_SMS
from my_utils import MailOperation

def Func_FileRead(FileFullPath, ReadMode = 'r'):
    if not os.path.isfile(FileFullPath):
        print("File %s does not exists" % (FileFullPath))
        return []
    try:
        with open(FileFullPath, ReadMode) as p_FileObj:
            return p_FileObj.readlines()
    except IOError:
        print("Open %s failed!" % (FileFullPath))
        return []

def getMailList(jobName):
    # jobName = "FSIH_FZNN_1Pipe_QT1_BTS157_57"
    ENVINFO=jobName.split('_')[-2]+'_'+jobName.split('_')[-1]
    print("ENVINFO is:"+ ENVINFO)
    to_list=[]
    cc_list=[]
    to_flag=False
    cc_flag=False
    to_str=ENVINFO+'_to'
    cc_str=ENVINFO+'_cc'
    if os.path.isfile(ROOT_PATH + '/config/' + ENVINFO +'.txt'):
        print("we found needed file")
        p_mailListLines=Func_FileRead(ROOT_PATH + '/config/' + ENVINFO +'.txt','r')
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
        # LOG.info(item)
        print(item)
    print("******cc_list are:")
    for item in cc_list:
        # LOG.info(item)
        print(item)
    return(to_list,cc_list)

def getSmgList(jobName):
    ENVINFO=jobName.split('_')[-2]+'_'+jobName.split('_')[-1]
    print("ENVINFO is:"+ ENVINFO)
    smg_to_list=[]
    smg_cc_list=[]
    smg_to_flag=False
    smg_cc_flag=False
    smg_to_str=ENVINFO+'_to'
    smg_cc_str=ENVINFO+'_cc'
    if os.path.isfile(ROOT_PATH + '/config/' + ENVINFO +'.txt'):
        print("we found needed file")
        p_mailListLines=Func_FileRead(ROOT_PATH + '/config/' + ENVINFO +'.txt','r')
        for line in p_mailListLines:
            line = line.replace('\t','').replace('\n','').replace('\r','').replace(' ','')
            if smg_to_flag:
                if (not line.startswith('#')) and (len(line) > 0) and ('smsgw' in line):
                    smg_to_list.append(line)
                elif not len(line):
                    smg_to_flag=False
            elif smg_cc_flag:
                if (not line.startswith('#')) and (len(line) > 0) and ('smsgw' in line):
                    smg_cc_list.append(line)
                elif not len(line):
                    smg_cc_flag=False
            if smg_to_str in line:
                smg_to_flag=True
            if smg_cc_str in line:
                smg_cc_flag=True
    print("******to_list are:")
    for item in smg_to_list:
        # LOG.info(item)
        print(item)
    print("******cc_list are:")
    for item in smg_cc_list:
        # LOG.info(item)
        print(item)
    return(smg_to_list,smg_cc_list)

def Failed_mail_notification(packageName, jobName, jobStatus, jobCase, jobTime, jobURL, to_list, cc_list):
    # LOG.info("Start to send email")
    print("Start to send email")
    mail_operator = MailOperation()    #类实例化
    mail_operator.to_list=to_list
    mail_operator.cc_list=cc_list
    mail_operator.subject = jobName + ' ' + jobStatus + ' notification' + '(' + packageName + ',' + jobCase + ')'
    mail_operator.content = 'Pls check it ASAP!'
    mail_operator.packageName = packageName
    mail_operator.jobName = jobName
    mail_operator.jobStatus = jobStatus
    mail_operator.jobCase = jobCase
    mail_operator.jobTime = jobTime
    mail_operator.jobURL = jobURL
    mail_operator.send_mail()

def Failed_sms_notification(packageName, jobName, jobStatus, jobCase, jobTime, jobURL, smg_to_list, smg_cc_list, to_list):
    # LOG.info("Start to send email")
    print("Start to send smg")
    smg_operator = MailOperation() #类实例化

    if to_list:
        smg_operator.sender=to_list[0]
        # smg_operator.sender='changping.zhou@nokia.com' #必须要sender（收费问题）
        print("SMG sender is:" + to_list[0])

    smg_operator.to_list=smg_to_list
    smg_operator.cc_list = smg_cc_list

    smg_operator.subject = jobName + ' ' + jobStatus + ' notification' + '(' + packageName + ',' + jobCase + ')'
    # smg_operator.content = "<a href='%s/console'>%s/console</a>" % (jobURL, jobURL)

    smg_operator.send_sms()

def argsParser():
    '''
        *Parsing arguments from SyslogChecking invocation
    '''
    parser = argparse.ArgumentParser(description='This is used to send email')
    parser.add_argument('-n', '--name',action='store', dest='packageName', default='PACKNAME', help='This is QT package name')
    parser.add_argument('-j', '--job',action='store', dest='jobName', default='job_name', help='This is job name')
    parser.add_argument('-s', '--status',action='store', dest='jobStatus', default='job_status', help='This is job status')
    parser.add_argument('-c', '--case',action='store', dest='jobCase', default='run_target', help='identify which case will be tested')
    parser.add_argument('-t', '--time',action='store', dest='jobTime', default='starttime', help='This is job starttime')
    parser.add_argument('-u', '--url',action='store', dest='jobURL', default='url', help='This is job URL')
    args = parser.parse_args()

    global ROOT_PATH
    ROOT_PATH = os.getcwd().replace("\\","/")
    print("ROOT_PATH is:"+ ROOT_PATH)
    if args.packageName:
        packageName = args.packageName
        print("package name is: %s" % packageName)
    if args.jobName:
        jobName = args.jobName
    if args.jobStatus:
        jobStatus = args.jobStatus
    if args.jobCase:
        jobCase = args.jobCase
    if args.jobTime:
        jobTime = args.jobTime
    if args.jobURL:
        jobURL = args.jobURL
    return(packageName, jobName, jobStatus, jobCase, jobTime, jobURL)

def main():
    p_Syslog = "mailNotification.log"

    #参数解析
    # #!/bin/bash
    # python _01_Email_Smg_Notification.py -n ${packageName} -j ${jobName} -s ${jobStatus} -c ${jobCase} -t ${jobTime} -u ${jobURL} || exit 1
    # (packageName, jobName, jobStatus, jobCase, jobTime, jobURL) = argsParser()
    global ROOT_PATH
    ROOT_PATH = os.getcwd().replace("\\","/")
    packageName = "TL00_ENB_9999_151127_037520"
    jobName = "FSIH_FZNN_1Pipe_QT1_BTS157_57"
    jobStatus = "test"
    jobCase = "6_CPE_Throught_UDP_Trunk"
    jobTime = "2015-11-30_12-17-30"
    jobURL = "http://hzling23.china.nsn-net.net:8080/job/TDD_QTp1_BTS157_57/916/"

    #获取邮件发送和抄送对象list
    (to_list,cc_list) = getMailList(jobName)

    #邮件发送
    if HANDLE_EMAIL == 'TRUE':
        Failed_mail_notification(packageName, jobName, jobStatus, jobCase, jobTime, jobURL, to_list, cc_list)

    #获取短信发送对象list
    (smg_to_list,smg_cc_list) = getSmgList(jobName)
    #短信发送
    if HANDLE_SMS == 'TRUE':
        Failed_sms_notification(packageName, jobName, jobStatus, jobCase, jobTime, jobURL, smg_to_list, smg_cc_list, to_list)

if __name__ == '__main__':
    main()