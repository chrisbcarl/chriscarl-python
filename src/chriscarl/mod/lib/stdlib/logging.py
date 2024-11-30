#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-29
Description:

mod.lib.stdlib.logging is... TODO: lorem ipsum
mod.lib are modules that shadow the original module, and by virtue of import, modify the original modules behavior with overrides.

Updates:
    2024-11-29 - mod.lib.stdlib.logging - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
# "shadow module" hack
if sys.path[0] == '':  # occurs in interactive mode
    __old_path = sys.path
    sys.path = sys.path[1:] + ['']
else:
    __old_path = []
# without the above hack, "import logging" would import THIS FILE rather than the intended original
import logging  # import the original unmodified module which can be used in the modifications below
# polutes this "shadow" module's locals with the original locals, allowing it to behave as normal
from logging import *  # noqa: F403
from typing import Any, Tuple, Dict

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/mod/lib/stdlib/logging.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

VERBOSE = 15
setattr(logging, 'VERBOSE', VERBOSE)

# undo "shadow module" mods
if __old_path:
    sys.path = __old_path
