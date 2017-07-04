from argparse import ArgumentParser, RawTextHelpFormatter
from setup_commands import create_indexes, exe_develop, exe_documentation, exe_update_paths, exe_install


REQUIRES = [  
    'robotframework',
    'Pygments',
    'robotframework-ride',
    'robotframework-sshlibrary',
    'xlrd',
    'xlwt',
    'xlutils',
    'lxml',
    'pywin32',
    'pyserial',
    'pycrypto',
    'paramiko',
    'Pyro4',    
    'robotframework-selenium2library',
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
INDEX_URLS = [
    ("*", "http://10.69.81.34/static/TA_INSTALL/pypi/"),
    #("wrling37.emea.nsn-net.net*", "http://wrling37.emea.nsn-net.net:25101/ute_files/pypi/packages"),
    ("*python.org", "http://f.pypi.python.org/simple/")
]

PATHS = [""]


def _create_install(subparsers):
    """
    Specify options needed by install command line command
    """
    setup = subparsers.add_parser('install',
                                  formatter_class=RawTextHelpFormatter,
                                  description="Available server urls:%s" % create_indexes(INDEX_URLS),
                                  help="Command to setup RobotWS")
    setup.add_argument("-i", dest='index_num', default=0, type=int, help="Index number of server url (default: 0)")
    setup.add_argument("-n", dest='number_of_tries', default=5, type=int, help="Number of tries to connect to server (default: 5)")
    setup.set_defaults(func=exe_install, index_urls=INDEX_URLS, requires=REQUIRES, paths=PATHS)


def _create_update_paths(subparsers):
    """
    Specify options needed by update_paths command line command
    """
    paths = subparsers.add_parser('update_paths', help="Command to extend PYTHONPATH needed by RobotWS")
    paths.set_defaults(func=exe_update_paths, paths=PATHS)


def _create_develop(subparsers):
    """
    Specify options needed by develop command line command
    """
    dev_require = REQUIRES + REQUIRES_DEV
    setup = subparsers.add_parser('develop',
                                  formatter_class=RawTextHelpFormatter,
                                  description="Available server urls:%s" % create_indexes(INDEX_URLS),
                                  help="Command to setup RobotWS in development mode")
    setup.add_argument("-i", dest='index_num', default=0, type=int, help="Index number of server url (default: 0)")
    setup.add_argument("-n", dest='number_of_tries', default=5, type=int, help="Number of tries to connect to server (default: 5)")
    setup.set_defaults(func=exe_develop, index_urls=INDEX_URLS, requires=dev_require, paths=PATHS)


def _create_documentation(subparsers):
    """
    Specify options needed by documentation command line command
    """
    docs = subparsers.add_parser('documentation', help="Command to generate documentation")
    docs.set_defaults(func=exe_documentation)


if __name__ == "__main__":
    
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter, description='Management script for RobotWS')

    subparsers = parser.add_subparsers()
    _create_develop(subparsers)
    _create_install(subparsers)
    _create_documentation(subparsers)
    _create_update_paths(subparsers)

    args = parser.parse_args()

    args.func(args)


