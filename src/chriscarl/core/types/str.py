#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-26
Description:

core.types.str is... TODO: lorem ipsum
core.types are modules that pertain to data structures, algorithms, conversions. non-self-referential, low-import, etc.

Updates:
    2024-11-26 - core.types.str - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import Generator, Union
from collections import OrderedDict

# third party imports

# project imports
from chriscarl.core.types.list import contains

SCRIPT_RELPATH = 'chriscarl/core/types/str.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

FILE_SIZE_UNITS = OrderedDict({'p': 5, 't': 4, 'g': 3, 'm': 2, 'k': 1})
FILE_SIZE_UNITS['b'] = 0  # so that this is searched last
for k in list(FILE_SIZE_UNITS.keys()):
    if k != 'b':
        v = FILE_SIZE_UNITS[k]
        FILE_SIZE_UNITS['{}b'.format(k)] = v
BYTES_TO_SIZE_UNITS = ['b', 'k', 'm', 'g', 't', 'p']


def find_index(search, text):
    # type: (str, str) -> Generator[int, None, None]
    len_search = len(search)
    for c, char in enumerate(text):
        if c + len_search > len(text):
            break
        if char == search[0] and text[c:c + len_search] == search:
            yield c


def size_to_bytes(size, into='b'):
    # type: (str, str) -> float
    '''
    Description:
        >>> size_to_bytes('512mb') -> 536870912.0
        >>> size_to_bytes('512mb', into='g') -> 0.5
    '''
    into = into.lower()
    if into[-1] == 's':
        into = into[0:-1]
    contains(FILE_SIZE_UNITS, into)

    size = str(size).lower().replace(' ', '')
    for unit in FILE_SIZE_UNITS:
        if unit in size:
            numeric = size.split(unit)[0]
            num = float(numeric)
            exponent = FILE_SIZE_UNITS[unit]
            num_bytes = num * 1024**exponent
            into_magnitude = (1024**FILE_SIZE_UNITS[into])
            return num_bytes / into_magnitude

    return int(size, base=0)


def bytes_to_size(size, upper=False):
    # type: (Union[int, float], bool) -> str
    '''
    # https://github.com/x4nth055/pythoncode-tutorials/blob/master/general/process-monitor/process_monitor.py
    Returns size of bytes in a nice format
    '''
    units = BYTES_TO_SIZE_UNITS if not upper else [e.upper() for e in BYTES_TO_SIZE_UNITS]
    for unit in units:
        if size < 1024:
            return '{:.2f}{}'.format(size, unit)
        size /= 1024
    return ''  # this will never hit
