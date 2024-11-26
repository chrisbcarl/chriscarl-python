#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@chriscarl.com
Date:           2024-11-24
Description:

core.lib.stdlib.os is all about file system traversal
core.lib.stdlib files are for utilities that make use of, but do not modify the stdlib

Updates:
    2024-11-26 - core.lib.stdlib.os - added chdir context manager
    2024-11-24 - core.lib.stdlib.os - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/os.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def abspath(*paths):
    # type: (str) -> str
    return os.path.abspath(os.path.expanduser(os.path.join(*paths)))


def dirpath(*paths):
    # type: (str) -> str
    abs_ = abspath(*paths)
    return os.path.dirname(abs_)


def make_dirpath(*paths):
    dp = abspath(*paths)
    if not os.path.isdir(dp):
        os.makedirs(dp)


def make_file_dirpath(*paths):
    dp = dirpath(*paths)
    if not os.path.isdir(dp):
        os.makedirs(dp)


class chdir(object):
    '''
    >>> with ContextManager('/tmp'):
    ...     os.chdir('/temp)
    '''
    pwd = ''
    _pwd = ''

    def __init__(self, pwd):
        self.pwd = pwd

    def __enter__(self):
        self._pwd = os.getcwd()
        os.chdir(self.pwd)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        os.chdir(self._pwd)
