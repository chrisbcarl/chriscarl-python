#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-22
Description:

core.functors.misc is shit code that needs to be refactored and placed appropriately or removed entirely but i'm too stubborn to kill my darlings.
core.functor are modules that functions that are usually defined as lambdas, but i like to hold onto them as named funcs. non-self-referential, low-import, etc.

Updates:
    2024-11-26 - core.functors.misc - removed logging / argparse and put them correctly away
    2024-11-22 - core.functors.misc - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from pathlib import Path
from typing import Any, Tuple, Dict, List, Iterable, Union, Callable, Optional

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/functors/misc.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def ping(*args, **kwargs):
    # type: (Tuple[Any], Dict[str, Any]) -> Tuple[str, str]
    '''Test function for all modules.

    Returns:
        'pong', __name__
    '''
    return 'pong', __name__


DAYMAP = {
    "M": "Monday",
    "T": "Tuesday",
    "W": "Wednesday",
    "R": "Thursday",
    "F": "Friday",
    "S": "Saturday",
    "U": "Sunday",
}
for dick in (
    DAYMAP,
    {
        k.capitalize(): v
        for k, v in DAYMAP.items()
    },
    {
        v[0:2].lower(): v
        for k, v in DAYMAP.items()
    },
    {
        v[0:2].upper(): v
        for k, v in DAYMAP.items()
    },
):
    DAYMAP.update(dick)
for dick in (
    DAYMAP,
    {
        v: v
        for _, v in DAYMAP.items()
    },
    {
        v.lower(): v
        for _, v in DAYMAP.items()
    },
    {
        v.upper(): v
        for _, v in DAYMAP.items()
    },
):
    DAYMAP.update(dick)


def file_text(path=Path()):
    # type: (Path) -> str
    '''newlines problem: https://stackoverflow.com/a/4877358
    Args:
        path (pathlib.Path)
    Returns:
        str
    Raises:
        FileNotFoundError
        UnicodeDecodeError
    '''
    if not isinstance(path, Path):
        path = Path(path)
    with open(str(path), 'rb') as p:
        try:
            text = p.read().decode('utf-8')
            # covers the windows situation where text files have \\r\\n
            text = text.replace('\r\n', '\n')
            # covers the macOS situation where text files have \\r
            text = text.replace('\r', '\n')
            return text
        except UnicodeDecodeError as e:
            # https://gehrcke.de/2015/12/how-to-raise-unicodedecodeerror-in-python-3/
            # encoding = e[0]
            obj = e.object  # e[1]
            start = e.start  # e[2]
            end = e.end  # e[3]
            reason = e.reason  # e[4]
            encoding = e.encoding

            length = len(obj)
            if start - 32 < 0:
                start = 0
            else:
                start -= 32
            if end + 32 > length:
                end = length
            else:
                end += 32

            msg = '{} at {}, repr: {}'.format(reason, path, repr(obj[start:end]))
            raise UnicodeDecodeError(encoding, obj, start, end, reason + msg)


def locals_to_dict(locals_dict, ignore=[]):
    # type: (dict, List[str]) -> dict
    ret = {key: value for key, value in locals_dict if key not in ignore}
    return ret


def is_int(s):
    try:
        int(str(s))
        return True
    except ValueError:
        return False


# strings
def is_ascii(string):
    for char in string:
        if not ord(char) < 128:
            return False
    return True


def sanitize_ascii(string, replacement):
    newstring = ''
    for char in string:
        if ord(char) < 128:
            newstring += char
        else:
            newstring += replacement
    return newstring


def sanitize_filename(filename, spaces=False):
    if spaces:
        return "".join([c for c in filename.strip() if c.isalpha() or c.isdigit() or c == ' '])
    else:
        return "".join([c for c in filename.strip() if c.isalpha() or c.isdigit()])


# dict
def dict_inverse(dick, lst=None):
    # type: (dict, Optional[list]) -> List[Tuple[str, List[str]]]
    '''creates a (probably) true mathematical inverse of a mapping. In effect,
        this function takes in a dictionary, and for every value, creates a
        linear set of keys that it would've taken to reach it through a dict.
    Note:
        RECURSIVE, and the second arg, lst is supposed to be left as None

    Args:
        types (dict):
            ex) { 'number': { 'real': { 'floating': 'float', }  }  }
        lst (list):
            Leave as default None on first run. This function uses itself
                to recurse.

    Returns:
        list:
            ex) [
                ('float', ['number', 'real, 'floating'])
            ]
    '''

    inverse = []
    for key, value in dick.items():
        if not isinstance(value, dict):
            if lst is None:
                inverse.append((value, [key]))
            else:
                inverse.append((value, lst + [key]))
        else:
            if lst is None:
                inverse += dict_inverse(value, lst=[key])
            else:
                inverse += dict_inverse(value, lst + [key])
    return inverse


def avg(iterable):
    # type: (Iterable[Union[int, float]]) -> float
    count = 0
    total = 0.0
    for i, el in enumerate(iterable):
        try:
            count += 1
            total += el
        except TypeError:
            raise TypeError('no way to += {} at index {}'.format(el, i))
    return total / count


def fib(n):
    # type: (int) -> int
    if n == 0:
        return 0
    elif n < 3:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def fib_fast(n):
    # type: (int) -> int
    a = 0
    b = 1
    c = 1
    if n == 0:
        return a
    elif n == 1:
        return b
    elif n == 2:
        return c
    for _ in range(n - 1):
        c = a + b
        a = b
        b = c
    return c


def int_to_hex(number, width=32):
    number = int(number)
    fmt = '0x{{:0{}X}}'
    width = width // 4
    mask = '0x{}'.format('F' * width)
    mask = int(mask, base=16)
    fmt = fmt.format(width)
    return fmt.format(number & mask)


def lambda_raise(x):
    raise x


def divide_chunks(lst, n):
    '''
    https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
    '''
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
