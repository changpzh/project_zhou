"""
**=============================================================
 * Copyright: 2012~2015
 * FullName:
 * Description:
 * Changes:
 *==============================================================
 * Date:
 * Author: changpzh
 * Comment:  download file from remote server, use "rsync" command.
**==============================================================
"""
import os, logging

def download_SM(JENKINS_L3SM,username,hostip):
    TempDirWin = "D:/temp"
    TempDirCygwin = "/cygdrive/d/temp"
    if os.path.exists(TempDirWin):

        cmd2 ="rsync -avz %s@%s:%s %s/BTSSiteEM-TD-LTE.exe" % (username,hostip,JENKINS_L3SM, TempDirCygwin)
        """
        rsync file from remote server to local pc.
        """
        logging.info("Run cmd: %s" % cmd2)
        try:
            if os.system(cmd2) !=0:
                logging.error("Run command %s failed" % cmd2)
                exit(1)
        except:
            logging.error("Get L3 SM form Jenkins failed")
            exit(1)
    else:
        logging.error("%s not exist !!!" % TempDirWin)
        exit(1)


    #cmd3 = "cacls %s/BTSSiteEM-TD-LTE.exe /G everyone:F" % TempDirCygwin
    cmd3 = "chmod 777 %s/BTSSiteEM-TD-LTE.exe" % TempDirCygwin
    """
    change file permission 'cacls filename /G everyone:F'
    """
    logging.info("Run cmd: %s" % cmd3)
    try:
        if os.system(cmd3) !=0:
                logging.error("Run command %s failed" % cmd3)
                exit(1)
    except:
        logging.error("Get L3 SM form Jenkins failed")
        exit(1)

def main():
    USERNAME = 'btstest'
    HOSTIP   = '10.140.90.25'
    BTSSMVERSION = 'TLF00_BTSSM_0000_000001_000000'
    JENKINS_L3SM = '/cygdrive/c/Temp/BTSSM_TDD/FZM_TRUNK/%s/C_Element/SE_UICA/Setup/*.exe' % BTSSMVERSION

    download_SM(JENKINS_L3SM,USERNAME,HOSTIP)

if __name__ == '__main__':
    main()