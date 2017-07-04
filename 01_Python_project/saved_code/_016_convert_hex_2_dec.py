## -*- coding: utf-8 -*-
#!/usr/bin/python
##===============================================================
# implement a to_int function, that convert hex string data to integer
# eg:
#     to_int('\xef')  ==> 239
#     to_int('\xef\x01')  ==> 61185
# NOTE: builtin function ord can return the integer ordinal of a one-character string
##===============================================================

def hex_to_int(hexstring):
    return reduce(lambda x, y : x * 256 + y, map(ord,hexstring))
    # >>> map(ord,'\xef\x02')
    # [239, 2]
    # >>> ord('\x02')
    # 2
    # >>> ord('\xef')
    # 239
def test():
    print(to_int('\xef'))
    print(to_int('\xef\x01'))
