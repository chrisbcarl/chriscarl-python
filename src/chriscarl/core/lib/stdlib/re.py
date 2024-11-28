#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-27
Description:

core.lib.stdlib.re has some nice functions, usually about searching
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Updates:
    2024-11-27 - core.lib.stdlib.re - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import re
from typing import Generator, Tuple

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/re.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def find_index(find_text, within, case_insensitive=True):
    # type: (str, str, bool) -> Generator[int, None, None]
    for mo in re.finditer(find_text, within, flags=re.IGNORECASE if not case_insensitive else 0):
        yield mo.start()


def find_lineno_colno(find_text, within, case_insensitive=True):
    # type: (str, str, bool) -> Generator[Tuple[int, int], None, None]
    '''
    NOTE: line no and col no are 1-indexed
    '''
    for l, line in enumerate(within.splitlines()):
        for mo in re.finditer(find_text, line, flags=re.IGNORECASE if not case_insensitive else 0):
            yield l + 1, mo.start() + 1
