"""
**=============================================================
 * Copyright: 2012~2015
 * FullName:
 * Description:
 * Changes:
 *==============================================================
 * Date:
 * Author: changpzh
 * Comment:  grep "Patten" From Local file
**==============================================================
"""

import re, os, sys
from third_get_content_from_web import *

FilePath = "D:\\Python_project\\test_file\\test.txt"
RE_VERSION = '\<title\>(.*)\<\/title\>'

def FileOpen(FilePath):
    """
    open FilePath file
    """
    if not os.path.isfile(FilePath):
        print "File %s does not exists" % (FilePath)
        return "File does not exists"
    else:
        try:
            f = open(FilePath, 'r')
            # **get a content of file**
            return f.readline()
        finally:
            f.close()
def test():
    File_Con = FileOpen(FilePath)
    grep_words = re.findall(r'%s' %RE_VERSION, File_Con)
    print"grep_words = %s" %(grep_words[0])
    print"grep_words2 = %s" %(grep_words)
    m = re.search(r'%s'%RE_VERSION, File_Con)
    if m is not None:
        print(m.group(1))

if __name__ == '__main__':
    test()

