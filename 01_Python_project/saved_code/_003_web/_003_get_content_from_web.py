"""
**=============================================================
 * Copyright: 2012~2015
 * FullName:
 * Description:
 * Changes:
 *==============================================================
 * Date:
 * Author: changpzh
 * Comment:  get content of URL, then write it to local file
**==============================================================
"""

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import urllib
import os
import stat

def open_url(url_path, prox):
    """
    open URL, return content
    """
    filehandle = urllib.urlopen(url_path,proxies=prox)
    return filehandle.readline()

def FileWrite(FilePath, NewContent):
    """
    write NewContent to FilePath file
    """
    try:
        f = open(FilePath, 'w') # open a file, create new one if not exist.
        f.write(NewContent)
    finally:
        f.close()

def FileOpen(FilePath):
    """
    open CurrentPath fle
    """
    if not os.path.isfile(FilePath):
        print("File %s does not exists" % (FilePath))
        return []
    else:
        try:
            f = open(FilePath, 'r')
            # **get a content of file**
            return f.readline()
        finally:
            f.close()

def main():
    url_path = "https://wft.inside.nsn.com/ALL/builds/TL16A_OM_0000_COMMON_366513_000000#build=0"

    FilePath = "D:\\Python_project\\test_file\\test.txt"
    filehandle = urllib.urlopen(url_path)
    FileWrite(FilePath, url_content)
    print("beforfinish")
    print (FileOpen(FilePath))
    print("finished")

if __name__ == '__main__':
    main()