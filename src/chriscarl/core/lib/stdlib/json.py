#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@chriscarl.com
Date:           2024-11-24
Description:

inspect is all about the framerate
core.lib.stdlib files are for utilities that make use of, but do not modify the stdlib

Updates:
    2024-11-24 - chriscarl.core.lib.stdlib.inspect - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import json
import logging
from typing import Union

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


def read_json(filepath, encoding='utf-8'):
    # type: (str, str) -> dict
    with open(filepath, 'r', encoding=encoding) as r:
        return json.load(r)


def read_json_list(filepath, encoding='utf-8'):
    # type: (str, str) -> list
    with open(filepath, 'r', encoding=encoding) as r:
        return json.load(r)


def write_json(filepath, content, encoding='utf-8', indent=4):
    # type: (str, dict, str, int) -> None
    make_file_dirpath(filepath)
    with open(filepath, 'w', encoding=encoding) as w:
        json.dump(content, w, indent=indent)


def dict_to_string(obj, indent=2):
    return json.dumps(obj, indent=indent)


json_to_string = dict_to_string
