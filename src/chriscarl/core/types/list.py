#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-25
Description:

core.types.list is all about these array-lists.
core.types are modules that pertain to data structures, algorithms, conversions. non-self-referential, low-import, etc.

Updates:
    2025-01-01 - core.types.list - added n_sized_chunks and n_chunks
    2024-12-09 - core.types.list - added as_list and contains
    2024-11-25 - core.types.list - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import List, Union, Callable, Any, Generator, Iterable

# third party imports

# project imports
from chriscarl.core.lib.stdlib.typing import T_TYPING, isinstance_raise
from chriscarl.core.lib.stdlib.inspect import get_caller_file_lineno

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


def as_list(obj_or_list, typing):
    # type: (Union[list, object], T_TYPING) -> List[Any]
    if not isinstance(obj_or_list, list):
        obj_or_list = [obj_or_list]
    isinstance_raise(obj_or_list, typing)
    return obj_or_list


def contains(choices, value_or_values):
    # type: (Iterable, Union[Any, Iterable]) -> None
    '''
    Description:
        does left side contain all of the right side?
    Raises:
        ValueError
    '''
    # NOTE: can't really use set, since set requires hashable, and who knows whats inside "choices"
    relpath, lineno = get_caller_file_lineno()
    choices = list(choices)  # helps to flatten iterators and sets and other things

    if not isinstance(value_or_values, (list, set, tuple)):
        if value_or_values not in choices:
            raise ValueError('"{}", line {} - provided value {!r} not in: {}'.format(relpath, lineno, value_or_values, choices))
    else:
        for i, v in enumerate(value_or_values):
            if v not in choices:
                raise ValueError('"{}", line {} - provided value {!r} at at index {} not in: {}'.format(relpath, lineno, v, i, choices))


def n_sized_chunks(lst, n):
    # type: (list, int) -> Generator[list, None, None]
    '''
    https://stackoverflow.com/a/312464
    '''
    if n < 1:
        raise ValueError('how can you divide a list into {} sized chunks... idiot'.format(n))
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def n_chunks(lst, n):
    # type: (list, int) -> Generator[list, None, None]
    '''
    if I want to divide 0, 1, 2, 3, 4 into 3 chunks, i'd expect 01, 23, 4 or 0, 12, 34
    '''
    if n < 1:
        raise ValueError('how can you divide a list into {} chunks... idiot'.format(n))
    i = 0
    even = len(lst) % n == 0
    size = len(lst) // n if even else len(lst) // n + 1
    while i < len(lst):
        yield lst[i:i + size]
        i += size
        if not even and size - 1 > 0 and (len(lst) - i) % (size - 1) == 0:  # if remaining list is divisible by dropping down chunk lenght, do it
            size -= 1
            even = True
