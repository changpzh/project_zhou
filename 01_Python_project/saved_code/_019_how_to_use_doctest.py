# -*- coding:utf-8 -*-
#!/usr/bin/python

# #=========================================
# below command teach you how to use doctest
# "_019_how_to_use_doctest" this is file name
# #=========================================

def square(x):
    '''
    :param x:
    :return: x * x
    >>> square(2)
    4
    >>> square(3)
    9
    >>> square(4)
    18
    '''
    return x*x

if __name__ == '__main__':
    import doctest, _019_how_to_use_doctest
    doctest.testmod(_019_how_to_use_doctest)
