#!/usr/bin/python
# -*- coding: UTF-8 -*-
class Testline:
    '''
        * This is Testline class
        * testline String testline
        * reslut String testline exec result
        * dsp String the dsp type
        * testLevel string test level
    '''
    branch = ""
    testLevel = ""
    dsp = ""
    testline = ""
    shortName = ""
    description = ""
    start = None
    end = None
    execTime = 0
    result = ""
    caseList = []
    jsonList = []
    
    def getBranch(self):
        return self.branch
    def setBranch(self,branch):
        self.branch = branch
    def getTestLevel(self):
        return self.testLevel
    def setTestLevel(self,testLevel):
        self.testLevel = testLevel
    def getDsp(self):
        return self.dsp
    def setDsp(self,dsp):
        self.dsp = dsp
    def getTestline(self):
        return self.testline
    def setTestline(self,testline):
        self.testline = testline
    def getShortName(self):
        return self.shortName
    def setShortName(self,shortName):
        self.shortName = shortName
    def getDescription(self):
        return self.description
    def setDescription(self,description):
        self.description = description
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
    def getResult(self):
        return self.result
    def setResult(self,result):
        self.result = result
    def getCaseList(self):
        return self.caseList
    def setCaseList(self,caseList):
        self.caseList = caseList
    def getJsonCaseList(self):
        return self.jsonList
    def setJsonCaseList(self,jsonList):
        self.jsonList = jsonList
             
        
    
        
        