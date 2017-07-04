#!/user/bin/env python
# -*- coding: utf-8 -*-


def safe_float1(obj):
    '''save version of float()'''
    try:
        retval = float(obj)
    except ValueError,error_reason:
        retval = "could not convert non-number to float:",error_reason
    except TypeError, diag:
        retval = str(diag)
    return retval

def safe_float2(obj):
    '''save version of float()'''
    try:
        retval = float(obj)
    except (ValueError, TypeError), diag:
        # retval = "argument must be a number or numeric string!", diag
        retval = str(diag)
    except Exception, e:
        retval = "other Error:", e
    return retval

if __name__ == '__main__':
    safe_float1()
    safe_float2()
