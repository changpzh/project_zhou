#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xmlrpclib import ServerProxy, Fault
from cmd import Cmd
from random import choice
from string import lowercase
from server import Node,UNHANDLED, inside
from threading import Thread
from time import sleep
import sys

def main():
    urlfile, directory = sys.argv[1:]
    client = inside(directory, urlfile)
    print client


if __name__ == '__main__':
    main()