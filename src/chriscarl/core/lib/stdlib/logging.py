#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-26
Description:

core.lib.stdlib.logging is one of the most pivotal libraries and largely informs how its shadow module counterpart is implemented
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Updates:
    2024-11-26 - core.lib.stdlib.logging - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import functools
from typing import Union, Callable

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/logging.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

LOG_LEVELS = list(logging._nameToLevel)  # pylint: disable=(protected-access)


def get_log_func(log_level='DEBUG'):
    # type: (Union[str, int]) -> Callable
    if isinstance(log_level, str):
        log_level_int = logging._nameToLevel.get(log_level, 1)
        if log_level_int != 1:
            return getattr(logging, log_level.lower())
    else:
        log_level_int = log_level
    log = functools.partial(logging.log, log_level_int)
    return log
