__author__ = 'changpzh'
#!/usr/bin/python
#-*- coding:utf-8 -*-

class AddrBookEntry(object):                          #父类定义
    'address book entry class'
    count = 0  # 用于统计实例个数

    def __init__ (self, nm, ph):                        #定义构造器
        self.name = nm
        self.phone = ph
        AddrBookEntry.count += 1                        #增加一个实例
        print('Created instance for:', self.name)

    def __del__ (self):                                 #减少一个实例
        AddrBookEntry.count -= 1

    def howMany(self):                                  #返回count数
        return AddrBookEntry.count

    def update_Phone(self, newph):                   #定义方法,命名采用Python Style guide的Camel_Case方法
        self.phone = newph
        print('Updated phone# for:', self.name)

class EmplAddrBookEntry(AddrBookEntry):             # 创建子类，继承父类AddrBookEntry
    'Employee Address Book Entry class'
    def __init__(self, nm, ph, id, em):
        # AddrBookEntry.__init__(self,nm, ph)
        super(EmplAddrBookEntry, self).__init__(self, nm, ph) # super()使你不需要明确提供父类
        self.empid = id
        self.email = em

    def update_Email(self, newem):
        self.email = newem
        print('update email address for:', self.name)
