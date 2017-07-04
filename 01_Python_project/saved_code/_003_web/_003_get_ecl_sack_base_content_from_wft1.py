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
from xml.etree import ElementTree as ET
import urllib.request
import argparse
import os,re

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

    def find_nodes(self, tree, path):
        '''查找某个路径匹配的所有节点
        tree: xml树
        path: 节点路径'''
        return tree.findall(path)

    def xml_print_line(self):
        print("-"*100)

    def xml_print(self, sc_prefix, sc_name, release_time):
        print("| %-21s| %-42s| %-30s|" % (sc_prefix, sc_name, release_time))

def file_write(FilePath, NewContent,Mode):
    if not os.path.isdir(os.path.dirname(FilePath)):
        os.makedirs(r'%s' % os.path.dirname(FilePath))  # create new dir path if none exist.

    try:
        f = open(FilePath,Mode) # open a file, create new one if not exist.
        f.write(NewContent + '\n')
    finally:
        f.close()

if __name__ == '__main__':
    #read xml content to File
    ecl_sack_base = "FL16A_ECL_SACK_BASE_0000_000088_000000"
    urlLink = "https://wft.inside.nsn.com/ext/build_content/"+ecl_sack_base+"#build=5"
    f = urllib.request.urlopen(urlLink)
    url_content = f.read().decode('utf-8') # f.read()文件流，相当于buffer，读一次便释放了
    file_write('d:\\project_zhou\\test_folder\\myxml.xml', url_content, "w")

    tatal_sc = {}
    my_sc = ["TL16A_BTSSM_"]
    #handle xml file
    foo = XmlHandle()
    ecl_used_in_contents = foo.xml_findContentsInHier('d:\\project_zhou\\test_folder\\myxml.xml', './assignments/ecl_used_in')


    for content in ecl_used_in_contents:
        is_match = foo.isMatch(content.text, ["TL16A", "FL16A"])
        if is_match:
            sc_prefix = content.text.split("W17")[0] if "FTM_FL16A_TL16A" in content.text else content.text.split("0000")[0]
            foo.xml_print_line()
            foo.xml_print(sc_prefix, content.text, "")
            tatal_sc[sc_prefix] = content.text
    foo.xml_print_line()

    print("="*20 + ecl_sack_base)
    for key,value in tatal_sc.items():
        foo.xml_print_line()
        foo.xml_print(key, value, "")
        # print(content.text)

    poo = XmlHandle()
    used_in_contents = poo.xml_findContentsInHier('d:\\project_zhou\\test_folder\\myxml.xml', './assignments/used_in')

    for node in used_in_contents:
        is_match = poo.xml_isMatch(node, "title", ["TL16A_0.3", "FL16A_0.3", "TL16A_1.0", "FL16A_1.0"])

        if is_match:
            print("="*10 + is_match)
            for child in node.getchildren():
                foo.xml_print_line()
                poo.xml_print(child.text.split("0000")[0], child.text, "")
            foo.xml_print_line()
                # print(child.text)

    # poo.xml_print("FL16A_ENB_", "FL16A_ENB_0000_001196_000000", "2016/09/09")
    # poo.xml_print("FLC16A_ZMGR_", "FLC16A_ZMGR_0000_000089_000000", "2016/09/09")

    # d = { 'Adam': 95, 'Lisa': 98, 'Bart': 100 }
    # def generate_tr(name, score):
    #     if score > 90:
    #         return '<tr><td>%s</td><td style="color:red">%s</td></tr>' % (name, score)
    #     # return '<tr><td>%s</td><td>%s</td></tr>' % (name, score)
    # tds = [generate_tr(name, score) for name, score in d.items()]
    # print('<table border="1">')
    # print('<tr><th>Name</th><th>Score</th><tr>')
    # print('\n'.join(tds))
    # print('</table>')


