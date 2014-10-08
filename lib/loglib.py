"""
The MIT License (MIT)
Copyright (c) 2014 Mats Liljegren
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import logging
import logging.handlers
import os
import sys
import textwrap

appname = os.path.basename(__file__)

def add_arguments(parser):
    parser.add_argument('--verbose', '-v', action='count', default=0,
                    help='be verbose, can be given multiple times for extra verbosity')
    parser.add_argument('--logfile', help='write log entries to FILE',
            metavar='FILE')
    parser.add_argument('--logfile-level', default='warning',
            help=textwrap.dedent('''\
                    set verbosity level for log entries in file given by --log-file
                    default: %(default)s'''),
                    choices=['debug', 'info', 'warning', 'error', 'critical'])
    parser.add_argument('--syslog', action='store_true',
            help='enable logging to syslog')
    parser.add_argument('--syslog-level', metavar='LEVEL', default='error',
            choices=['debug', 'info', 'warning', 'error', 'critical'],
            help=textwrap.dedent('''\
                    set verbosity level for entries to syslog, if --syslog is given
                    default: %(default)s'''))

def getLogger(module_name):
        return logger.getLogger(appname + "." + module_name)

def configure(arg):

    loglevel_verbose = {
            0 : logging.ERROR,
            1 : logging.WARNING,
            2 : logging.INFO,
            3 : logging.DEBUG
    }

    if arg.verbose > 3: arg.verbose = 3

    log = logging.getLogger(os.path.basename(__file__))

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    consoleHandler.setLevel(loglevel_verbose[arg.verbose])
    log.addHandler(consoleHandler)

    if getattr(arg, 'logfile', None) != None:
        try:
            fileHandler = logging.handlers.WatchedFileHandler(os.path.expanduser(arg.logfile))
            fileHandler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
            fileHandler.setLevel(getattr(logging, arg.logfile_level.upper()))
            log.addHandler(fileHandler)
        except IOError as e:
            log.error('Could not open or create log file for append: {}'.format(e))
            sys.exit(1)

    if arg.syslog:
        try:
            sysHandle = logging.handlers.SysLogHandler()
            sysHandle.setLevel(getattr(logging, arg.syslog_level.upper()))
            log.addHandler(sysHandle)
        except Exception as e:
            log.error('Could not enable syslog: {}'.format(e))
    return log


