#!/usr/bin/python
import sys
from config.default_settings import MAIL_HOST, MAIL_SENDER,MAIL_REPLY_TO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging


class MailOperation():
    def __init__(self, sender="", to_list=[], cc_list=[], subject="", content="", packageName="", jobName="", jobStatus="", jobCase="", jobTime="", jobURL=""):       
        self.sender = sender
        self.to_list = to_list
        self.cc_list = cc_list
        self.subject = subject
        self.content = content
        self.packageName = packageName
        self.jobName = jobName
        self.jobStatus = jobStatus
        self.jobCase = jobCase
        self.jobTime = jobTime
        self.jobURL = jobURL
        
    
    def send_mail(self):
        contents = MIMEMultipart('related')
        contents['from'] = self.sender or MAIL_SENDER
        contents['to'] = ";".join(self.to_list)
        contents['cc'] = ";".join(self.cc_list)
        contents['Subject'] = self.subject
        contents.preamble = 'This is a multi-part message in MIME format.'
        
        msg = MIMEText(self.format_content(),'html','utf-8')
        contents.attach(msg)
        try:
            smtp = smtplib.SMTP()
            smtp.connect(MAIL_HOST)
            smtp.set_debuglevel(1)
            if self.to_list:
                smtp.sendmail(contents['from'],self.to_list,contents.as_string())
            if self.cc_list:
                smtp.sendmail(contents['from'],self.cc_list,contents.as_string())
            smtp.quit()    
        except:        
            sys.exit(1)
            
    def send_sms(self):
        contents = MIMEMultipart('related')
        contents['from'] = self.sender or MAIL_SENDER
        contents['to'] = ";".join(self.to_list)
        contents['cc'] = ";".join(self.cc_list)
        contents['Subject'] = self.subject
        contents.preamble = 'This is a multi-part message in MIME format.'

        msg = MIMEText(self.content,'html','utf-8')
        contents.attach(msg)

        try:
            smtp = smtplib.SMTP()
            smtp.connect(MAIL_HOST)
            smtp.set_debuglevel(1)
            if self.to_list:
                smtp.sendmail(contents['from'],self.to_list,contents.as_string())
            if self.cc_list:
                smtp.sendmail(contents['from'],self.cc_list,contents.as_string())
            smtp.quit()    
        except:        
            sys.exit(1)
        
    def format_content(self):
        message = "Hi,<br><br>This notification intend to show status of jenkins job:<br>"
        message += """<style type="text/css">
                    table{
                        margin-top: 5px;
                        font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
                        width: 100%;
                        border-collapse: collapse;
                    }
                    .name {
                       background-color: #daf7db;
                    }
                    th {
                        background-color: #97ed9b;
                    }
                    td, th {
                        font-size: 12px;
                        height: 21px;
                        border: 1px solid #98bf21;
                    }
                    </style>
                    <html><table>""" 
        message += "<tr><td class='name'>Job name:</td><td>%s</td></tr>" % self.jobName
        message += "<tr><td class='name'>Job status:</td><td>%s</td></tr>" % self.jobStatus
        message += "<tr><td class='name'>Run target:</td><td>%s</td></tr>" % self.jobCase       
        message += "<tr><td class='name'>Job starttime:</td><td>%s</td></tr>" % self.jobTime
        message += "<tr><td class='name'>Link for test report:</td><td><a href='%s'>%s</a></td></tr>" % (self.jobURL, self.jobURL)
        message += "<tr><td class='name'>Link for detail:</td><td><a href='%s/console'>%s/console</a></td></tr>" % (self.jobURL, self.jobURL)
        message += "</table><br>%s</html>" % self.content
        message += "<br>Br,<br><a href='%s'>%s</a>" % (MAIL_REPLY_TO, MAIL_REPLY_TO)
        return message
    
    
class Cpdlog():
    """
    cpdlog config
    """
    def __init__(self,logFile,file_level):
        self.MAPPING={"CRITICAL" :50,
           "ERROR" : 40,
           "WARNING" : 30,
           "INFO" : 20,
           "DEBUG" : 10,
           "NOTSET" :0,
           }
        self.config(logFile, file_level)

    def config(self,logFile,file_level):
        self.logger = logging.getLogger(" *Send Email* ")
        self.logger.setLevel(self.MAPPING[file_level])
        self.fh = logging.FileHandler(logFile,mode='w')
        self.fh.setLevel(self.MAPPING[file_level])

        self.ch = logging.StreamHandler()
        self.ch.setLevel(self.MAPPING[file_level])

        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s : %(message)s",'%Y-%m-%d %H:%M:%S')
        self.fh.setFormatter(formatter)
        self.ch.setFormatter(formatter)
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)


    def debug(self,msg):
        if msg is not None:
            self.logger.debug(msg)
    def info(self,msg):
        if msg is not None:
            self.logger.info(msg)
    def warning(self,msg):
        if msg is not None:
            self.logger.warning(msg)
    def error(self,msg):
        if msg is not None:
            self.logger.error(msg)
    def critical(self,msg):
        if msg is not None:
            self.logger.critical(msg)
    def Close(self):
        """Close logger"""
        self.fh.flush()
        self.ch.flush()
        self.logger.removeHandler(self.fh)
        self.logger.removeHandler(self.ch)
        return True         

