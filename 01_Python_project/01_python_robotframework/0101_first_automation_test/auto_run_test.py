#!/usr/bin python
''' Entry point of acceptance testing '''
import os
import sys

def get_libpath():
	return os.path.join(os.path.dirname(__file__), 'libraries')

def get_suitepath():
	return os.path.join(os.path.dirname(__file__), 'test_suites')


def main():
	lib_path = get_libpath()
	suite_path = get_suitepath()

	# osPath = os.path.dirname(__file__)
	# print "osPath=%s" % osPath
	# print "lib_path=%s" % lib_path
	# print "suite_path=%s" % suite_path
	rt = os.system('pybot --pythonpath %s -L Trace %s' % (lib_path, suite_path))
	if rt != 0:
	    sys.exit(-1)


if __name__ == '__main__':
	main()
