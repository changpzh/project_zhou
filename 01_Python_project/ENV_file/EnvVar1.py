__author__ = 'changpzh'

import os
# ***********************************User variable************************
VARENVPATH_varenv = os.path.join(os.getcwd(),"ENV_file")
a = 123
b ='12343'

LOCAL_VAR = {
    'a1'              : '1',
    'b2'              : '2',
    }

def VarEnvPathGet(): return VARENVPATH_varenv

def test():
    VarEnvPathGet()

if __name__ == '__main__':
    test()
