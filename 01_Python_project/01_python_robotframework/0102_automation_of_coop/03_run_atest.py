import os
import sys

def get_libpath():
	return os.path.join(os.path.dirname(__file__), 'libraries')

def get_suitepath():
	return os.path.join(os.path.dirname(__file__), 'suites')

def main():
	lib_path = get_libpath()
	suite_path = get_suitepath()
	rt = os.system('pybot --pythonpath %s -i type-NCDR -l 03_fault_ncdr.html %s' % (lib_path, suite_path))
	if rt != 0:
		sys.exit(-1)

if __name__ == '__main__':
	main()