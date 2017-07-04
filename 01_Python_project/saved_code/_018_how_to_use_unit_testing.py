##==================================================================================
# implement a to_int function, that convert hex string data to integer
# eg:
#     to_int('\xef')  ==> 239
#     to_int('\xef\x01')  ==> 61185
# NOTE: builtin function ord can return the integer ordinal of a one-character string
##==================================================================================

# Unit Testing
import unittest

def to_int(hexstring):
    #return 1
    #return map(ord, hexstring)[0]
    # return reduce(lambda x, y : x + y, map(ord, hexstring))
    return reduce(lambda x, y : x * 256 + y, map(ord,hexstring))

class TestToInt(unittest.TestCase):

    def test_to_int_with_one_char_string(self):
        self.assertEqual(to_int('\x01'), 1)

    def test_to_int_with_one_char_string2(self):
        self.assertEqual(to_int('\xef'), 239)
    #
    # def test_to_int_with_two_chars_string(self):
    #     self.assertEqual(to_int('\xef\x01'), 61185)
    #
    # def test_to_int_with_three_chars_string(self):
    #     self.assertEqual(to_int('\xef\x01\x01'), 15663361)
    #
    # def test_to_int_with_four_chars_string(self):
    #     self.assertEqual(to_int('\xef\xf1\x01\xef'), 4025549295)

suite = unittest.TestLoader().loadTestsFromTestCase(TestToInt)
unittest.TextTestRunner().run(suite)


aa = TestToInt()
bb = TestToInt()

aa.s