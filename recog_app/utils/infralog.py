#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import syslog
import time

def currentframe():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        return sys.exc_info()[2].tb_frame.f_back
_srcfile = os.path.normcase(currentframe.__code__.co_filename)

class InfraLog(object):
    DEV_NULL    = 0x00
    DEV_CONSOLE = 0x01
    DEV_FILE    = 0x01 << 1
    DEV_SYSLOG  = 0x01 << 2

    PRI_ERROR   = syslog.LOG_ERR
    PRI_WARNING = syslog.LOG_WARNING
    PRI_NOTICE  = syslog.LOG_NOTICE
    PRI_INFO    = syslog.LOG_INFO
    PRI_DEBUG   = syslog.LOG_DEBUG

    _PRI_KEYWORD_ID = {
        "ERROR"   : PRI_ERROR,
        "WARNING" : PRI_WARNING,
        "NOTICE"  : PRI_NOTICE,
        "INFO"    : PRI_INFO,
        "DEBUG"   : PRI_DEBUG
    }

    _PRI_SHORT = {
        PRI_ERROR   : "E",
        PRI_WARNING : "W",
        PRI_NOTICE  : "N",
        PRI_INFO    : "I",
        PRI_DEBUG   : "D"
    }

    _CONFIG = None
    

    @staticmethod
    def Identity(file):
        return os.path.basename(file)


    @staticmethod
    def Priority(keyword):
        keyword = keyword.upper() if keyword is not None else "NOTICE"
        return InfraLog._PRI_KEYWORD_ID[keyword] if keyword in InfraLog._PRI_KEYWORD_ID\
            else InfraLog.PRI_NOTICE


    @staticmethod
    def findCaller():
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        #On some versions of IronPython, currentframe() returns None if
        #IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            rv = (co.co_filename, f.f_lineno, co.co_name)
            break
        return rv


    @staticmethod
    def Setup(ident=None, device=None, priority=None, project=None, log_path=None):
        if InfraLog._CONFIG is not None and InfraLog._CONFIG["DEVICE"] & InfraLog.DEV_SYSLOG:
            syslog.closelog()

        InfraLog._CONFIG = {
            "IDENT"    : ident if ident is not None else "?",
            "DEVICE"   : device if device is not None else InfraLog.DEV_NULL,
            "PRIORITY" : priority if priority is not None else InfraLog.PRI_WARNING,
            "PROJECT" : project,
            "LOGPATH": log_path
        }

        if InfraLog._CONFIG["DEVICE"] & InfraLog.DEV_SYSLOG:
            syslog.openlog(InfraLog._CONFIG["IDENT"], syslog.LOG_PID, syslog.LOG_LOCAL0)
            syslog.setlogmask(syslog.LOG_UPTO(InfraLog._CONFIG["PRIORITY"]))

        return

    @staticmethod
    def Write(priority, message):
        if InfraLog._CONFIG is None \
            or "DEVICE" not in InfraLog._CONFIG \
            or InfraLog._CONFIG["DEVICE"] == InfraLog.DEV_NULL:
            return

        try:
            file_name, fno, func_name = InfraLog.findCaller()
        except ValueError:
            file_name, fno, func_name = "(unknown file)", 0, "(unknown function)"

        logmsg = "[%c][%s] %s" % (InfraLog._PRI_SHORT[priority],\
            "%s.%s"%(func_name, fno), message)
        
        if InfraLog._CONFIG["DEVICE"] & InfraLog.DEV_CONSOLE and\
             InfraLog._CONFIG["PRIORITY"] >= priority:
            print >> sys.stderr, "%s[%d]: %s" % (InfraLog._CONFIG["IDENT"], os.getpid(), logmsg)

        if InfraLog._CONFIG["DEVICE"] & InfraLog.DEV_SYSLOG:
            syslog.syslog(priority, logmsg)

        if InfraLog._CONFIG["DEVICE"] & InfraLog.DEV_FILE and\
             InfraLog._CONFIG["PRIORITY"] >= priority:
            if InfraLog._CONFIG["LOGPATH"] is None:
                logpath = "/opt/var/%s/log/%s"%(InfraLog._CONFIG["PROJECT"],\
                    time.strftime('%Y%m%d'))
            else:
                logpath = "%s/log/%s"%(os.path.join(InfraLog._CONFIG["LOGPATH"]),\
                    time.strftime('%Y%m%d'))
                logpath = os.path.abspath(logpath)
            try:
                if not os.path.exists(logpath):
                    os.makedirs(logpath)
            except IOError, e:                
                print >> sys.stderr, "InfraLog.DEV_FILE os.makedirs error - %s"%(e,)

            try:
                log_file = InfraLog._PRI_KEYWORD_ID.keys()[InfraLog._PRI_KEYWORD_ID.values().index(priority)]
                fp = open("%s/%s"%( logpath, log_file ), 'a')
                fp.write("[%s][%s(%s)]%s%s"%(time.strftime('%Y/%m/%d %H:%M:%S'), InfraLog._CONFIG["IDENT"],\
                     os.getpid(), logmsg, os.linesep))
                fp.close()
            except IOError, e:
                print >> sys.stderr, "InfraLog.DEV_FILE error - %s"%(e,)

        return


def main(argv=None):
    ident = InfraLog.Identity(__file__)
    device = InfraLog.DEV_CONSOLE | InfraLog.DEV_SYSLOG | InfraLog.DEV_FILE
    priority = InfraLog.Priority("DEBUG")
    InfraLog.Setup(ident=ident, device=device, priority=priority)

    InfraLog.Write(InfraLog.PRI_ERROR, "Testing for ERROR")
    InfraLog.Write(InfraLog.PRI_WARNING, "Testing for WARNING")
    InfraLog.Write(InfraLog.PRI_NOTICE, "Testing for NOTICE")
    InfraLog.Write(InfraLog.PRI_INFO, "Testing for INFO")
    InfraLog.Write(InfraLog.PRI_DEBUG, "Testing for DEBUG")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

