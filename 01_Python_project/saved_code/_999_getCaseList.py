__author__ = 'changpzh'
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
''' get qt data,
and submit it to falcon
'''
# ***************import zone start************
import logging
import sys,os
if os.path.join(os.getcwd(),"ENV_file") not in sys.path:
    sys.path.append(os.path.join(os.getcwd(),"ENV_file"))
from Case import Case
print(sys.path)
# ***************import zone end**************

def getCaseList(caseConfig):
    """Get case name from case config file
    @param caseConfig: case config file
    @type caseConfig: String
    Caselist.txt file should format like below
    Casename TestLevel env1,env2,env3,env4,...,envN
    SWDL_SEM 1 2PIPEFZND,2PIPEFWNC,4PIPE,8PIPE,8FSIH,2IR,8IR
    """
    caseList = []
    confile = open(caseConfig,'r')
    i=0
    j=100
    for line in confile.readlines():
        logging.debug(line)
        line = line.strip()
        if not line.startswith('#') and line != '':
            if len(line.split()) >= 3:
                envs = line.split()[2].split(',')
                j+=1
                print(j)
                print(line.split())
                print("envs is: %s" % envs)
                for env in envs:
                    case = Case()
                    print ("case: %s" % case)
                    case.setName(line.split()[0])
                    print("caseName: %s" % case.name)
                    case.setTestLevel(line.split()[1])
                    print("testlevel: %s" % case.testLevel)
                    case.setDsp(env)
                    print("Dsp: %s" % case.dsp)
                    caseList.append(case)
                    i+=1
                    print(i)
                    print( "caseList: %s" % caseList)
                    print( "end %s\n" % i)
                    logging.debug(case.getName()+":"+case.getTestLevel()+":"+case.getDsp())

            else:
                print(line.split()[1]+"is config is not correct please check")
                logging.error(line.split()[1]+"is config is not correct please check")
    confile.close()
    print( "zhouzhou=====================")
    print( "case: %s" % case)
    print( "caseList: %s" % caseList)
    return caseList

def main():
        caseConfig = "D:\\Project_Zhou\\01_Python_project\\FilePath\\caselist.txt"
        caseList = getCaseList(caseConfig)
        print( "\nstart")
        print(caseList)
        print( "end")

if __name__ == '__main__':
    main()