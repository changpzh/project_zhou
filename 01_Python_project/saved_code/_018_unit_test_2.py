# -*- coding:utf-8 -*-
#!/usr/bin/python

# unittest lib can be find from below link.
# https://docs.python.org/2.7/library/unittest.html

import unittest, unit_test_zhou
class TestToInt(unittest.TestCase):
    '''
    ##==================================================================================
    # implement a to_int function, that convert hex string data to integer
    # eg:
    #     to_int('\xef')  ==> 239
    #     to_int('\xef\x01')  ==> 61185
    #     to_int('\xef\x01\01')  ==> 15663361
    # NOTE: builtin function ord can return the integer ordinal of a one-character string
    ##==================================================================================
    '''

    # def setUp(self):
    #     self.widget = Widget('The widget')
    #
    # def tearDown(self):
    #     self.widget.dispose()
    #     self.widget = None

    def test_one_char_to_int(self):
        self.assertEqual(unit_test_zhou.to_int('\x01'), 1)

    def test_one_char_to_int_2(self):
        self.assertEqual(unit_test_zhou.to_int('\xef'), 239)

    def test_one_char_to_int_3(self):
        self.assertEqual(unit_test_zhou.to_int('\xff'), 255)

    def test_two_char_to_int(self):
        self.assertEqual(unit_test_zhou.to_int('\xef\x01'), 61185)

    def test_three_char_to_int(self):
        self.assertEqual(unit_test_zhou.to_int('\xef\x01\01'), 15663361)

if __name__ == '__main__':
    unittest.main()

