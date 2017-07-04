import os
import platform
from distutils.sysconfig import get_python_lib
from subprocess import call, check_output


def exe_develop(args):
    """
    Method to execute actions related to develop command
    """
    exe_update_paths(args)
    index_num = args.index_num
    if index_num >= len(args.index_urls):
        print("%s: error: wrong index number. \nPlease type \"python psetup.py develop -h\" to see available indexes" % __file__)
        exit(1)

    for require in args.requires:
        for i in range(args.number_of_tries):
            try_message = 'Try: %d for %s' % (i + 1, require)
            print '-' * len(try_message)
            print try_message
            print '-' * len(try_message)
            #cmd = "easy_install --allow-hosts=%s --index-url=%s --upgrade %s" % (args.index_urls[index_num][0],
            cmd = "easy_install --always-unzip --index-url=%s --upgrade %s" % (args.index_urls[index_num][1],
                                                                require)
            rc = call(cmd.split())
            if not rc:
                break
            print 'Server is not available, try again\n'

        if rc:
            exit(rc)


def exe_documentation(args):
    """
    Method to execute actions to generate documentation
    """
    robotws_path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(os.path.join(robotws_path, 'doc'))
    check_output(["python", "prepare_rst.py"])
    if platform.system() == "Linux":
        check_output(["make", "html"])
    elif platform.system() == "Windows":
        check_output(["make.bat", "html"])
    os.chdir(robotws_path)


def exe_update_paths(args):
    """
    Method updates python path via .pth file to add RobotWS directories
    """
    if args.paths is None:
        return
    robotws_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    with open("%s/tdlte.pth" % get_python_lib(), "w") as f:
        f.write(robotws_path + '\n')
        for path in args.paths:
            path = os.path.normpath(os.path.join(robotws_path, path))
            f.write(path + '\n')


def exe_install(args):
    """
    Method to execute actions related to install command
    """
    exe_develop(args)
    exe_update_paths(args)


def create_indexes(index_urls):
    return "".join(["\n    [%d    """
    Method creates string with available indexes. Each index has number to identify
    """
] %s" % (i, each[1]) for i, each in enumerate(index_urls)])
