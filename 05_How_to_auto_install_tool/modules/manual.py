import os
import glob
import inspect 
from distutils.sysconfig import get_python_lib

def update_lib_path():
    cur = os.path.abspath(os.path.dirname(__file__))
    print("cur=%s" % cur)
    robotws_path = os.path.dirname(os.path.dirname(cur))
    print("robotws_path=%s" % robotws_path)
    lib_path = get_python_lib()
    print("lib_path=%s" % lib_path)
    pth_file = os.path.join(lib_path, 'RL55Lib.pth')
    print("pth_file=%s" % pth_file)
    f_obj = open(pth_file, 'w')
    print("f_obj1=%s" % f_obj)
    f_obj.write(robotws_path)
    f_obj = open(pth_file, 'r')
    print("f_obj2=%s" % f_obj)
    f_obj.close()


def get_path():    
    path = os.path.abspath(os.path.dirname(__file__))
    print("path=%s" % path)
    print(os.path)
    print(os.path.dirname(__file__))
    print(os.path.abspath(os.path.dirname(__file__)))
    return path

REQUIRES = [  
    'robotframework-2.8.4',
    'Pygments',
    'robotframework-ride',
    'robotframework-sshlibrary-2.1',
    'xlrd',
    'xlwt',
    'xlutils',
    'lxml',
    'pyserial',
    'pycrypto',
    'ecdsa',
    'paramiko-1.15.2',
    'Pyro4',    
    'pyasn1',
    'pysnmp',
    ]
    
REQUIRES_DEV = [
                'MySQL-python',
                'BeautifulSoup',
                'py2exe',
                'coverage', 
                'colorama',
                'logilab-astng',
                'logilab-common',
                'logilab-astroid',
                'pylint',
               ]



if __name__ == "__main__":

    pkgs = os.path.join(get_path(), 'must')
    print(pkgs)
    for pck in REQUIRES:
        pkg_path = glob.glob(os.path.join(pkgs, '%s*'%pck))[0]
        print(pkg_path)
        #cmd = "easy_install --always-unzip \"%s\"" % pkg_path
        #os.system(cmd)

    update_lib_path()
    



