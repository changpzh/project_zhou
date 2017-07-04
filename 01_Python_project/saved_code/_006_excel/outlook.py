#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# #----------------------------------------------
#  Copyright: 2015~2025
#  Function :
#  Data: 2016/5/25 14:48
#  Author:changping.zhou@foxmail.com
# #----------------------------------------------
# #----------------------------------------------
'''
from tkinter import Tk
from time import sleep
from tkinter.messagebox import showwarning
import win32com.client as win32

warn = lambda app: showwarning(app, 'Exit?') # 显示询问是否退出窗口
RANGE = range(3, 8)

def outlook():
    app = 'Outlook'
    olook = win32.gencache.EnsureDispatch('%s.Application' % app)

    mail = olook.CreateItem(win32.constants.olMailItem)
    recip = mail.Recipients.Add('changping.zhou@nokia.com')
    subj = mail.Subject = 'Python-to-%s Demo' % app
    body = ["Line %d" % i for i in RANGE]
    body.insert(0, '%s\r\n' % subj)
    body.append("\r\nTh-th-th-that's all folks!\r\n")
    print(body)
    mail.Body = '\r\n'.join(body)
    print(mail.Body)
    mail.Send()

    ns = olook.GetNamespace("MAPI")
    obox = ns.GetDefaultFolder(win32.constants.olFolderOutbox)
    obox.Display()
    obox.Items.Item(1).Display()

    warn(app)
    olook.Quit()

if __name__ == '__main__':
    Tk().withdraw()
    outlook()