#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# #------------------------------------
#  Copyright: 2015~2025
#  Function :
#  Data: 2016/10/18 10:55
#  Author:changping.zhou@foxmail.com
# #-------------------------------------
# #-------------------------------------
'''
# try:
#     from urllib.request import urlopen
# except ImportError:
#     from urllib2 import urlopen
from xml.etree import ElementTree as ET
import urllib.request
import argparse
import os,re

#windows systerm
import _000_show_color as myColor
BOLDER_GREEN = '\033[1;32m'
END = "\033[0m"

class XmlHandle(object):
    def xml_findContentsInHier(self, file, hierarchy):
        '''
        :param file: xml file full path
        :param hierarchy: which node do you want [eg: ./assignments/ecl_used_in]
        :return:'''
        contents = []
        f = ET.parse(file)
        per = f.findall(hierarchy)
        for oneper in per:
            for child in oneper.getchildren():
                contents.append(child)
                # print(child.tag, ":", child.text)
                #action for loop
        return contents

    def xml_isMatch(self, node, attriName, kw_map):
        '''判断某个节点是否包含传入node的attriName属性
           node: 节点
           attriName: 需要获取的attributeName
           kw_map: 属性及属性值组成的list : []'''
        tmpName = node.get(attriName)
        return tmpName if tmpName in kw_map else False

    def isMatch(self, myInput, kw_map):
        """:param myInput:
        :param kw_map:
        :return:
        """
        for one in kw_map:
            if one in myInput:
                return True
        return False
        # return myInput if myInput in kw_map else False

    def FindNodes(self, tree, path):
        '''查找某个路径匹配的所有节点
       tree: xml树
       path: 节点路径'''
        return tree.findall(path)

def print_line():
    print("-"*135)

def print_table_title(release, build_1, build_2):
    print_line()
    print("| %-30s| %-50s| %-50s|" % (release,build_1,build_2))
    print_line()

def print_content(sc_prefix, sc_name, release_time):
    print("| %-30s| %-50s| %-50s|" % (sc_prefix, sc_name, release_time))


def file_write(FilePath, NewContent,Mode):
    if not os.path.isdir(os.path.dirname(FilePath)):
        os.makedirs(r'%s' % os.path.dirname(FilePath))  # create new dir path if none exist.

    try:
        f = open(FilePath,Mode) # open a file, create new one if not exist.
        f.write(NewContent + '\n')
    finally:
        f.close()

if __name__ == '__main__':

    base_build = "TL16A_ENB_0000_002030_000000"
    build_2 = "TL16A_ENB_0000_002029_000000"
    build_link_1 ="https://wft.inside.nsn.com/ext/build_content/"+base_build.strip()+"#build=1"
    build_link_2 ="https://wft.inside.nsn.com/ext/build_content/"+build_2.strip()+"#build=1"

    #replace[TL] to x.
    patt = re.compile(r'[TF]')
    repl_string = "x"
    release = re.sub(patt, repl_string, base_build.split("_ENB_")[0])

    # get content of build 1
    f_1 = urllib.request.urlopen(build_link_1)
    build_content_1 = f_1.read().decode('utf-8')    # f.read()文件流，相当于buffer，读一次便释放了
    file_write('d:\\project_zhou\\test_folder\\base_build.xml', build_content_1, "w")
    # get content of build 2
    f_2 = urllib.request.urlopen(build_link_2)
    build_content_2 = f_2.read().decode('utf-8')    # f.read()文件流，相当于buffer，读一次便释放了
    file_write('d:\\project_zhou\\test_folder\\build_2.xml', build_content_2, "w")

    foo_1 = XmlHandle()
    build_contents_1 = foo_1.xml_findContentsInHier('d:\\project_zhou\\test_folder\\base_build.xml', './content')
    foo_2 = XmlHandle()
    build_contents_2 = foo_2.xml_findContentsInHier('d:\\project_zhou\\test_folder\\build_2.xml', './content')

    # save all sc in dict.
    all_sc = {}
    special_SC = ["PHY_TX", "PHY_RX"] # PHY_TX has two，one with TL##_PHY_TX, another is FL##_PHY_TX。
    digit_patt = re.compile(r'_\d+_')   # split name with _numbers_
    for content in build_contents_1:
        tmpTitle = content.get("title")
        # PHY_TX has two，one with TL##_PHY_TX, another is FL##_PHY_TX。
        if (tmpTitle in special_SC):
            tmpTitle = re.split(digit_patt,content.text)[0]
        all_sc[tmpTitle] = {"tdd": content.text, "fdd": ""}

    # get another build's contents save to all_sc with base build.
    for content in build_contents_2:
        tmpTitle = content.get("title")
        # PHY_TX has two，one with TL##_PHY_TX, another is FL##_PHY_TX。
        if (tmpTitle in special_SC):
            tmpTitle = re.split(digit_patt, content.text)[0]
        # didn't consider build 2's unique sc
        if tmpTitle in all_sc.keys():
            all_sc[tmpTitle]['fdd'] = content.text
        # else:
        #     all_sc[content.get("title")] = {"fdd": content.text, "tdd":""}

    # print Table title with given color.
    print_table_title(myColor.colorBegin(release, front="bold", fore='green'), base_build, myColor.colorEnd(build_2))
    # foo_1.print_table_title("\033[1;32m"+release, base_build, build_2+"\033[0m")

    # print table contents. highlight SC when diff with build 2 but both have content.
    for key, value in all_sc.items():
        if (value["tdd"] != value["fdd"] and value["fdd"] != ""):
            print_content(key, (myColor.colorStyle(value["tdd"], front="bold", fore="red")), value["fdd"])
        else:
            print_content(key, value["tdd"], value["fdd"])
        print_line()
