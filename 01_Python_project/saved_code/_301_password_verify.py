#!/usr/bin/python
# -*- coding: utf-8 -*-

#verify input password

def varify_pwd(passwordList):
    valid = False
    count = 3
    while count > 0:
        input = raw_input("Enter password:")
        #check for valid password
        for eachPassword in passwordList:
            if input == eachPassword:
                valid = True
                print("password correct")
                break
        if not valid:    #(or valid == 0)
            print("invalid password!")
            count -= 1
            continue
        else:
            break

def main():
    passwordList = ['ZCSzcs001','zhouzhou', '  ']
    varify_pwd(passwordList)

if __name__ == '__main__':
    main()