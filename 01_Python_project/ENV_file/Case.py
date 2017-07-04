#!/usr/bin/python
# -*- coding: UTF-8 -*-
#=============================================================
# Copyright: 2012~2015 NokiaSiemensNetworks
# FullName: Case
# Changes: 
# Date                Author           Comment
#==============================================================
#  May 31, 2013    y21chen(yong.5.chen@nsn.com)     Create file, implement feature
#==============================================================
class Case:
    '''
        * This is Case class
        * name String case name
        * reslut String case exec result
        * dsp String the dsp type
        * testLevel string test level
    '''
    name = ""
    result = ""
    dsp = ""
    testLevel = ""
    start = None
    end = None
    execTime = 0
    resultUrl = "#"

    #def __str__(self):
    #    return self.getName()
    '''
    this used for print the value of the address.
    due to clase always show pointer instead of value.
    '''
    def getName(self):
        return self.name
    def setName(self,name):
        self.name = name
    def getResult(self):
        return self.result
    def setResult(self,result):
        self.result = result
    def getDsp(self):
        return self.dsp
    def setDsp(self,dsp):
        self.dsp = dsp
    def getTestLevel(self):
        return self.testLevel
    def setTestLevel(self,testLevel):
        self.testLevel = testLevel 
    def getStart(self):
        return self.start
    def setStart(self,start):
        self.start = start
    def getEnd(self):
        return self.end
    def setEnd(self,end):
        self.end = end
    def getExecTime(self):
        return self.execTime
    def setExecTime(self,execTime):
        self.execTime = execTime
    def getResultUrl(self):
        return self.resultUrl
    def setResultUrl(self, resultUrl):
        self.resultUrl = resultUrl
        
        
    
        
        