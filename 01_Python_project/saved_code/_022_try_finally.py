#!/usr/bin/python
# -*- coding: utf-8 -*-

def main():
    # try:
    #     try:
    #         ccfile = open('can.txt','r')
    #         tx = ccfile.readlines()
    #     except IOError,diag:
    #         print(str(diag))
    # finally:
    #     ccfile.close()
    #

    # try:
    #     try:
    #         ccfile = open('can.txt','r')
    #         tx = ccfile.readlines()
    #     finally:
    #         ccfile.close()
    # except IOError,diag:
    #     print(str(diag))

    try:
        ccfile = open('can.txt','r')
        tx = ccfile.readlines()
    finally:
        ccfile.close()

if __name__ == '__main__':
    main()