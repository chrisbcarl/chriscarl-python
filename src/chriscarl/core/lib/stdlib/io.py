#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@chriscarl.com
Date:           2024-11-24
Description:

io is all about basic input/output operations
core.lib.stdlib files are for utilities that make use of, but do not modify the stdlib

Updates:
    2024-11-24 - chriscarl.core.lib.stdlib.inspect - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging

# third party imports

# project imports
from chriscarl.core.lib.stdlib.os import make_file_dirpath

SCRIPT_RELPATH = 'chriscarl/core/functors/python.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def read_text_file(filepath, encoding='utf-8'):
    # type: (str, str) -> str
    with open(filepath, 'r', encoding=encoding) as r:
        return r.read()


def read_bytes_file(filepath):
    # type: (str) -> bytes
    with open(filepath, 'rb') as rb:
        return rb.read()


def write_text_file(filepath, content, encoding='utf-8'):
    # type: (str, str, str) -> int
    make_file_dirpath(filepath)
    with open(filepath, 'w', encoding=encoding) as w:
        return w.write(content)


def write_bytes_file(filepath, content):
    # type: (str, bytes) -> int
    make_file_dirpath(filepath)
    with open(filepath, 'wb') as wb:
        return wb.write(content)
