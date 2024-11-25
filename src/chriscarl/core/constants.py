#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-22
Description:

Core files are non-self-referential, do very little importing, and define the bedrock from which other things do import.
Constants are useful from lots of contexts

Updates:
    2024-11-22 - chriscarl.core.constants - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import datetime
from typing import Any, Tuple, Dict, List, Iterable, Union

# third party imports

# project imports
import chriscarl

SCRIPT_RELPATH = 'chriscarl/core/constants.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

MODULE_DIRPATH = os.path.abspath(os.path.dirname(chriscarl.__file__))
PYPA_SRC_DIRPATH = os.path.join(MODULE_DIRPATH, '../')
REPO_DIRPATH = os.path.join(PYPA_SRC_DIRPATH, '../')
TESTS_DIRPATH = os.path.join(REPO_DIRPATH, 'tests')
CWD = os.getcwd()
NOW = datetime.datetime.now()
DATE = NOW.strftime('%Y-%m-%d')
TIME = NOW.strftime('%H:%M:%S.%f')
