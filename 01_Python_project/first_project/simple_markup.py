__author__ = 'changpzh'
"""
##=============================================================
# Copyright:
# Function:transfer txt file to html
# Description: input must like: python simple_arkup.py <test.txt> test.html
# Date:2015-12-24
# Author: changpzh
# Email:changping.zhou@foxmail.com
##==============================================================
"""

import sys, re
from util import *

print ('<html><head><title>...</title></head><body>')

title = True
for block in blocks(sys.stdin):
    block = re.sub(r'\*(.+?)\*', r'<em>\1</em>', block)
    if title:
        print('<h1>')
        print(block)
        print('</h1>')
        title = False
    else:
        print('<p>')
        print(block)
        print('</p>')

print('</body></html>')