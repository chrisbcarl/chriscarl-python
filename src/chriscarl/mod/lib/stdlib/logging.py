#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-29
Description:

mod.lib.stdlib.logging augments logging with new constants, functions, and helpers
mod.lib are modules that shadow the original module, and by virtue of import, modify the original modules behavior with overrides.

Updates:
    2024-12-04 - mod.lib.stdlib.logging - properly added my log levels
    2024-11-29 - mod.lib.stdlib.logging - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
# "shadow module" hack
if sys.path[0] == '':  # occurs in interactive mode
    __old_path = sys.path
    sys.path = sys.path[1:] + ['']
else:
    __old_path = []
# without the above hack, "import logging" would import THIS FILE rather than the intended original
import logging  # import the original unmodified module which can be used in the modifications below
# polutes this "shadow" module's locals with the original locals, allowing it to behave as normal
from logging import *  # noqa: F403
from typing import Any, Tuple, Dict

# third party imports
from six import string_types

# project imports

SCRIPT_RELPATH = 'chriscarl/mod/lib/stdlib/logging.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

# https://stackoverflow.com/a/13638084
SUCCESS = 69
setattr(logging, 'SUCCESS', SUCCESS)
# CRITICAL: 50
# ERROR: 40
IMPORTANT = 35
setattr(logging, 'IMPORTANT', IMPORTANT)
# WARNING: 30
INFORM = 25
setattr(logging, 'INFORM', INFORM)
# INFO: 20
VERBOSE = 15
setattr(logging, 'VERBOSE', VERBOSE)
# DEBUG: 10
DIFFUSE = 5
setattr(logging, 'DIFFUSE', DIFFUSE)
PROLIX = 1
setattr(logging, 'PROLIX', PROLIX)

logging.addLevelName(SUCCESS, 'SUCCESS')
logging.addLevelName(IMPORTANT, 'IMPORTANT')
logging.addLevelName(INFORM, 'INFORM')
logging.addLevelName(VERBOSE, 'VERBOSE')
logging.addLevelName(DIFFUSE, 'DIFFUSE')
logging.addLevelName(PROLIX, 'PROLIX')

NAME_TO_LEVEL = {
    'SUCCESS': SUCCESS,
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'IMPORTANT': IMPORTANT,
    'INFO': logging.INFO,
    'VERBOSE': VERBOSE,
    'DEBUG': logging.DEBUG,
    'DIFFUSE': DIFFUSE,
    'PROLIX': PROLIX,
}
setattr(logging, 'NAME_TO_LEVEL', NAME_TO_LEVEL)
LEVEL_TO_NAME = {v: k for k, v in NAME_TO_LEVEL.items()}
setattr(logging, 'LEVEL_TO_NAME', LEVEL_TO_NAME)


def _logger_function_factory(level):
    '''do not modify or suffer death.'''

    def _logger_function(self, message, *args, **kwargs):
        if self.isEnabledFor(level):
            self._log(level, message, args, **kwargs)

    return _logger_function


class LoggerMod(logging.Logger):
    success = _logger_function_factory(SUCCESS)
    important = _logger_function_factory(IMPORTANT)
    inform = _logger_function_factory(INFORM)
    verbose = _logger_function_factory(VERBOSE)
    diffuse = _logger_function_factory(DIFFUSE)
    prolix = _logger_function_factory(PROLIX)


logging._loggerClass = LoggerMod  # type: ignore


class RootLoggerMod(LoggerMod):
    """
    A root logger is not that different to any other logger, except that
    it must have a logging level and there is only one instance of it in
    the hierarchy.
    """

    def __init__(self, level):
        """
        Initialize the logger with the name "root".
        """
        LoggerMod.__init__(self, "root", level)

    def __reduce__(self):
        return logging.getLogger, ()


LoggerMod.root = logging.root = root = RootLoggerMod(logging.WARNING)
LoggerMod.manager = logging.Manager(LoggerMod.root)
logging.Logger = LoggerMod


def _logging_function_factory(level):
    '''do not modify or suffer death.'''

    name = LEVEL_TO_NAME.get(level, 'PROLIX').lower()

    def _loging_function(msg, *args, **kwargs):
        '''
        Log a message with severity 'DEBUG' on the root logger. If the logger has
        no handlers, call basicConfig() to add a console handler with a pre-defined
        format.
        '''
        if len(logging.root.handlers) == 0:
            logging.basicConfig()
        getattr(logging.root, name)(msg, *args, **kwargs)

    return _loging_function


success = _logging_function_factory(SUCCESS)
important = _logging_function_factory(IMPORTANT)
inform = _logging_function_factory(INFORM)
verbose = _logging_function_factory(VERBOSE)
diffuse = _logging_function_factory(DIFFUSE)
prolix = _logging_function_factory(PROLIX)

setattr(logging, 'success', success)
setattr(logging, 'important', important)
setattr(logging, 'inform', inform)
setattr(logging, 'verbose', verbose)
setattr(logging, 'diffuse', diffuse)
setattr(logging, 'prolix', prolix)

if sys.version_info[0] == 2:
    LEVELS = [k for k in logging._levelNames.keys() if isinstance(k, string_types)]
else:
    LEVELS = list(logging._nameToLevel.keys())
setattr(logging, 'LEVELS', LEVELS)

setattr(logging.Logger, '_default_makeRecord', logging.Logger.makeRecord)
if sys.version_info[0] == 2:

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None):
        '''
        # C:\\Python27\\lib\\logging\\__init__.py', line 1270
        A factory method which can be overridden in subclasses to create
        specialized LogRecords.
        '''
        rv = logging.LogRecord(name, level, fn, lno, msg, args, exc_info, func)
        if extra is not None:
            for key in extra:
                # allow this, see def ssh()
                # if (key in ['message', 'asctime']) or (key in rv.__dict__):
                #     raise KeyError('Attempt to overwrite %r in LogRecord' % key)
                rv.__dict__[key] = extra[key]
        return rv
else:

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        '''
        C:\\Python36\\lib\\logging\\__init__.py, line 1406
        A factory method which can be overridden in subclasses to create
        specialized LogRecords.
        '''
        rv = logging._logRecordFactory(name, level, fn, lno, msg, args, exc_info, func, sinfo)
        if extra is not None:
            for key in extra:
                # allow this, see def ssh()
                # if (key in ['message', 'asctime']) or (key in rv.__dict__):
                #     raise KeyError('Attempt to overwrite %r in LogRecord' % key)
                rv.__dict__[key] = extra[key]
        return rv


setattr(logging.Logger, 'makeRecord', makeRecord)

# undo "shadow module" mods
if __old_path:
    sys.path = __old_path
