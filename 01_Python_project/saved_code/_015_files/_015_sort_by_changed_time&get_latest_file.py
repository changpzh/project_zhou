"""
**=============================================================
 * Copyright: 2012~2015
 * FullName:
 * Description:
 * Changes:
 *==============================================================
 * Date:
 * Author: changpzh
 * Comment:  sort file by changed time, and get the latest changed
 *    file
**==============================================================
"""
import os, sys

def get_last_modified_file(parent_dir, file_ext, file_pattern=""):
    """This keyword gets latest modified file in given directory,
        no matter the OS type is windows or linux.

    | Input Parameters | Man. | Description |
    | parent_dir       | Yes  | Target directory for file searching |
    | file_ext         | Yes  | File extention for file filterring |
    | file_pattern     | No   | File pattern for file filtering, default is for Counter file |

    | Return value | The absolute file path of last modified file |

    Example
    | Get Last Modified File | /root | txt |
    """
    from BtsShell.high_shell_lib.common_operation import _GetRuntimeVar
    def _GetRuntimeVar(varname):
    try:
        if not varname.startswith("${"):
            varname = "${%s}" % varname
        return BuiltIn().replace_variables(varname)
    except:
        print "Not run with robot..."
        return


    connection_type = connections.get_current_connection_type()

    if connection_type == 'Windows':
        if _GetRuntimeVar("BTS_CONTROL_PC_LAB") == connections.BTSTELNET._current.host:
            if not os.path.exists(parent_dir):
                raise Exception, 'Given path "%s" is not exists!' % parent_dir
            mtime = lambda f: os.stat(os.path.join(parent_dir, f)).st_mtime
            match_pattern = file_pattern == '' and '.' or '^.*%s' % file_pattern
            latestFiles = list(sorted([f for f in os.listdir(parent_dir) if (os.path.splitext(f)[-1] \
                                      == file_ext or f.endswith(file_ext)) and  re.match(match_pattern, f)], key=mtime, reverse=True))
            for f in latestFiles:
                print f
            if latestFiles:
                #SYSLOG_008.LOG
                UDPLOG_PAT = "SYSLOG_(\d+)\.LOG"
                if not re.match(UDPLOG_PAT, latestFiles[0].strip(), re.I):
                    latestFile = latestFiles[0]
                else:
                    if len(latestFiles) == 1:
                        latestFile = latestFiles[0]
                    else:
                        firstFileID = re.match(UDPLOG_PAT, latestFiles[0], re.I).group(1)
                        secondFileID = re.match(UDPLOG_PAT, latestFiles[1], re.I).group(1)
                        if mtime(os.path.join(parent_dir,latestFiles[0])) == mtime(os.path.join(parent_dir,latestFiles[1])):
                            if int(secondFileID) - int(firstFileID) == 1:
                                latestFile = latestFiles[1]
                            else:
                                latestFile = latestFiles[0]
                        else:
                            latestFile = latestFiles[0]
            else:
                raise Exception, 'no any files found with extention (%s) and with pattern (%s)' \
              % (file_ext, file_pattern)
            return os.path.join(parent_dir, latestFile)


        else:
            ret = connections.execute_shell_command('dir /A /B /O-D-S "%s"' % parent_dir)
            lines = ret.splitlines()
            match_pattern = file_pattern == '' and '.' or '^.*%s' % file_pattern

            for line in lines:
                try:
                    (file_name, file_extention) = line.split('.')
                    print file_extention
                    if file_extention == file_ext and re.match(match_pattern, line):
                        file_full_path = os.path.join(parent_dir, line)
                        connections.execute_shell_command('dir "%s"' % file_full_path)
                        return file_full_path
                except ValueError:
                    pass
    elif connection_type == 'Linux':
        ret = connections.execute_shell_command('ls -tl "%s"|awk \'{print $9}\'' % parent_dir)
        lines = ret.splitlines()
        match_pattern = '.*%s.*\.%s' % (file_pattern, file_ext)

        for line in lines:
            if re.search('\[0\;0m', line):
                line = re.sub('\[0\;0m', '', line)
                line = re.sub('\[0m', '', line)
            try:
                ret = re.match(match_pattern, line)
                if ret:
                    return str2unicode(line)
            except ValueError:
                pass

    raise Exception, 'no any files found with extention (%s) and with pattern (%s)' \
          % (file_ext, file_pattern)
