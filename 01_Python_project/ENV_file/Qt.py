#!/usr/bin/python
# -*- coding: UTF-8 -*-
class Qt:
    '''
        * This is Qt class
        * testLevel string test level
    '''
    testLevel = ""
    buildId = ""
    product = ""
    url = ""
    start = None
    end = None
    execTime = 0
    totalTestLine = 0
    execTestLine = 0
    failTestLine = 0
    passTestLine = 0
    score = 0
    result = ""
    testlineList = []
    jsonList = []

    def getTestLevel(self):
        return self.testLevel
    def setTestLevel(self,testLevel):
        self.testLevel = testLevel
    def getBuildId(self):
        return self.buildId
    def setBuildId(self, buildId):
        self.buildId = buildId
    def getProduct(self):
        return self.product
    def setProduct(self, product):
        self.product = product
    def getUrl(self):
        return self.url
    def setUrl(self, url):
        self.url = url
    def getStart(self):
        return self.start
    def setStart(self, start):
        self.start = start
    def getEnd(self):
        return self.end
    def setEnd(self, end):
        self.end = end
    def getExecTime(self):
        return self.execTime
    def setExecTime(self,execTime):
        self.execTime = execTime    
    def getTotalTestLine(self):
        return self.totalTestLine
    def setTotalTestLine(self, totalTestLine):
        self.totalTestLine = totalTestLine
    def getExecTestLine(self):
        return self.execTestLine
    def setExecTestLine(self, execTestLine):
        self.execTestLine = execTestLine
    def getFailTestLine(self):
        return self.failTestLine
    def setFailTestLine(self, failTestLine):
        self.failTestLine = failTestLine
    def getPassTestLine(self):
        return self.passTestLine
    def setPassTestLine(self, passTestLine):
        self.passTestLine = passTestLine
    def getScore(self):
        return self.score
    def setScore(self, score):
        self.score = score         
    def getResult(self):
        return self.result
    def setResult(self,result):
        self.result = result
    def getTestlineList(self):
        return self.testlineList
    def setTestlineList(self,testlineList):
        self.testlineList = testlineList
    def getJsonTestlineList(self):
        return self.jsonList
    def setJsonTestlineList(self,jsonList):
        self.jsonList = jsonList

    def print_zhou(self):
        print("self is: %s" % self.testLevel)
        
        