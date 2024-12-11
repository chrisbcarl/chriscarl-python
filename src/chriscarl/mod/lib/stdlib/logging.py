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
    2024-12-11 - mod.lib.stdlib.logging - removed _logger_function_factory and replaced them explicitly for better stubgen
    2024-12-09 - mod.lib.stdlib.logging - small refactors
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
import chriscarl.core.lib.stdlib.logging as lib

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

# easy and quick ones to override
logging._defaultFormatter = lib.SuccinctFormatter()
logging.Formatter = lib.SuccinctFormatter

# https://stackoverflow.com/a/13638084
SUCCESS = 69
setattr(logging, 'SUCCESS', SUCCESS)
CRITICAL = 50
ERROR = 40
IMPORTANT = 35
setattr(logging, 'IMPORTANT', IMPORTANT)
WARNING = 30
INFORM = 25
setattr(logging, 'INFORM', INFORM)
INFO = 20
VERBOSE = 15
setattr(logging, 'VERBOSE', VERBOSE)
DEBUG = 10
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

NEW_NAME_TO_LEVEL = {
    'SUCCESS': SUCCESS,
    'IMPORTANT': IMPORTANT,
    'VERBOSE': VERBOSE,
    'DIFFUSE': DIFFUSE,
    'PROLIX': PROLIX,
}  # type: Dict[str, int]

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
}  # type: Dict[str, int]
setattr(logging, 'NAME_TO_LEVEL', NAME_TO_LEVEL)
lib.NAME_TO_LEVEL.update(NAME_TO_LEVEL)
LEVEL_TO_NAME = {v: k for k, v in NAME_TO_LEVEL.items()}  # type: Dict[int, str]
setattr(logging, 'LEVEL_TO_NAME', LEVEL_TO_NAME)
lib.LEVEL_TO_NAME.update(LEVEL_TO_NAME)
if sys.version_info[0] == 2:
    logging._levelNames.update(NAME_TO_LEVEL)
    logging._levelNames.update(LEVEL_TO_NAME)
else:
    logging._nameToLevel.update(NAME_TO_LEVEL)
    logging._levelToName.update(LEVEL_TO_NAME)

setattr(logging.Logger, '_default_makeRecord', logging.Logger.makeRecord)
setattr(logging.Logger, 'makeRecord', lib.Logger_makeRecord)


class Logger(logging.Logger):

    def success(self, msg, *args, **kwargs):
        if self.isEnabledFor(SUCCESS):
            self._log(SUCCESS, msg, args, **kwargs)

    def important(self, msg, *args, **kwargs):
        if self.isEnabledFor(IMPORTANT):
            self._log(IMPORTANT, msg, args, **kwargs)

    def inform(self, msg, *args, **kwargs):
        if self.isEnabledFor(INFORM):
            self._log(INFORM, msg, args, **kwargs)

    def verbose(self, msg, *args, **kwargs):
        if self.isEnabledFor(VERBOSE):
            self._log(VERBOSE, msg, args, **kwargs)

    def diffuse(self, msg, *args, **kwargs):
        if self.isEnabledFor(DIFFUSE):
            self._log(DIFFUSE, msg, args, **kwargs)

    def prolix(self, msg, *args, **kwargs):
        if self.isEnabledFor(PROLIX):
            self._log(PROLIX, msg, args, **kwargs)


logging.setLoggerClass(Logger)
logging._loggerClass = Logger  # type: ignore


class RootLogger(Logger):
    """
    A root logger is not that different to any other logger, except that
    it must have a logging level and there is only one instance of it in
    the hierarchy.
    """

    def __init__(self, level):
        """
        Initialize the logger with the name "root".
        """
        Logger.__init__(self, "root", level)

    def __reduce__(self):
        return logging.getLogger, ()


Logger.manager.setLoggerClass(Logger)
Logger.manager.root = logging.root = root = RootLogger(logging.WARNING)
Logger.manager = logging.Manager(Logger.root)


def success(msg, *args, **kwargs):
    if len(logging.root.handlers) == 0:
        logging.basicConfig()
    root.success(msg, *args, **kwargs)


def important(msg, *args, **kwargs):
    if len(logging.root.handlers) == 0:
        logging.basicConfig()
    root.important(msg, *args, **kwargs)


def inform(msg, *args, **kwargs):
    if len(logging.root.handlers) == 0:
        logging.basicConfig()
    root.inform(msg, *args, **kwargs)


def verbose(msg, *args, **kwargs):
    if len(logging.root.handlers) == 0:
        logging.basicConfig()
    root.verbose(msg, *args, **kwargs)


def diffuse(msg, *args, **kwargs):
    if len(logging.root.handlers) == 0:
        logging.basicConfig()
    root.diffuse(msg, *args, **kwargs)


def prolix(msg, *args, **kwargs):
    if len(logging.root.handlers) == 0:
        logging.basicConfig()
    root.prolix(msg, *args, **kwargs)


setattr(logging, 'success', success)
setattr(logging, 'important', important)
setattr(logging, 'inform', inform)
setattr(logging, 'verbose', verbose)
setattr(logging, 'diffuse', diffuse)
setattr(logging, 'prolix', prolix)

# undo "shadow module" mods
if __old_path:
    sys.path = __old_path
