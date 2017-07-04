__author__ = 'changpzh'
#!/usr/bin/python
#-*- coding:utf-8 -*-

class person(object):
    '''
    include person's name, age and sex
    '''

    name = ""
    age = ""
    sex = ""

    def setName(self, name):
        self.name = name
    def getName(self):
        return self.name

    def setAge(self, age):
        self.age = age
    def getAge(self):
        return self.age

    def setSex(self, sex):
        self.sex = sex
    def getSex(self):
        return self.sex

    def greet(self):
        print("self.name address is: %s." % self)
        print("self.name is: \"%s\"." % self.name)

if __name__ == '__main__':
    foo = person()  #类实例化
    bar = person()

    foo.setName('zhou changping')
    foo.setAge('30')
    foo.setSex("male")

    bar.setName('test name')
    bar.setAge('36')
    bar.setSex("female")

    print("%s\'s age is %s and gender is %s" % (foo.getName(), foo.getAge(), foo.getSex()))
    print("%s\'s age is %s and gender is %s" % (bar.getName(), bar.getAge(), bar.getSex()))
    foo.greet()


