#-*- coding:UTF-8 -*-
import urllib, urllib2, cookielib, httplib
import re, sys, os, time, getopt
import binascii
import inspect
import gzip
from StringIO import StringIO
from datetime import datetime
from DBControl import *

__version__ = '5.0'
__wftversion__ = '2.0'
__author__ = 'sam.c.zhang@nsn.com'



global  qtresult
global  mail_content
global  qtlinks
global  qtreason
global  mail_to
global  mail_cc
global  mail_reply
global  mail_subject

#get wft user and password
##try:
##    sys.path.append('.')
##    from auth import Auth
##    authinfo = Auth().getauth()
##    WFTUSER = authinfo[0]
##    WFTPASWD = authinfo[1]
##except:
##    raise "Error! Can not get auth-info from auth file."
#WFTUSER = "hugao"
#WFTPASWD = "NSN32ght"
WFTUSER = "&9G1K=S,V"
WFTPASWD = "abc"

proxy = "http://proxyconf.glb.nsn-net.net/proxy.pac"
DB_NAME = "qtreport"
DB_IP = '10.140.90.13'
DB_USER = 'root'
DB_PASWD = 'btstest'

Debug = False
Force = False
FailBedTh = 2
FailTCTh = 4
QTReleaseResultMailTag = ['released', 'released with restrictions', 'not released']
QTReleaseResult = ['1', '3', '2']
QTFinalResult = ['Pass', 'PASS with restrictions', 'Fail']
alarmExclude = ['6203']

