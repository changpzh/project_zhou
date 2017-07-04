"""
**=============================================================
 * Copyright: 2012~2015
 * FullName:
 * Description:
 * Changes:
 *==============================================================
 * Date:
 * Author: changpzh
 * Comment:  create a file if file not exist in target location
 *    use "os" function, os.makedirs can create like c:/temp/temp2/
**==============================================================
"""
import os,sys

def filewrite(FilePath):
    if not os.path.isdir(os.path.dirname(FilePath)):
        os.makedirs(r'%s' % os.path.dirname(FilePath))
        f = open(FilePath, "w")
        f.close()

    try:
        f = open(FilePath, "a+")
        if len(f.readlines()) == 0:
            f.write("11111\n")
            f.write("22222\n")
            f.write("33333\n")
        elif len(f.readlines()) == 1:
            f.write("11111\n")
            f.write("22222\n")
        else:
            f.write("mmmmmm\n")
    finally:
        f.close()

def main():
        FilePath = "C:\\RL25\\NewReleaseInfo.ini"
        filewrite(FilePath)

if __name__ == '__main__':
    main()
