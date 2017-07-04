__author__ = 'changpzh'
#you should know something about optparse and argparse
#here is a example on the last of argparse of QT team project.
# '''
# As of 2.7, optparse is deprecated, and will hopefully go away in the future.
# argparse is better for all the reasons listed on its original page (http://code.google.com/p/argparse/):
#
# handling positional arguments
# supporting sub-commands
# allowing alternative option prefixes like + and /
# handling zero-or-more and one-or-more style arguments
# producing more informative usage messages
# providing a much simpler interface for custom types and actions
# '''

import os
import shutil
import sys
import tempfile
import zipfile
import optparse
import subprocess
import platform
import textwrap
import contextlib
import warnings

from distutils import log
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

try:
    from site import USER_SITE
except ImportError:
    USER_SITE = None

DEFAULT_VERSION = "18.3.2"
DEFAULT_URL = "https://pypi.python.org/packages/source/s/setuptools/"
DEFAULT_SAVE_DIR = os.curdir

def _parse_args():
    """Parse the command line for options."""
    """
D:\Python_project>C:\Python33\python.exe D:/Python_project/010_how_use_parse_args.py
{'version': '18.3.2', 'to_dir': '.', 'user_install': False, 'download_base': 'https://pypi.python.org/packages/source/s/setuptools/'}

D:\Python_project>C:\Python33\python.exe D:/Python_project/010_how_use_parse_args.py --version 32
{'version': '32', 'to_dir': '.', 'download_base': 'https://pypi.python.org/packages/source/s/setuptools/', 'user_install': False}

D:\Python_project>C:\Python33\python.exe D:/Python_project/010_how_use_parse_args.py --version=21
{'to_dir': '.', 'version': '21', 'download_base': 'https://pypi.python.org/packages/source/s/setuptools/', 'user_install': False}
"""
    parser = optparse.OptionParser()
    parser.add_option(
        '--user', dest='user_install', action='store_true', default=False,
        help='install in user site package (requires Python 2.6 or later)')
    parser.add_option(
        '--download-base', dest='download_base', metavar="URL",
        default=DEFAULT_URL,
        help='alternative URL from where to download the setuptools package')
    parser.add_option(
        '--version', help="Specify which version to download",
        default=DEFAULT_VERSION,
    )
    parser.add_option(
    	'--to-dir',
    	help="Directory to save (and re-use) package",
    	default=DEFAULT_SAVE_DIR,
    )
    options, args = parser.parse_args()
    # positional arguments are ignored
    return options

def main():
    """Install or upgrade setuptools and EasyInstall."""
    options = _parse_args()
    print(options)

if __name__ == '__main__':
    sys.exit(main())


"""
D:\Python_project>C:\Python33\python.exe D:/Python_project/010_how_use_parse_args.py
{'version': '18.3.2', 'to_dir': '.', 'user_install': False, 'download_base': 'https://pypi.python.org/packages/source/s/setuptools/'}

D:\Python_project>C:\Python33\python.exe D:/Python_project/010_how_use_parse_args.py --version 32
{'version': '32', 'to_dir': '.', 'download_base': 'https://pypi.python.org/packages/source/s/setuptools/', 'user_install': False}
"""


'''----------------------------------------------------------------------
C:\Python33\Scripts>py -3 ez_install.py --help
Usage: ez_install.py [options]

Options:
  -h, --help           show this help message and exit
  --user               install in user site package (requires Python 2.6 or
                       later)
  --download-base=URL  alternative URL from where to download the setuptools
                       package
  --insecure           Use internal, non-validating downloader
  --version=VERSION    Specify which version to download
  --to-dir=TO_DIR      Directory to save (and re-use) package
------------------------------------------------------------------------'''

#program2: this comes from getQt2result.py
'''
import logging
import argparse
import ast
import datetime,time
import os

def argsParser():
    """Parsing arguments from getQt2result invocation"""
    parser = argparse.ArgumentParser(description='This is used to get the final result from qt result log')
    parser.add_argument('-n', '--name',action='store', dest='packageName', help='This is QT package name')
    parser.add_argument('-c', '--caseconfig',action='store', dest='caseConfig', default='caselist.txt' ,help='This is case config file')
    parser.add_argument('-d', '--directory', action='store', dest='resultDir', default='/build/home/citdlte/CPD/QTResult/', help='You can get it from QT guys, which used store all package test result')
    parser.add_argument('-e', '--evnconfig',action='store', dest='envList', help='This is evn config file')
    parser.add_argument('-l','--level',action='store', dest='logLevel',help='This is log level setup')
    parser.add_argument('--buildurl',action='store', dest='buildUrl',default="",help='The build aip URL')
    parser.add_argument('--reporturl',action='store', dest='reportUrl',default="",help='The report url')
    parser.add_argument('--template',action='store', dest='template',default="caseResult.xsl",help='The transfer xsl tempalte')
    args = parser.parse_args()

    if not args.packageName:
        print('packageName is must be need')
        print('please use -h to get help info')
        exit(1)
    else:
        packageName = args.packageName

    caseConfig = args.caseConfig
    logging.debug("Load case config from:"+caseConfig)

    packResultDir = args.resultDir+'/'+packageName+'/'

    if args.envList:
        envConfig = args.envList
        evns = getEnvList(envConfig)
        resFileList = getResultFileList(packageName, evns)
    else:
        logging.debug("useing default env config")
        resFileList = getFilterResFileList(packageName, packResultDir)

    buildUrl = args.buildUrl
    reportUrl = args.reportUrl
    templateFile = args.template

    getAllResultTempFile(packResultDir,resFileList)
    caseList = getCaseResults(caseConfig)
    generateJunitXml(caseList,"testReport.xml")
    return (packageName, packResultDir, resFileList, buildUrl, reportUrl, templateFile, caseList)

def main():
    """main function"""
    (packageName, packResultDir, resFileList, buildUrl, reportUrl, templateFile, caseList) = argsParser()

if __name__ == '__main__':
    main()

'''

#'''
# argparse模块的具体应用如下：
#
#    1. creating argparser:
#
#            parser=argparse.ArgumentParser(description=,formatter_class=)
#
#        formatter_class=ArgumentDefaultHelpFormatter会将参数默认值自动放在help信息中
#
#    2. adding arguments:
#
#            parser.add_argument(name,action,nargs,const,default,type,choices,help,metavar,dest)
#
#        name：对于positional参数，即为dest，对于optional参数，可以是'-f','--format'
#
#        action主要有：'store','store_const','version'(version='%(prog)s 1.0')等
#
#        nargs：'N','?','*','+'等
#
#        const：值省略时的默认值（主要用在‘store_const’和‘？’两种情况）
#
#        default：参数省略时的默认值
#
#        type：参数获取后的数据类型转换
#
#        choices：可供选择的参数值
#
#        help：help信息
#
#        metavar：命令行显示的参数值
#
#        dest：参数存储的目标变量，对positional参数是name。
#
#    3. parsing arguments:
#
#            args=parser.parse_args()
#
#        args.dest用来调用参数。
# '''