class Process_WFT:
    def __init__(self,username,passwd):
        self.username = username
        self.passwd = passwd
        self.debuglevel = 1
        httplib.HTTPConnection.debuglevel = self.debuglevel
        self.cookie = cookielib.CookieJar()
        proxy_sp = urllib2.ProxyHandler({'http': proxy})  #proxy
        cookie_sp= urllib2.HTTPCookieProcessor(self.cookie) #cookie cookie_sp
        self.opener = urllib2.build_opener(proxy_sp, cookie_sp, urllib2.HTTPSHandler)
        self.header = [('Host', 'wft.inside.nsn.com'),
                       ('User-Agent' ,'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN;\
rv:1.9.2.24) Gecko/20111103 Firefox/3.6.24 (.NET CLR 3.5.30729)'),
                       ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                       ('Accept-Language', 'zh-cn,zh;q=0.5'),
                       ('Accept-Encoding', 'gzip,deflate'),
                       ('Accept-Charset', 'GB2312,utf-8;q=0.7,*;q=0.7'),
                       ('Keep-Alive','115'),
                       ('Connection', 'keep-alive'),
                       ('Referer', 'https://wft.inside.nsn.com:8000/')
                       ]
        self.Login()


    def Login(self):
        login_url = "https://wam.inside.nokiasiemensnetworks.com/siteminderagent/forms/login.fcc"
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
        header = [     ('Host', 'wam.inside.nsn.com'),
                       ('User-Agent' ,'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN;\
rv:1.9.2.24) Gecko/20111103 Firefox/3.6.24 (.NET CLR 3.5.30729)'),
                       ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                       ('Accept-Language', 'zh-cn,zh;q=0.5'),
                       ('Accept-Encoding', 'gzip,deflate'),
                       ('Accept-Charset', 'GB2312,utf-8;q=0.7,*;q=0.7'),
                       ('Keep-Alive','115'),
                       ('Connection', 'keep-alive'),
                       ('Referer', 'https://wam.inside.nsn.com/siteminderagent/forms/common-login-silent2.asp'),
                       ('Content-Type','application/x-www-form-urlencoded')
                       ]
        login_data = urllib.urlencode(login_data)
        self.opener.addheaders = header
        result = self.opener.open(login_url, data = login_data)
        buf = StringIO(result.read())
        result = gzip.GzipFile(fileobj=buf)

        #if str(result.code)[0] == '2' and ("Profile &amp; Settings" in result.read()):
        #if ("Profile &amp; Settings" in result.read()):
        if ("Main Page" in result.read()):
            print "    Login success!"
            return str(result)
        else:
            print "Request failed! Httpstatus: %d" % result.code
            raise "    Login failed!"


    def SendDataToWFT(self, link):
        header = [     ('Host', 'wft.inside.nsn.com:8000'),
                       ('User-Agent' ,"Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0"),
                       ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                       ('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
                       ('Accept-Encoding', 'gzip,deflate'),
                       ('Connection', 'keep-alive'),
                       ('Referer', 'https://wft.inside.nsn.com:8000'),
                       ('Content-Type','application/x-www-form-urlencoded; charset=UTF-8'),
                       ('X-Requested-With', 'XMLHttpRequest')
                       ]
        req_data  = urllib.urlencode(_DATA_DIC[JOB])
        self.opener.addheaders = header
        urllib2.socket.setdefaulttimeout(60)
        try:
            result = self.opener.open(link, req_data)
            if str(result.code)[0] == '2':
                return str(result.read())
            else:
                print "Request failed! Httpstatus: %d" % result.code
        except:
            print sys.exc_info()

    def GetContentOfJob(self, link):
        self.opener.addheaders = self.header
        result = self.opener.open(link)
        if str(result.code)[0] == '2':
            buf = StringIO(result.read())
            gzipper = gzip.GzipFile(fileobj=buf)
            return gzipper.read()                
            #return str(result.read())
        else:
            print "Request failed! Httpstatus: %d" % result.code
        #self.cookie.save(ignore_discard=True, ignore_expires=True)

    def GetHrefOfRel(self, RelID, content, RelType = "Release"):
        if RelType.upper().strip() == "RELEASE":
            if JOB =="QT1":
                flag = "Release to I&amp;V"
            else:
                flag = " Release "
        elif RelType.upper().strip() == "UPDATE":
            flag = "Send Update"
        hrefpat = QtLink + "/release/\d+"
        lines = content.splitlines()
        for line in content.splitlines():
            if line.find(RelID) >= 0 :
                lindex = lines.index(line)
                for ln in lines[lindex: (lindex+5)]:
                    result = re.findall(hrefpat, ln, re.I)
                    if ln.find(flag) >=0 and result:
                        return result[0]

def GetTokenFromContent(content):
    lines = content.splitlines()
    lines.remove("")
    for line in lines:
        if line.find("authenticity_token") >=0:
            lindex  = lines.index(line)
            break
    for line in lines[lindex+1: lindex+3]:
        token =  re.findall("content=\"(.*)\" name=.*", line)
        if token:
            print "Token is: %s" %token[0]
            return token[0]

def timestamp():return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
class Redstdout:
    def __init__(self, logfile):
        self.f = logfile
        try:
            self.file_handle = open(self.f, 'w')
        except Exception, e:
            print e
            print "Log file create failed!"
    def write(self, s):
        self.file_handle.write(s)
    def __del__(self):
        self.file_handle.close()

def GetSWRelease(BuildID):
    #tmp_id = re.findall('LN[T,Z](\d)\.\d_ENB.*', BuildID, re.I)[0]
    #if int(tmp_id) == 1:
    #    SWRelease = "RL15"
    #    print "No such sw build!"
    #    sys.exit(5)
    #elif int(tmp_id) == 2:
        #CaseNeedCheck = [(item[0],item[1]) for item in CaseINFO if (int(item[2])==1 or int(item[2]) == 3)]
    #    SWRelease = "RL25"
    if 'LNT5.0' in BuildID:
        SWRelease = 'RL55'
    elif 'LNZ5.0' in BuildID:
        SWRelease = 'FZMRL55'
    elif 'TL15A_ENB_0000_000655' in BuildID:
        SWRelease = 'TL15A_OPENCPRI'
    elif 'TL15A' in BuildID:
        SWRelease = 'TL15A'
    elif 'TL16A' in BuildID:
        SWRelease = 'TL16A'
    elif 'TL16' in BuildID:
        SWRelease = 'TL16'
    elif 'TLF16A' in BuildID:
        SWRelease = 'TLF16A'
    elif 'TLF16' in BuildID:
        SWRelease = 'TLF16'
    elif 'TLF15A' in BuildID:
        SWRelease = 'TLF15A'
    elif 'LNT3.1' in BuildID:
        SWRelease = 'CMCCRL35'
    #elif 'LNT4.0_ENB_1311_109' in BuildID:
    elif 'LNT4.0' in BuildID: #and '_55' in BuildID:
        SWRelease = 'RL45'
#    elif 'LNT4.0' in BuildID:
#        SWRelease = 'CMCCRL45'
    elif int(tmp_id) == 3:
##        print "Not support RL35 now!!! Exit..."
##        sys.exit(1)
        #CaseNeedCheck = [(item[0],item[1]) for item in CaseINFO if (int(item[2])==2 or int(item[2]) == 3)]
        SWRelease = "RL35"
    else:
        print "The BuildID (%s) is not support now!" %BuildID
        sys.exit(1)
    return SWRelease

def GetTokenFromContent(content):
    lines = content.splitlines()
    lines.remove("")
    for line in lines:
        if line.find("authenticity_token") >=0:
            lindex  = lines.index(line)
            break
    for line in lines[lindex+1: lindex+3]:
        token =  re.findall("content=\"(.*)\" name=.*", line)
        if token:
            print "Token is: %s" %token[0]
            return token[0]

def create45head(old_table,config,result_type,qt_type):
    ######
    if config == 'RL45TD --- FSMF R3 MAIN – 2PIPE' or config == 'RL45EP --- FSMF R3 IR – Single Mode-2PIPE' or config == 'RL45TD --- FSIH FZHJ – 8PIPE':
        result_type = 'Not tested'
    ######    
    if qt_type != '':
        old_table = '<TABLE style="WIDTH: 718pt; BORDER-COLLAPSE: collapse; MARGIN-LEFT: -0.6pt" class=MsoNormalTable border=0 cellSpacing=0 cellPadding=0 width=957>\
<tr><td>Configuration</td><td>%s Result</td></tr>' % (qt_type)
    show_color = 'green'
    if result_type.upper() == 'FAIL':
        show_color = 'red'
    elif result_type.upper() != 'PASS':
        show_color = 'blue'
    old_table = old_table + '<tr><td>%s</td><td><font color="%s">%s</font></td></tr>' % (config,show_color,result_type)
    return old_table

def printhelp():
    print """
    =======================Processwft.exe(%s)==============================
    Usage:
        processwft.exe [qrltmuph][option]
    Where:
        -q   Mean the QT phase, can be QT1, QT2.
        -r   The SW package of your test. eg: LNT2.0_ENB_9308_066_00.
        -l   When it's open, will store all print info to a log file.
              If given , will work.
        -t   Send type, you can choise to send update or release to I&V
              can be update, release.
        -m   Send methord, preview or just send out.
              can be release , preview.
        -u   WFT Username, if given, default will not work.
        -p   WFT Password, if given, default will not work.
        -b   Failed test bed threshold. Default value is 2.
        -c   Failed case threshold. Default is 4.
        -f   Use torce to send out mail.
        -h   help.
    =========================================================================
""" %(__version__)


if __name__=='__main__':

    JOB = "QT1"
    BuildID = None
    opts, args = getopt.getopt(sys.argv[1:],"q:r:m:t:u:p:b:c:lhf")
    WFTUSER = binascii.a2b_uu(WFTUSER)

    path11=os.path.realpath(sys.argv[0])  
    if os.path.isfile(path11):  
        path11=os.path.dirname(path11)
    file_path = os.path.abspath(path11 + '/login.dat')
    print file_path
    try:
        file_obj = open(file_path, 'r')
	lines = file_obj.readline()
	WFTPASWD = binascii.a2b_uu(lines)
	file_obj.close()
    except IOError:
        raise Exception, "Open %s failed!" % (file_path)


    for k, v in opts:
        if '-q' == k:
            JOB = v.upper().strip()
        elif '-r' == k:
            BuildID = v.upper().strip()
        elif '-l' ==k:
            Debug = True
        elif '-f' ==k:
            Force = True
        elif '-t' ==k:
            SendType = v.strip()
        elif '-m' ==k:
            SendMethod = v.strip()
        elif '-u' ==k:
            WFTUSER = v.strip()
        elif '-p' ==k:
            WFTPASWD = v.strip()
        elif '-b' ==k:
            FailBedTh = int(v.strip())
        elif '-c' ==k:
            FailTCTh = int(v.strip())
        elif '-h' ==k:
            printhelp()
            sys.exit(1)
    if Debug and BuildID:
        LOG_FILE = '%s%s%s_WFT_%s.log' % (os.curdir, os.sep, BuildID, timestamp())
        sys.stdout = Redstdout(LOG_FILE)
    print "\n************************Start %s************************" %timestamp()

    print "==%s"%Force
    if not BuildID:
        try:
            BuildID = GetNewestBuildVersion(JOB).upper().strip()
        except:
            print "The newest BuildVersion have not appeared! Exit..."
            print
            sys.exit("Exit....")
    else:
        print "\n*******************Process %s build: %s**************" %(JOB, BuildID)

    if CheckMailStatus(BuildID, JOB) and SendMethod.upper() == 'RELEASE' and not Force:
        print "Have updated the %s WFT status on version: %s" %(JOB, BuildID)
        sys.exit(2)
    else:
        pass
    
    if JOB == "QT2" :
        if CheckMailStatus(BuildID, "QT1") and SendMethod.upper() == 'RELEASE':
            print "Have updated the %s WFT status on version: %s" %(JOB, BuildID)
            pass
        else:
            if SendMethod.upper() == 'PREVIEW':
                pass
            else:
                print "The QT1 have not send, so can not send QT2 on %s" %(BuildID)
                sys.exit(3)
            
    SWRelease = GetSWRelease(BuildID)
    print "**************************%s***************************" %SWRelease

##    if JOB == "QT2" and SWRelease == "RL25":
##        print "Exit... QT2 RL25 does't not send..."
##        sys.exit(3)
##        pass
    QTCaseResult = GetAllResult(BuildID, JOB)
    print "QTCaseResult: ", QTCaseResult

    appendWhere=""
    #appendWhere="and name not like '%%[FSIH FZND 2Pipe]%%' and name not like '%%[FSIH FZFF 8Pipe]%%' "
# init RL55 result
    conf55=[]
    ret55 = {}
    failCase55 = []
    passCase55 = []
    if SWRelease == "RL55" or SWRelease == "FZMRL55" or SWRelease == "TL15A" or SWRelease == "TLF15A" or SWRelease == "TL16" or SWRelease == "TL16A" or SWRelease == "TLF16" or SWRelease == "TLF16A" or SWRelease == "TL15A_OPENCPRI":
        for tc in QTCaseResult:
            if tc[6].strip() != "0":
                #print tc[0]
                case_config = (re.sub('.*\[','',tc[0],0)).replace(']','').strip()
                cn = re.sub('\[.*\]','',tc[0],0).strip()
                if case_config == cn:
                    case_config=''
                testRet = tc[1].upper().strip()
                print "case:%s result:%s config:%s " %(cn,testRet,case_config)
                if 'SWDL SEM' in cn.upper() and testRet=="FAIL":
                    appendWhere = "%s and name not like '%%[%s]%%' " %(appendWhere,case_config)
                if case_config!='':
                    if not cn in ret55:
                        ret55[cn]= {}
                    if (not ret55[cn].has_key(case_config)) or ("FAIL" in ret55[cn][case_config]):
                        if 'CPE Throught UDP' in cn:
                            ret55[cn][case_config] = testRet + '<br>'+ GetThroughput(BuildID, tc[5])
                        else:
                            ret55[cn][case_config] = testRet
                    if not case_config in conf55:
                        conf55.append(case_config)
                    if "FAIL" in testRet:
                        if cn not in passCase55 and cn not in failCase55:
                            failCase55.append(cn)
                        FailedTCNum = int(GetFailedTC(BuildID, int(tc[5])))
                        if FailedTCNum < FailTCTh -3 :
                            print "\t\n %s TC %s failed num(%s) less than FailTCTh(%s) ! \n\tExit.." %(SWRelease,tc[0], FailedTCNum, FailTCTh -3)
                            sys.exit(2)
                        else:
                            print "\t\n %s TC %s pass with restrictions num(%s) >= FailTCTh(%s) ! send mail.." %(SWRelease, tc[0], FailedTCNum, FailTCTh-3)
                    else:
                        if cn not in passCase55:
                            passCase55.append(cn)
                        if cn in failCase55:
                            failCase55.remove(cn)
                else:
                    print "Warning:\"%s\" can not found config info in case name" % tc[0]

    CaseInfo = GetCaseInfo(BuildID, SWRelease, JOB,appendWhere)
    if JOB == "QT2" and SWRelease == 'CMCCRL45//':
        print "Exit, CMCCRL45 don't test QT2"
        sys.exit(2)
    if not len(CaseInfo) == 0 :
        print "Exit, there is some case still not run. ", CaseInfo
        sys.exit(2)

    
    result_list = []
    FailedTCID = []
    sendMail = 0
    RL45_head = ''
    RL45_comp = ''
    RL45_ret = ''

    for tc in QTCaseResult:
        result_list.append(tc[1])
        if tc[6] != '0':
            if tc[1].upper().strip() == "FAIL":
                FailedTCID.append(int(tc[5]))

    finally_result = QTFinalResult[0]
    release_result = QTReleaseResult[0]
    release_mailtag = QTReleaseResultMailTag[0]



    if JOB == "QT1" and len(FailedTCID) ==0:
        color = "green"
        sendMail = 1
    elif JOB == "QT1" and SWRelease == "CMCCRL35" and len(FailedTCID) !=0:
        ALLCASEINFO = {}
        for tc in QTCaseResult:
            if tc[1].upper().strip() == "FAIL":
                FailedTCNum = int(GetFailedTC(BuildID, int(tc[5])))
                if FailedTCNum <= FailTCTh -1 :
                    print "\t\n CMCC TC %s failed num(%s) less than FailTCTh(%s) ! \n\tExit.." %(tc[0], FailedTCNum, FailTCTh)
                    sys.exit(2)
                if tc[0].endswith('[FZND]'):
                    tmp_name = tc[0].strip(' [FZND]')
                else:
                    tmp_name = tc[0]
                for ts in QTCaseResult:
                    if ts[0] == tmp_name :
                        if ts[1].upper().strip() == "FAIL":
                            FailedTCNum = int(GetFailedTC(BuildID, int(ts[5])))
                            if FailedTCNum >= FailTCTh -1 :
                                finally_result = QTFinalResult[2]
                                release_result = QTReleaseResult[2]
                                release_mailtag = QTReleaseResultMailTag[2]
                                color = "red"
                                sendMail = 1
                                break
                            else:
                                print "\t\n CMCC TC %s failed num(%s) less than FailTCTh(%s) ! \n\tExit.." %(ts[0], FailedTCNum, FailTCTh)
                                sys.exit(2)
                        else:
                            finally_result = QTFinalResult[1]
                            release_result = QTReleaseResult[1]
                            release_mailtag = QTReleaseResultMailTag[1]
                            color = "yellow"
                            sendMail = 1
                            continue    
                if color == 'red':
                    break
    elif JOB == "QT1" and SWRelease == "RL35" and len(FailedTCID) !=0:
        ALLCASEINFO = {}
        for tc in QTCaseResult:
            if tc[1].upper().strip() == "FAIL":
                FailedTCNum = int(GetFailedTC(BuildID, int(tc[5])))
                if FailedTCNum <= FailTCTh -3 :
                    print "\t\n CMCC TC %s failed num(%s) less than FailTCTh(%s) ! \n\tExit.." %(tc[0], FailedTCNum, FailTCTh)
                    sys.exit(2)
                finally_result = QTFinalResult[2]
                release_result = QTReleaseResult[2]
                release_mailtag = QTReleaseResultMailTag[2]
                color = "red"
                sendMail = 1
                break                  
    elif JOB == "QT1" and SWRelease == "RL45" and len(FailedTCID) !=0:
        ALLCASEINFO = {}
        for tc in QTCaseResult:
            if tc[1].upper().strip() == "FAIL" and tc[6].strip() != "0":
                FailedTCNum = int(GetFailedTC(BuildID, int(tc[5])))
                if FailedTCNum <= FailTCTh -3 :
                    print "\t\n RL45 TC %s failed num(%s) less than FailTCTh(%s) ! \n\tExit.." %(tc[0], FailedTCNum, FailTCTh -3)
                    sys.exit(2)
                else:
                    print "\t\n RL45 TC %s pass with restrictions num(%s) > FailTCTh(%s) ! send mail.." %(tc[0], FailedTCNum, FailTCTh-3)
                if tc[0].endswith('[IR 2Pipe]'):
                    RL45_comp=RL45_comp + '1'
                elif tc[0].endswith('[IR 8Pipe]'):
                    RL45_comp=RL45_comp + '2'
                elif tc[0].endswith('[FSIH 8Pipe]'):
                    RL45_comp=RL45_comp + '3'
                elif tc[0].endswith('[2Pipe]'):
                    RL45_comp=RL45_comp + '4'
                elif tc[0].endswith('[8Pipe]'):
                    RL45_comp=RL45_comp + '5'
                else:
                    pass
        if RL45_comp.find('1')<0 or RL45_comp.find('2')<0 or RL45_comp.find('3')<0 or RL45_comp.find('4')<0 or RL45_comp.find('5')<0:
            finally_result = QTFinalResult[1]
            release_result = QTReleaseResult[1]
            release_mailtag = QTReleaseResultMailTag[1]
            color = "blue"
            sendMail = 1
        else:
            finally_result = QTFinalResult[2]
            release_result = QTReleaseResult[2]
            release_mailtag = QTReleaseResultMailTag[2]
            color = "red"
            sendMail = 1
    elif JOB == "QT1" and (SWRelease == "RL55" or SWRelease == "FZMRL55" or SWRelease == "TL15A" or SWRelease == "TLF15A" or SWRelease == "TL16" or SWRelease == "TL16A" or SWRelease == "TLF16" or SWRelease == "TLF16A" or SWRelease=="TL15A_OPENCPRI") and len(FailedTCID) !=0:
        if len(failCase55)<1:
            finally_result = QTFinalResult[1]
            release_result = QTReleaseResult[1]
            release_mailtag = QTReleaseResultMailTag[1]
            color = "blue"
            sendMail = 1
        else:
            finally_result = QTFinalResult[2]
            release_result = QTReleaseResult[2]
            release_mailtag = QTReleaseResultMailTag[2]
            color = "red"
            sendMail = 1
    elif JOB == "QT1" and len(FailedTCID) !=0 and SWRelease != "CMCCRL35" and SWRelease !=  "RL35" and SWRelease !=  "RL45" and SWRelease !=  "RL55" and SWRelease !=  "FZMRL55" :
        for case in FailedTCID:
            print "**FailedTCID is : ", FailedTCID
            print "**Will check if it meet the failed criterion..."
            TCFailedTestBed = int(GetFailedTestBed(BuildID, int(case)))
            print "**TCFailedTestBed number is : ", TCFailedTestBed
            print "**The FailBedTh is: ", FailBedTh
            if  TCFailedTestBed>= FailBedTh:
                FailedTCNum = int(GetFailedTC(BuildID, int(case)))
                print "**FailedTCNum is : ", FailedTCNum
                print "**The FailedTCTh is : ", FailTCTh
                if FailedTCNum >= 3:
                    print "TCID: %s, This is a failed TC..." % case
                    finally_result = QTFinalResult[2]
                    release_result = QTReleaseResult[2]
                    release_mailtag = QTReleaseResultMailTag[2]
                    color = "red"
                    sendMail = 1
                
    if JOB == "QT2" and len(FailedTCID) ==0:
        finally_result = QTFinalResult[0]
        release_result = "released"#QTReleaseResult[0]
        release_mailtag = QTReleaseResultMailTag[0]
        color = "green"
        sendMail = 1
        if SWRelease == "RL45":
            #RL45_head = create45head(RL45_head,'RL45EP --- FSMF R3 IR – Single Mode-2PIPE','Pass', JOB)
            #RL45_head = create45head(RL45_head,'RL45EP --- FSMF R3 IR – Dual Mode – 8PIPE','Pass',JOB)
            #RL45_head = create45head(RL45_head,'RL45EP --- FSIH IR – 8PIPE','Pass','')
            RL45_head = create45head(RL45_head,'RL45TD --- FSMF R3 MAIN – 8PIPE','Pass','')
            #RL45_head = create45head(RL45_head,'RL45TD --- FSIH FZHJ – 8PIPE','Pass','')
            RL45_head = """<span style="font-size: 24px;">The QT2 result on RL45 EP: </span><span style="color: Green; font-size: 24px;">Pass</span>
<span style="font-size: 24px;">The QT2 result on RL45 TD: </span><span style="color: Green; font-size: 24px;">Pass</span>
""" + RL45_head
     
    if sendMail == 0 and JOB == "QT1":
        print "Not meet the send mail criterion, exit..."
        sys.exit(2)
    print "Have meet the send mail criterion, send mail next..."
    if JOB == 'QT1':
        QtLink = "https://wft.inside.nsn.com:8000/quicktests"
    elif JOB == 'QT2':
        QtLink = "https://wft.inside.nsn.com:8000/quicktest2s"

    RelLink = "%s/%s/release" % (QtLink, BuildID)

    Alarm_Case = GetAlarmView(BuildID)
    
    ALL_CASE_ALARM = {}
    for tc in Alarm_Case:
        ALL_CASE_ALARM[tc[0]] = []
    for tc in Alarm_Case:
        atc_name = tc[0]
        alarm_id = []
        for am in tc[1].split('|')[1:]:
            res = re.match(".*\((\d+)\).*", am)
            if res:
                alarm_id.append(res.groups()[0])
        for ai in alarm_id:
            if ai not in ALL_CASE_ALARM[tc[0]]:
                ALL_CASE_ALARM[tc[0]].append(ai)
                
    if JOB == "QT1":            
        ALL_ALARMS_ID = []
        for alm in ALL_CASE_ALARM.values():
             ALL_ALARMS_ID.extend(alm)
        ALL_ALARMS_ID = list(set(ALL_ALARMS_ID))
        for ex in alarmExclude:
            if ex in ALL_ALARMS_ID:
                ALL_ALARMS_ID.remove(ex)
        if ALL_ALARMS_ID and finally_result == QTFinalResult[0]:
            finally_result = QTFinalResult[1]
            release_mailtag = QTReleaseResultMailTag[1]
            release_result = QTReleaseResult[1]
        if SWRelease == "RL45":
            for alm in ALL_CASE_ALARM:
                 #print "*************%s,%s" % (alm,ALL_CASE_ALARM[alm])
                 for alarmID in ALL_CASE_ALARM[alm]:
                     if alarmID not in alarmExclude:
                        if alm.endswith('[IR 2Pipe]'):
                            RL45_ret=RL45_ret + '1'
                        elif alm.endswith('[IR 8Pipe]'):
                            RL45_ret=RL45_ret + '2'
                        elif alm.endswith('[FSIH 8Pipe]'):
                            RL45_ret=RL45_ret + '3'
                        elif alm.endswith('[2Pipe]'):
                            RL45_ret=RL45_ret + '4'
                        elif alm.endswith('[8Pipe]'):
                            RL45_ret=RL45_ret + '5'
                        else:
                            pass
                        break

    if SWRelease == "RL45":
        tmp_ret = ''
        ep_ret = 0
        td_ret = 0

        if RL45_comp.find('1')<0 and RL45_ret.find('1')<0:
            tmp_ret = 'Pass'
        elif RL45_comp.find('1')<0:
            tmp_ret = 'Pass with restrictions'
            ep_ret += 1
        else:
            tmp_ret = 'Fail'
            ep_ret += 2
        #RL45_head = create45head(RL45_head,'RL45EP --- FSMF R3 IR – Single Mode-2PIPE',tmp_ret, JOB)

        if RL45_comp.find('2')<0 and RL45_ret.find('2')<0:
            tmp_ret = 'Pass'
        elif RL45_comp.find('2')<0:
            tmp_ret = 'Pass with restrictions'
            ep_ret += 1
        else:
            tmp_ret = 'Fail'
            ep_ret += 2
        #RL45_head = create45head(RL45_head,'RL45EP --- FSMF R3 IR – Dual Mode – 8PIPE',tmp_ret,JOB)

        if RL45_comp.find('4')<0 and RL45_ret.find('4')<0:
            tmp_ret = 'Pass'
        elif RL45_comp.find('4')<0:
            tmp_ret = 'Pass with restrictions'
            ep_ret += 1
        else:
            tmp_ret = 'Fail'
            ep_ret += 2
        tmp_ret='Not test'
        #RL45_head = create45head(RL45_head,'RL45EP --- FSIH IR – 8PIPE',tmp_ret,'')

        if RL45_comp.find('5')<0 and RL45_ret.find('5')<0:
            tmp_ret = 'Pass'
        elif RL45_comp.find('5')<0:
            tmp_ret = 'Pass with restrictions'
            td_ret += 1
        else:
            tmp_ret = 'Fail'
            td_ret += 2
        RL45_head = create45head(RL45_head,'RL45TD --- FSMF R3 MAIN – 8PIPE',tmp_ret,'')

        if RL45_comp.find('3')<0 and RL45_ret.find('3')<0:
            tmp_ret = 'Pass'
        elif RL45_comp.find('3')<0:
            tmp_ret = 'Pass with restrictions'
            td_ret += 1
        else:
            tmp_ret = 'Fail'
            td_ret += 2
        #RL45_head = create45head(RL45_head,'RL45TD --- FSIH FZHJ – 8PIPE',tmp_ret,'')
        
        ep_tmp=""
        td_tmp=""
        if ep_ret == 0:
            #ep_tmp = """<span style="font-size: 24px;">The result on RL45 EP: </span><span style="color: Green; font-size: 24px;">Pass</span><BR>"""
            pass
        elif ep_ret<6:
            #ep_tmp = """<span style="font-size: 24px;">The result on RL45 EP: </span><span style="color: blue; font-size: 24px;">Pass with restrictions</span><BR>"""
            pass
        else:
            #ep_tmp = """<span style="font-size: 24px;">The result on RL45 EP: </span><span style="color: Red; font-size: 24px;">Fail</span><BR>"""
            pass
        if td_ret == 0:
            td_tmp = """<span style="font-size: 24px;">The result on RL45 TD: </span><span style="color: Green; font-size: 24px;">Pass</span><BR>"""
        elif td_ret<4:
            td_tmp = """<span style="font-size: 24px;">The result on RL45 TD: </span><span style="color: blue; font-size: 24px;">Pass with restrictions</span><BR>"""
        else:
            td_tmp = """<span style="font-size: 24px;">The result on RL45 TD: </span><span style="color: Red; font-size: 24px;">Fail</span><BR>"""
        RL45_head = ep_tmp + td_tmp + RL45_head

    #define mail template
    qtlinks = ""
    #Reason for "NOT RELEASED" or "RELEASED WITH RESTRICTIONS" (ProntoID)
    qtreason = ""

    mail_to = """coo-ra-bts-td-lte-build-release@mlist.emea.nsn-intra.net;i_ext_lte_tdd_qt_gms@internal.nsn.com; \
i_ext_mbb_global_lte_tdd_test_all@internal.nsn.com; I_EXT_MBB_LTE_CPD_CI_HZ@internal.nsn.com; I_MBB_SM_RACS_BUILD_NOTIFICATION_LA20@internal.nsn.com;"""
    if SWRelease == "FZMRL55":
        mail_to += """I_MBB_SM_RACS_BUILD_NOTIFICATION_LA20@internal.nsn.com;I_FZM_SCM@internal.nsn.com;I_EXT_FZM_DEV_IV@internal.nsn.com;\
I_FZM_QUICKTEST@internal.nsn.com;petr.kacena@internal.nsn.com"""
    
    #mail_to = "sam.c.zhang@nsn.com"
    mail_cc = ''
    
    #mail_reply = "I_EXT_MBB_LTE_CPD_CI_HZ_GMS DG <I_EXT_MBB_LTE_CPD_CI_HZ@internal.nsn.com>;"
    mail_reply = "I_EXT_MBB_LTE_CPD_CI_HZ <I_EXT_MBB_LTE_CPD_CI_HZ@internal.nsn.com>;"
    #mail_reply = "I_EXT_TDLTE_CB_SCM_GMS DG <I_EXT_TDLTE_CB_SCM_GMS@internal.nsn.com>;"
    #mail_subject = "%s report sw build %s %s [TA auto send]" \
       #            %(JOB, BuildID, release_result)
    FBTAG = BuildID.split('_')[2][:2]+'.'+BuildID.split('_')[2][2:]
    if JOB == "QT1":
        mail_subject = "RELEASENOTE LTE eNB TDD FB%s build %s %s /QT Phase1 [TA auto send]" %(FBTAG, BuildID, release_mailtag)
        if "2.1" in BuildID:
            mail_subject = "RELEASENOTE LTE eNB TDD FB%s RL25_Sprint build %s %s /QT Phase1 [TA auto send]" %(FBTAG, BuildID, release_mailtag)
        elif "3.1" in BuildID:
            mail_subject = "RELEASENOTE LTE eNB TDD FB%s CMCC build %s %s /QT Phase1 [TA auto send]" %(FBTAG, BuildID, release_mailtag)
        elif SWRelease == "FZMRL55":
            mail_subject = "RELEASENOTE LTE eNB TDD FB%s_FZM build %s %s /QT Phase1 [TA auto send]" %(FBTAG, BuildID, release_mailtag)
        elif SWRelease == "TLF15A":
            mail_subject = "RELEASENOTE LTE eNB TDD FZM build %s %s /QT Phase1 [TA auto send]" %( BuildID, release_mailtag)
        elif SWRelease == "TL15A":
            mail_subject = "RELEASENOTE LTE eNB TDD build %s %s /QT Phase1 [TA auto send]" %( BuildID, release_mailtag)
        elif SWRelease == "TL16" or SWRelease == "TL16A" :
            mail_subject = "RELEASENOTE LTE eNB TDD build %s %s /QT Phase1 [TA auto send]" %( BuildID, release_mailtag)
        elif SWRelease == "TLF16" or SWRelease == "TLF16A" :
            mail_subject = "RELEASENOTE LTE eNB TDD FZM build %s %s /QT Phase1 [TA auto send]" %( BuildID, release_mailtag)
        elif SWRelease == "TL15A_OPENCPRI":
            mail_subject = "RELEASENOTE LTE eNB TDD OPEN CPRI build %s %s /QT Phase1 [TA auto send]" %( BuildID, release_mailtag)
        elif SWRelease == "RL55":
            mail_subject = "RELEASENOTE LTE eNB TDD LNT5.0_1.0 build %s %s /QT Phase1 [TA auto send]" %( BuildID, release_mailtag)
    if JOB == "QT2":
        mail_subject = "RELEASENOTE LTE eNB TDD FB%s build %s %s /QT Phase2 [TA auto send]" %(FBTAG, BuildID, release_mailtag)
        if "2.1" in BuildID:
            mail_subject = "RELEASENOTE LTE eNB TDD FB%s RL25_Sprint build %s %s /QT Phase2 [TA auto send]" %(FBTAG, BuildID, release_mailtag)
        elif "3.1" in BuildID:
            mail_subject = "RELEASENOTE LTE eNB TDD FB%s CMCC build %s %s /QT Phase2 [TA auto send]" %(FBTAG, BuildID, release_mailtag)
        elif SWRelease == "FZMRL55":
            mail_subject = "RELEASENOTE LTE eNB TDD FB%s_FZM build %s %s /QT Phase2 [TA auto send]" %(FBTAG, BuildID, release_mailtag)
        elif SWRelease == "TL16" or SWRelease == "TL16A" :
            mail_subject = "RELEASENOTE LTE eNB TDD build %s %s /QT Phase2 [TA auto send]" %( BuildID, release_mailtag)
        elif SWRelease == "TLF16" or SWRelease == "TLF16A" :
            mail_subject = "RELEASENOTE LTE eNB TDD FZM build %s %s /QT Phase2 [TA auto send]" %( BuildID, release_mailtag)
        elif SWRelease == "TL15A_OPENCPRI":
            mail_subject = "RELEASENOTE LTE eNB TDD OPEN CPRI build %s %s /QT Phase2 [TA auto send]" %( BuildID, release_mailtag)
        elif SWRelease == "TLF15A":
            mail_subject = "RELEASENOTE LTE eNB TDD FZM build %s %s /QT Phase2 [TA auto send]" %( BuildID, release_mailtag)
        elif SWRelease == "TL15A":
            mail_subject = "RELEASENOTE LTE eNB TDD build %s %s /QT Phase2 [TA auto send]" %( BuildID, release_mailtag)
        elif SWRelease == "RL55":
            mail_subject = "RELEASENOTE LTE eNB TDD LNT5.0_1.0 build %s %s /QT Phase2 [TA auto send]" %( BuildID, release_mailtag)

    
    mail_content = """
<style>
span{
    font-size:9.0pt; 
    font-family:'Calibri','Arial','sans-serif'; 
    }
</style>
<P><SPAN>Hello All,</SPAN></P>
<P><I><SPAN>
(The mail was sent automatically by TA tools. The failure reason will be updated by manual
execution if the release is not passed or passed with restrictions )
</SPAN></I></P>
<P><span>The %s for %s &nbsp;was performed by TA tools.</span></p>
<P><b><span>The %s result : <font color=%s>%s</font></span></b></p>
""" % (JOB, BuildID, JOB, color, finally_result)

    if SWRelease == "RL45":
        mail_content=mail_content + RL45_head + '</table><br>'
        
    mail_content = mail_content + """
<P><i><u><b><span>QT Execution Environments</span></b></u></i></p>
<p style="MARGIN-LEFT: 15pt"><span>
"""

    cpe_type = "CPE DeMing" if SWRelease == 'CMCCRL35' or SWRelease == 'RL45' else "CPE NSN 7210"
    cpe_type = cpe_type if SWRelease != 'CMCCRL45' else "FSIH: CPE NSN 7210 | FSMF: CPE DeMing"
    rru_type = "FZND/FZFF" if SWRelease == 'CMCCRL35' else "FZHA(A102)"
    if JOB == "QT1":
        CellFlag = ""
    else:
        CellFlag = "3*"
    if SWRelease == 'FZMRL55':
        mail_content += """
QT1 eNB1:FWHE(A101) | 2pipe | 20MHz | Dynamic open Loop Mimo | 2/7<BR>
QT1 eNB2:FWHD(X22)  | 4pipe | 20MHz | Dynamic open Loop Mimo | 2/7<BR>
QT2 eNB4:FWHD(X22) | 4pipe | 20MHz | Dynamic open Loop Mimo | 2/7<BR>
UE: <SPAN style="COLOR: #1f497d">CPE DeMing
</SPAN></SPAN></P>""" 
    elif SWRelease == 'TL16':
        mail_content += """
1. TL16 FSMr3 OBASI 4 Pipe QT1: ConfID =T1-4TX-4RX: RRU Type: FZHA ; QT2 : ConfID=T111-4TX-4RX Type: FZHA<BR>
2. TL16 FSIH NOKIA CPRI 8 Pipe QT1: ConfID = T2-8TX-8RX: RRU Type: FZHM <BR>
3. TL16 FSIH OBASI 8 Pipe QT1: ConfID = T1- -8TX-8RX: RRU Type: FZHJ; QT2: ConfID = T1118 TX-8RX: RRU Type: FZHJ <BR>
4. TL16 FSIH DM 1 Pipe QT1: ConfID = T2-1TX-1RX: RRU Type: FZNN <BR>
5. TL16 2 Pipe CPRI SM QT1: ConfID = T1- -2TX-2RX: BBU:FSIH RRU Type: FZND ; QT2: ConfID = T111 2TX-2RX: BBU:FSMF RRU Type: FZND<BR>
UE: <SPAN style="COLOR: #1f497d">CPE DeMing
</SPAN></SPAN></P>""" 
    elif SWRelease == 'TL16A':
        mail_content += """
1. TL16A FSMr3-DM FZFF 8Pipe 1Cell QT1 <BR>
2. TL16A FSIH FZHM 8Pipe 1Cell QT1+QT2 <BR>
3. TL16A FSIH FZHJ 8Pipe 1Cell QT1+QT2 <BR>
4. TL16A FSIH FZHM+FZFF 8Pipe 2Cell QT1 <BR>
5. TL16A FSIH-DM FZNN 1Pipe QT1 <BR>
6. TL16A FSIH ALU CPRI UZNA 2Pipe QT1 <BR>
7. TL16A ASMI FZHM 8pipe x31 8pipe QT1+QT2 <BR>
UE: <SPAN style="COLOR: #1f497d">CPE DeMing
</SPAN></SPAN></P>""" 
    elif SWRelease == 'TLF16':
        mail_content += """
QT1 eNB1:FWNC(A101)single cell | 2pipe | 20MHz | Dynamic open Loop Mimo | 2/7<BR>
QT2 eNB2:FWNC(A101)dual cell  | 2pipe | 20MHz | Dynamic open Loop Mimo | 2/7<BR>
UE: <SPAN style="COLOR: #1f497d">CPE DeMing
</SPAN></SPAN></P>""" 
    elif SWRelease == 'TLF16A':
        mail_content += """
QT1 eNB1:FWHE(A101)single cell | 2pipe | 20MHz | Dynamic open Loop Mimo | 2/7<BR>
QT2 eNB2:FWHE(A101)dual cell  | 2pipe | 20MHz | Dynamic open Loop Mimo | 2/7<BR>
UE: <SPAN style="COLOR: #1f497d">CPE DeMing
</SPAN></SPAN></P>""" 
    elif SWRelease == 'TL15A_OPENCPRI':
        mail_content += """
QT1 eNB1:FZNG(A101)single cell | 2pipe | 20MHz | Dynamic open Loop Mimo | 2/7<BR>
UE: <SPAN style="COLOR: #1f497d">CPE DeMing
</SPAN></SPAN></P>""" 
    elif SWRelease == 'TLF15A':
        mail_content += """
QT1 eNB1:FWHE(A101) | 2pipe | 20MHz | Dynamic open Loop Mimo | 2/7<BR>
QT2 eNB3:FWHE(X22)  | 2pipe | 20MHz | Dynamic open Loop Mimo | 2/7<BR>
UE: <SPAN style="COLOR: #1f497d">CPE DeMing
</SPAN></SPAN></P>""" 
    elif SWRelease == "RL35":
        mail_content += """
eNB: FSMF(X41) + 3*FZHA(A102) | (8pipe)<BR>
Config: 20MHz | Dynamic Open Loop MIMO | 1,7<BR>
UE: <SPAN style="COLOR: #1f497d">%s
</SPAN></SPAN></P>""" % (cpe_type)
    elif SWRelease == "CMCCRL45":
        mail_content += """
eNB1: FSIH(X32) + 3*FZHJ(X11) | (8pipe)<BR>
Config: 20MHz | Dynamic Open Loop MIMO | 1,7<BR>
eNB2: FSMF(A101) + 3*FZHA(A103) | (8pipe)<BR>
Config: 20MHz | Dynamic Open Loop MIMO | 1,7<BR>
UE: <SPAN style="COLOR: #1f497d">%s
</SPAN></SPAN></P>""" % (cpe_type)
    elif SWRelease == "RL45":
        mail_content += """
<font color = blue>eNB1</font>: FSIH(A101) + 1*FZHJ(A101) | (8pipe)<BR>
Config: 20MHz | Dynamic Open Loop MIMO | 1,7<BR>
<font color = blue></font> <BR>
UE: %s <BR>"""% (cpe_type)
    elif SWRelease == "RL55" and JOB == "QT1":
        mail_content +="""
1. RL55 FSIH 8 Pipe QT1: ConfID = T1-L-145-8TX-8RX:1L,RRU Type: FZHJ; QT2: ConfID = T111-x-42-8TX-8RX:1+1+1,RRU Type: FZHJ <br>
2. RL55 FSIH 8 Pipe QT1: ConfID = T1-x-30-8TX-8RX: 1 L, RRU Type: FZFF; QT2: ConfID = T111-x-42-8TX-8RX:1+1+1,RRU Type: FZFF <br>
3. RL55 DM QT1: FSMr3 8 Pipe ConfID = T1-x-30-8TX-8RX: 1 L, RRU Type: FZFF; QT2: FSIH 8pipe ConfID = T111-x-42-8TX-8RX:1+1+1,RRU Type: FZFF <br>
"""
    elif SWRelease == "TL15A"and JOB == "QT1":
        mail_content +="""
1.TL15A FSMr3 8 Pipe QT1: ConfID =T1-x-52-8TX-8RX: 1 I, RRU Type: FZHA; QT2: ConfID = T111-x-42-8TX-8RX: 1+1+1 L, RRU Type: FZHA <br>
2.TL15A FSMr3 2 Pipe QT1: ConfID = T1-x-30-2TX-2RX: 1 L, RRU Type: FZND;QT2: ConfID = T111-x-42-2TX-2RX: 1+1+1 L, RRU Type: FZND<br>
3.TL15A FSIH 8 Pipe QT1: ConfID = T1-L-145-8TX-8RX:1L,RRU Type: FZFF; QT2: ConfID = T111-x-42-8TX-8RX:1+1+1,RRU Type: FZFF<br>
4.TL15A FSIH 8 Pipe QT1: ConfID = T111-8TX-8RX: 1+1+1 L, RRU Type: FZHJ <br>
5.TL15A FSMr3 8 Pipe DM QT1: ConfID = T1-8TX-8RX: 1 L, RRU Type: FZFF<br>
"""
    elif SWRelease == "TL15A"and JOB == "QT2":
        mail_content +="""
1.TL15A FSMr3 8 Pipe QT1: ConfID =T1-x-52-8TX-8RX: 1 I, RRU Type: FZHA; QT2: ConfID = T111-x-42-8TX-8RX: 1+1+1 L, RRU Type: FZHA <br>
2.TL15A FSMr3 2 Pipe QT1: ConfID = T1-x-30-2TX-2RX: 1 L, RRU Type: FZND;QT2: ConfID = T111-x-42-2TX-2RX: 1+1+1 L, RRU Type: FZND<br>
3.TL15A FSIH 8 Pipe QT1: ConfID = T1-L-145-8TX-8RX:1L,RRU Type: FZFF; QT2: ConfID = T111-x-42-8TX-8RX:1+1+1,RRU Type: FZFF<br>
4.TL15A FSIH 8 Pipe QT1: ConfID = T111-8TX-8RX: 1+1+1 L, RRU Type: FZHJ <br>
5.TL15A FSMr3 8 Pipe DM QT1: ConfID = T1-8TX-8RX: 1 L, RRU Type: FZFF<br>
"""
    elif SWRelease == "RL55" and JOB == "QT2":
        mail_content +="""
1. RL55 FSMF  8 Pipe QT1: ConfID = T1-x-30-8TX-8RX: 1 L, RRU Type: FZFD; <br>
"""
    else:
        mail_content += """
eNB: FSMF(X41) + %s%s<BR>
Config: 20MHz | Dynamic Open Loop MIMO | 1,7<BR>
UE: <SPAN style="COLOR: #1f497d">%s
</SPAN></SPAN></P>""" % (CellFlag, rru_type, cpe_type)
    

    mail_content += """
<P><i><u><b><span>Notes for the release:</SPAN></b></u></i></p>
1.<span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Please see the release notes</SPAN><br>
2.<span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Special notes will be added manually if needed</SPAN><br>
"""
    if SWRelease == 'RL55':
        mail_content += """<br><span style='color:black'>
&nbsp;&nbsp;&nbsp;&nbsp;<b>More info to link : </b><a href="http://hzling21.china.nsn-net.net:8080/job/CB_TDD_RL55_P8/">http://hzling21.china.nsn-net.net:8080/job/CB_TDD_RL55_P8/</a><br>
</span>"""
    if SWRelease == 'TL15A':
        mail_content += """<br><span style='color:black'>
&nbsp;&nbsp;&nbsp;&nbsp;<b>More info to link : </b><a href="http://hzling21.china.nsn-net.net:8080/job/CB_TDD_TL15A/">http://hzling21.china.nsn-net.net:8080/job/CB_TDD_TL15A/</a><br>
</span>"""
    if SWRelease == 'TL16':
        mail_content += """<br><span style='color:black'>
&nbsp;&nbsp;&nbsp;&nbsp;<b>More info to link : </b><a href="http://hzling21.china.nsn-net.net:8080/job/CB_TDD_TL16/">http://hzling21.china.nsn-net.net:8080/job/CB_TDD_TL16/</a><br>
&nbsp;&nbsp;&nbsp;&nbsp;<font color='red'><b>Know issue : </b></font><a href="http://hzlinb01.china.nsn-net.net:8000/qt/issue/?raised_time_from=2013-01-01&raised_time_to=2016-09-29&status=NEW&sc_name=&analyze_reason=&priority=&days_to_fix_from=&days_to_fix_to=&release=TL16&submit=Query/">URL link</a><br>
</span>"""
    if SWRelease == 'TL16A':
        mail_content += """<br><span style='color:black'>
&nbsp;&nbsp;&nbsp;&nbsp;<b>More info to link : </b><a href="http://hzling21.china.nsn-net.net:8080/job/CB_TDD_TL16A/">http://hzling21.china.nsn-net.net:8080/job/CB_TDD_TL16A/</a><br>
&nbsp;&nbsp;&nbsp;&nbsp;<font color='red'><b>Know issue : </b></font><a href="http://hzlinb01.china.nsn-net.net:8000/qt/issue/?raised_time_from=2016-04-27&raised_time_to=2017-09-29&status=NEW&sc_name=&analyze_reason=&priority=&days_to_fix_from=&days_to_fix_to=&release=TL16&submit=Query/">URL link</a><br>
</span>"""
    if SWRelease == 'TLF16':
        mail_content += """<br><span style='color:black'>
&nbsp;&nbsp;&nbsp;&nbsp;<b>More info to link : </b><a href="http://wrlinb08.emea.nsn-net.net:8080/view/FZM_Branch_QT/job/TLF16_QTp1_FZM1645_163/">http://wrlinb08.emea.nsn-net.net:8080/view/FZM_Branch_QT/job/TLF16_QTp1_FZM1645_163/</a><br>
</span>"""
    if SWRelease == 'TLF16A':
        mail_content += """<br><span style='color:black'>
&nbsp;&nbsp;&nbsp;&nbsp;<b>More info to link : </b><a href="http://ullteb40.emea.nsn-net.net:9093/view/FZM_Branch_QT/">http://ullteb40.emea.nsn-net.net:9093/view/FZM_Branch_QT/</a><br>
</span>"""
    if SWRelease == 'TL15A_OPENCPRI':
        mail_content += """<br><span style='color:black'>
&nbsp;&nbsp;&nbsp;&nbsp;<b>More info to link : </b><a href="http://hzling21.china.nsn-net.net:8080/view/TL15A/job/RL65_OPEN_CPRI_BTS615_46//">http://hzling21.china.nsn-net.net:8080/view/TL15A/job/RL65_OPEN_CPRI_BTS615_46/</a><br>
</span>"""
        
    if SWRelease == 'RL45':
        mail_content += """<span style='color:red'>1. Please see the release notes<BR>
    2. Special notes will be added manually if needed<BR>
    3. Please execute below action if you upgrade to RL45 build in the first time:  ENB with OBSAI RRU connected: delete the app.oam.startup.loadIndicat! ion  ;in /flash/config/fct pcf file; ENB with CPRI RRU connected: set app.oam.startup.loadIndication to be CPRI in  /flash/config/fct pcf file.  <BR>
    4. Please follow the LCR9.0 guide strictly,Or the TDS cell can not be actived.guide link: \\10.68.152.98\tdlte\I&V\TDTECH\LCR9.0\LCR9.0_Guide <BR>
    </span>"""
        mail_content += """<span style='color:#00B050'>LTE940 hard security is enabled. Please EVERYONE strictly follow the upgrade guideline provided by Hu Yue.</span></b>
<b><span style='font-size:12.0pt;color:red'> Otherwise your HW is very easy to get broken, and can only be repaired by sending back to the factory. </span>"""
    if SWRelease == 'CMCCRL45':
        mail_content += """<span style='color:red'>
              If your UE is not supported Band41, you can modify 'Band41' to 'Band38' under 'FZHJ' in BPF.<BR>
</span>"""
    if SWRelease == 'CMCCRL35':
        mail_content += """<span style='color:#00B050'>LTE940 hard security is enabled from LNT3.1_ENB_1209_202_00 onwards. Please EVERYONE strictly follow the upgrade guideline provided by Hu Yue.</span></b>
<b><span style='font-size:16.0pt;color:red'> Otherwise your HW is very easy to get broken, and can only be repaired by sending back to the factory.</span>"""
    elif SWRelease == 'RL35':
        mail_content += """<span style='color:#00B050'>LTE940 hard security is enabled from LNT3.0_ENB_1304_079_01 onwards. Please EVERYONE strictly follow the upgrade guideline provided by Hu Yue.</span></b>
<b><span style='font-size:16.0pt;color:red'> Otherwise your HW is very easy to get broken, and can only be repaired by sending back to the factory.</span>"""
    else:
        pass
    mail_content += """
<P><i><u><b><SPAN>%s TA Execution Details</SPAN></b></u></i></P>
<TABLE style="font-size:9.0pt; BORDER-COLLAPSE: collapse; MARGIN-LEFT: -0.6pt" border=0 cellSpacing=0 cellPadding=0 width=%s>
"""%(JOB, 957 if SWRelease != 'RL55' else (len(conf55) +2)*100)


    #if SWRelease == 'RL55' or SWRelease == 'FZMRL55':
    if SWRelease == 'RL55' or SWRelease == 'TL15A' or SWRelease == 'TLF15A' or SWRelease == 'FZMRL55' or SWRelease == 'TL16' or SWRelease == 'TL16A' or SWRelease == 'TLF16' or SWRelease == 'TLF16A' or SWRelease == 'TL15A_OPENCPRI':
        rl55_body = ""
        rl55_head = "<tr><th><b>Case Name</b></th>"
        for i in range(len(conf55)):
            rl55_head +="<th><b>%s</b></th>"%conf55[i]
        rl55_head +="</tr>"
        for case_key in sorted(ret55.keys()):
            print("%s"%case_key)
            rl55_body += "<tr><td><b>%s</b></td>"%case_key
            #for i in range(len(conf55)):
            #for conf in sorted(conf55,key=lambda a:a[1],reverse=1):
            for conf in conf55:
                htmlTmp =  ret55[case_key][conf.strip()] if conf in ret55[case_key] else '-'
                if 'FAIL' in htmlTmp:
                    htmlTmp = "<font color=\"red\">FAIL</font>"
                rl55_body +="<td>%s</td>"% htmlTmp 
            rl55_body +="</tr>"
        mail_content += rl55_head + rl55_body
    else:
        mail_content += "<tr><td>Test Name</td><td>Result</td><td>Executed Times</td><td>Pass Times</td><td>Pass Rate</td><td>Failure Reason</td></tr>"
        if JOB == 'QT1':
            for qt in QTCaseResult:
                qt = list(qt)
                qt[6] = int(qt[6])
                if qt[6] == 0:
                    continue
                if qt[6] in [8, 3, 5, 7,9] :
                    if SWRelease == 'CMCCRL35' and qt[0].find("FZ")<0:
                        qt[0] = qt[0] + ' [FZFF]'
                    elif SWRelease == 'RL35':
                        qt[0] = qt[0] + ' [8Pipe]'
                if qt[6] in [2, 3, 4] and SWRelease == "RL35":
                    qt[0] = qt[0].replace("FZND", "2Pipe")
                if qt[1].upper() == "PASS" or qt[1].upper() == "LIMITEPASS":
                    if str(qt[5]) in ('17436' , '17445' , '17621' , '21258' , '21276' , '21312' , '21294','25645','25655','63665','68418'):
                        qt[1] = qt[1] + ' '+ GetThroughput(BuildID, qt[5])
                    else:
                        qt[1] = "Pass"
                    qt[2] = qt[3] = 1
                    qt[4] = "100%"
                else:
                    qt[2] = 1
                    qt[3] = 0
                    qt[4] = "0%"
                mail_content += """<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"""%(qt[0], qt[1] if qt[1].upper().find('PASS')>=0 else '<font color="red">' + qt[1] + '</font>', qt[2], qt[3], qt[4], "&nbsp;")
        elif JOB == "QT2":
            for qt in QTCaseResult:
                qt = list(qt)
                qt[6] = int(qt[6])
                if qt[6] == 0:
                    continue
                if qt[6] in [2, 3, 5, 7, 8, 9] :
                    if SWRelease == 'CMCCRL35' and qt[0].find("FZ")<0:
                        qt[0] = qt[0] + ' [FZFF]'
                    elif SWRelease == 'RL35' and qt[0].find("FZ")<0:
                        qt[0] = qt[0] + ' [8Pipe]'
                if qt[6] in [2, 3, 4] and SWRelease == "RL35":
                    qt[0] = qt[0].replace("FZND", "2Pipe")
                if str(qt[5]) in ('17457', '17464', '17456', '17458', '17465', '17627', '17628', '18684','21264','21282','21318','21300','21255','17618','21273','21309','21291','21265','21283','21319','21301') and (qt[1].upper() == "PASS" or qt[1].upper() == "LIMITEPASS"):
                    qt[1] = "Pass"
                    qt[2] = qt[3] = 3
                    qt[4] = "100%"
                else:
                    qt[2] = qt[3] = 1
                    qt[4] = "100%"
                mail_content += """<tr><td>%s</td><td>%s</td><td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td></tr>"""%(qt[0], qt[1], qt[2], qt[3], qt[4], "&nbsp;")
    
    if 'LNT3.1' in BuildID:
        mail_content += """</table>
<STRONG><SPAN style="FONT-FAMILY: 'Calibri','sans-serif'">CommonCFG:&nbsp;</STRONG>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<A href="http://82ndx2x.china.nsn-net.net/envbackup/RL35_CMCC/GOLDEN_CMCC">
http://82ndx2x.china.nsn-net.net/envbackup/RL35_CMCC/GOLDEN_CMCC</A>&nbsp;
""" 
    else:
        mail_content += "</table>"

    print "##############\n%s" %mail_content
    
    Public_alarm = {}
    if SWRelease == "RL25":
        Public_alarm["All"] = []
    elif SWRelease == "RL35":
        #Public_alarm["2Pipe"] = []
        Public_alarm["8Pipe"] = []
    elif  SWRelease == "CMCCRL35":
        #Public_alarm["FZND"] = []
        #Public_alarm["FZNN"] = []
        Public_alarm["FZFF"] = []
    elif SWRelease == "RL45":
        #Public_alarm["2Pipe"] = []
        Public_alarm["8Pipe"] = []
        #Public_alarm["IR_2Pipe"] = []
        Public_alarm["IR_8Pipe"] = []
        #Public_alarm["FSIH_8Pipe"] = []
    elif SWRelease == "CMCCRL45":
        Public_alarm["8Pipe"] = []
        Public_alarm["FSIH_8Pipe"] = []
    for tc in Alarm_Case:
        if SWRelease == "RL25":
            alarm_flag = ""
            Public_alarm['All'].append(tc)
        elif SWRelease == "RL35":
            if tc[0].find("FZND") >0 :
                Public_alarm['2Pipe'].append(tc)
            else :
                Public_alarm['8Pipe'].append(tc) 
        elif SWRelease == "CMCCRL35":
            if tc[0].find("FZND") >0:
                Public_alarm['FZND'].append(tc)
            elif tc[0].find("FZNN") >0:
                Public_alarm['FZNN'].append(tc)
            else:
                Public_alarm['FZFF'].append(tc)
        elif SWRelease == "CMCCRL45":
            if tc[0].endswith('[8Pipe]'):
                Public_alarm['8Pipe'].append(tc)
            elif tc[0].endswith('[FSIH 8Pipe]'):
                Public_alarm['FSIH_8Pipe'].append(tc)
        elif SWRelease == "RL45":
            #if tc[0].endswith('[IR 2Pipe]'):
            #    Public_alarm['IR_2Pipe'].append(tc)
            if tc[0].endswith('[IR 8Pipe]'):
                Public_alarm['IR_8Pipe'].append(tc)
            #elif tc[0].endswith('[FSIH 8Pipe]'):
            #    Public_alarm['FSIH_8Pipe'].append(tc)
            #elif tc[0].endswith('[2Pipe]'):
            #    Public_alarm['2Pipe'].append(tc)
            elif tc[0].endswith('[8Pipe]'):
                Public_alarm['8Pipe'].append(tc)
            else:
                pass
            

    def content_with_table_style(content, color="yellow"):
        return """<span style='color:black;background:%s;mso-highlight:%s'>%s</span>""" %(color, color, content)
        
    if JOB == "QT1":
        for k in Public_alarm.keys():
            case_alarm = Public_alarm[k]
            mail_content += """
        <P class=MsoNormal><SPAN
              style="FONT-FAMILY: 'Calibri','sans-serif'; COLOR: black; FONT-SIZE: 11pt"
              lang=EN-US><STRONG>%s Alarm List:</STRONG><SPAN
              class=387322905-11062012><FONT color=#0000ff size=2
              face=Arial>&nbsp;</FONT></SPAN></SPAN></P>
              <P class=MsoNormal><SPAN
              style="FONT-FAMILY: 'Calibri','sans-serif'; COLOR: black; FONT-SIZE: 11pt"
              lang=EN-US>
        
        <TABLE style="font-size:9.0pt; WIDTH: 718pt; BORDER-COLLAPSE: collapse; MARGIN-LEFT: 0.6pt"
        class=MsoNormalTable border=0 cellSpacing=0 cellPadding=0 width=957>
        """%(k)
            
            mail_content += "<tr><td>Serverty</td><td>Time</td><td>Fault Name</td><td>Source</td></tr>"
            cur_alarms_added = []
            for tc in case_alarm:
                #cur_alarm_ids = ALL_CASE_ALARM[tc[0]]:
                cur_tc_alarms = tc[1].split("|")[1:]
                for alm in cur_tc_alarms:
                    res = re.match(".*\((\d+)\).*", alm)
                    if not res:
                        continue
                    alm_id = res.groups()[0]
                    alarm_color = "yellow"
                    if alm_id not in cur_alarms_added:
                        if alm_id.strip() in alarmExclude:
                            alarm_color = "white"
                        cur_alarms_added.append(alm_id)
                        alarm_tmp = alm.split(";")
                        mail_content += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" %tuple([content_with_table_style(x, alarm_color) for x in alarm_tmp])
            mail_content += "</table>"

    mail_content +="""
<P><u><i><B><SPAN>QT release criteria:</SPAN></B></i></u></P>

<ul>
<li><span>1. released when success rate =100%.</span></li>
<li><span>2. released with restriction when success rate&ge;66% or some errors shown on SEM.</span></li>
<li><span>3. not released when success rate&lt;66%.</span></li>
</ul>
<span>You can subscribe or unsubscribe to the TDLTE release note quicktest mail through the links below:</span><br>
<p><a href="mailto:Majordomo@mlist.emea.nsn-intra.net?subject=Subscribe&amp;Body=subscribe%20coo-ra-bts-td-lte-build-release@mlist.emea.nsn-intra.net%0dend">
<span style='font-family:"Arial","sans-serif";background:white;text-decoration:none'>Subscribe</span></a></p>
<p><a href="mailto:Majordomo@mlist.emea.nsn-intra.net?subject=Subscribe&amp;Body=unsubscribe%20coo-ra-bts-td-lte-build-release@mlist.emea.nsn-intra.net%0dend">
<span style='font-family:"Arial","sans-serif";background:white;text-decoration:none'>Unsubscribe</span></a></p>
"""
#    if SWRelease == "RL35":
#        mail_content += "<BR> </SPAN></P>"
#    else:
#        mail_content += "<BR> </SPAN></P>"

    _DATA_DIC = {
            'QT1': {
                    '_method'                        : "patch",
                    #'attach_sub_notes'               : '1',
                    'authenticity_token'             : '',
                    'build[important_notes_qt]'      : "",
                    'build[important_notes_qt_author]':"",
                    'build[important_notes_qt_created_at]':"",
                    'build[quick_test_template_id]'  : 43,

                    'cc'                             : mail_cc,
                    'quicktest[links]'               : qtlinks,
                    'quicktest[reason]'              : qtreason,
                    'quicktest[result]'              : release_result,
                    'quicktest[subject]'             : mail_subject,
                    'quicktest[tests]'               : mail_content,
                    'quicktest[text]'                : mail_content,
                    'to'                             : mail_to,
                    'reply_to'                       : mail_reply,
                    #'attach_releasenote'             : '0',
                    'utf8'                           :'✓',
                    'commit'                         : 'Send Releasenote'
                    },
             'QT2': {
                    '_method'                        : "patch",
                    #'attach_sub_notes'               : '1',
                    'authenticity_token'             : '',
                    'build[important_notes_qt2]'      : "",
                    'build[important_notes_qt2_author]':"",
                    'build[important_notes_qt2_created_at]':"",
                    'build[quicktest2_template_id]'  : 91,
                    'quicktest2[result]'             : release_result,
                    'quicktest2[tests]'              : mail_content,
                    'quicktest2[links]'              : qtlinks,
                    'quicktest2[reason]'             : qtreason,
                    'to'                             : mail_to,
                    'cc'                             : mail_cc,
                    'reply_to'                       : mail_reply,
                    'quicktest2[subject]'            : mail_subject,
                    'quicktest2[text]'               : mail_content,
                    #'attach_releasenote'             : '0',
                    'utf8'                           :'✓',
                    'commit'                         : 'Send Releasenote'
                    }
            }
    if WFTUSER != "":
        print """
    ==================1, LogIn to WFT=========================="""
        obj = Process_WFT(WFTUSER, WFTPASWD)
    else:
        raise "Pls fill in you WFT username and password."

    print """
    ================= 2, GetContentOfLink======================
    %s
    ===========================================================
    """ %RelLink
    BuildContent = obj.GetContentOfJob(RelLink)
    AuthToken = GetTokenFromContent(BuildContent)
    print """
    ================= 3, GetHrefOfBuild======================
    BuildID: %s
    QTLink: %s
    ===========================================================
    """ %(BuildID, QtLink)

    #RelLink = obj.GetHrefOfRel(BuildID, BuildContent, SendType)
    print "The Release link is: %s" % RelLink
    if SendMethod.upper().strip() == "PREVIEW":
        #RelID = re.findall("https://.*/(\d+)", RelLink)[0]
        RelID = re.findall("edit_build_(\d+)", BuildContent)[0]
        link = "%s/%s/preview.js" %(QtLink, RelID)
    else:
        link = RelLink
        #if JOB == "QT2":
         #   RelID = re.findall("edit_build_(\d+)", BuildContent)[0]
          #  link = "%s/released/%s" %(QtLink,  RelID)
    #QT2 "https://wft.inside.nokiasiemensnetworks.com:8000/quicktest2s/released/71195"
    #https://wft.inside.nokiasiemensnetworks.com:8000/quicktest2s/LNT3.0_ENB_1207_027_00/release
    if not link:
        print "Have not get the last data link! Exit..."
        sys.exit(2)

    print """
    ==================4, SendDataToWFT==========================
    link: %s
    ===========================================================
""" %link
    _DATA_DIC[JOB]["authenticity_token"] = AuthToken
    obj.SendDataToWFT(link)
    if SendMethod.upper().strip() != "PREVIEW":
        UpdateMailStatus(BuildID, JOB)
    print "Process OK! Passed."
    sys.exit(0)
