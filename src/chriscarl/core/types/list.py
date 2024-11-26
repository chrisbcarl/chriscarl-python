#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-25
Description:

core.types.list is... TODO: lorem ipsum
core.types are modules that pertain to data structures, algorithms, conversions. non-self-referential, low-import, etc.

Updates:
    2024-11-25 - core.types.list - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import List, Union, Callable, Any, Generator

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/types/list.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def dedupe(lst):
    # type: (list) -> list
    vals = {line: 1 for line in lst}
    return list(vals.keys())


def find_index(filter, lst):
    # type: (Callable[[Any], bool], list) -> Generator[int, None, None]
    '''
    Description:
        like map and filter, use a lambda to find all of the indexes that meet that lambda
    '''
    for i, x in enumerate(lst):
        if filter(x):
            yield i


def frequency_table(lst):
    # type: (list) -> Union[dict, Any]
    frequency = {}
    for ele in lst:
        if ele not in frequency:
            frequency[ele] = 0
        frequency[ele] += 1
    return frequency


def generate_list_by_frequency(lst, ascending=True):
    # type: (list, bool) -> Generator[Any, None, None]
    frequency = frequency_table(lst)
    for k, v in sorted(frequency.items(), key=lambda tpl: tpl[1], reverse=not ascending):
        yield k


def sorted_list_by_frequency(lst, ascending=True):
    # type: (list, bool) -> List[Any]
    return list(generate_list_by_frequency(lst, ascending=ascending))
