#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# #----------------------------------------------
#  Copyright: 2015~2025
#  Function :
#  Data: 2016/5/23 15:43
#  Author:changping.zhou@foxmail.com
# #----------------------------------------------
# #----------------------------------------------
'''
from tkinter import Tk
from time import sleep
# from tkMessageBox import showwarning --->
from tkinter.messagebox import showwarning
import win32com.client as win32

warn = lambda app: showwarning(app, 'Exit?')
RANGE = range(3,8)

def excel():
    app = 'Excel'
    xl = win32.gencache.EnsureDispatch('%s.Application' % app)
    print(xl)
    ss = xl.Workbooks.Add()
    sh = ss.ActiveSheet
    xl.Visible = True
    sleep(1)
    print(ss)
    print(sh)

    sh.Cells(1,1).Value = 'Python-to-%s Demo' % app
    sleep(1)
    for i in RANGE:
        sh.Cells(i,1).Value = 'Line %d' % i
        sleep(1)
    sh.Cells(i+2, 1).Value = "Th-th-th-that's all folks!"

    warn(app)
    ss.Close(False)
    xl.Application.Quit()

if __name__ == '__main__':
    Tk().withdraw()
    excel()