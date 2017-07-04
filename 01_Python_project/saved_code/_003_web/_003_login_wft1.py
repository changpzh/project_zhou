#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# #----------------------------------------------
#  Copyright: 2015~2025
#  Function :
#  Data: 2016/5/26 10:32
#  Author:changping.zhou@foxmail.com
# #----------------------------------------------
# #----------------------------------------------
'''
# import urllib, urllib2, cookielib, httplib  ---->python3
import urllib.request
import http.client
import http.cookies
import http.cookiejar
import urllib.parse
import gzip
import io,os

WFTUSER = "changpzh"
WFTPASWD = "ZCSzcs016"

proxy = "http://proxyconf.glb.nsn-net.net/proxy.pac"
RelLink = "https://wft.inside.nsn.com/ALL/builds/TL16A_ENB_0000_000162_000000#build=1"

class process_WFT():
    def __init__(self,username,passwd):
        self.username = username
        self.passwd = passwd
        self.debuglevel = 1

        http.client.HTTPConnection.debuglevel = self.debuglevel
        self.cookie = http.cookiejar.CookieJar()
        proxy_sp = urllib.request.ProxyHandler({'http': proxy})  #proxy
        cookie_sp= urllib.request.HTTPCookieProcessor(self.cookie) #cookie cookie_sp
        self.opener = urllib.request.build_opener(proxy_sp, cookie_sp, urllib.request.HTTPHandler)
        self.Login()

    def Login(self):
        login_url = "https://wam.inside.nsn.com/siteminderagent/forms/login.fcc"
        login_data = {
            'SMENC'     : "ISO-8859-1",
            'SMLOCALE'  : 'US-EN',
            'USER'      : self.username,
            'PASSWORD'  : self.passwd,
            'target'    : "-SM-HTTPS://wft.inside.nsn.com/",
            'smauthreason' : '0',
            'postpreservationdata' : '',
            'x'         : '0',
            'y'         : '0'
             }
        header = [('Host', 'wam.inside.nsn.com'),
                ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
                ('Accept-Encoding', 'gzip,deflate'),
                ('Accept-Language', 'zh-CN,zh;q=0.8'),
                # ('Cache-Control', 'max-age=0'),
                ('Connection', 'keep-alive'),
                # ('Content-Length', '152'),
                ('Content-Type', 'application/x-www-form-urlencoded'),
                # ('Cookie', 's_fid=43662AE4BAABE8CC-359EFDBFD9067563; ASPSESSIONIDQCRATSDA=EPAFIPNBGCIAHDJDENFFAHFK; '
                #            'BIGipServer~nsn-esp-nipf~login-lbesp.emea.nsn-net.net_80=2905638666.20480.0000'),
                # ('Origin', 'https://wam.inside.nsn.com'),
                ('Referer', 'https://wam.inside.nsn.com/siteminderagent/forms/common-login-silent-nokia_alu.asp'),
                # ('Upgrade-Insecure-Requests', '1'),
                ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'),
                ]
        login_data = urllib.parse.urlencode(login_data).encode('utf-8')
        # self.opener.addheaders = header # 问题点,可以不用这句，一样可用
        result = self.opener.open(login_url, data = login_data)
        temp = result.read()
        if ("Main Page" in temp.decode('utf-8')):
            print("""
            =================1, Login success!==========================
            """)
            return str(temp)
        else:
            raise("    Login failed!")
        # buf = io.StringIO(result.read().decode('utf-8'))
        # result = gzip.GzipFile(fileobj=buf)
        # if ("Main Page" in result.read()):
        #     print( "    Login success!")
        #     return str(result)
        # else:
        #     raise("    Login failed!")

    def FileWrite(self, FilePath, NewContent):
        if not os.path.isdir(os.path.dirname(os.path.split(FilePath)[0])):
            os.makedirs(r'%s' % os.path.dirname(FilePath))  # create new dir path if none exist.
        try:
            f = open(FilePath, 'wb')
            f.write(NewContent + "\n".encode('ascii'))
        finally:
            f.close()

    def GetContentOfJob(self, link):
        # self.opener.addheaders = self.header
        result = self.opener.open(link)
        temp = result.read()
        return  temp

    def timestamp():return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

if __name__ == '__main__':

    if WFTUSER != "":
        print( """
            =================1, LogIn to WFT==========================""")
        obj = process_WFT(WFTUSER, WFTPASWD)
    else:
        raise( "Pls fill in you WFT username and password.")

    print("""
            ================= 2, GetContentOfLink======================
            %s
            ===========================================================
            """ % RelLink)
    BuildContent = obj.GetContentOfJob(RelLink)
    print("""
            ================= 3, Content is ===========================
            %s
            ================= 3, Content end ==========================
            """ % BuildContent.decode('utf-8'))
    FilePath = os.path.join(os.getcwd(),"test.html")
    obj.FileWrite (FilePath, BuildContent) #把内容写到文件里面去
