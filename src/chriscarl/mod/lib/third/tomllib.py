#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-12-04
Description:

mod.lib.third.tomllib augments logging with new constants, functions, and helpers
mod.lib are modules that shadow the original module, and by virtue of import, modify the original modules behavior with overrides.

Updates:
    2024-12-04 - mod.lib.third.tomllib - initial commit
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
try:
    # without the above hack, "import tomllib" would import THIS FILE rather than the intended original
    import tomllib  # import the original unmodified module which can be used in the modifications below
    # polutes this "shadow" module's locals with the original locals, allowing it to behave as normal
    from tomllib import *  # noqa: F403
except ImportError:
    import tomli as tomllib
import logging
from typing import Any, Tuple, Dict

# third party imports
import tomli_w
from tomli_w import *  # noqa: F403

# project imports

SCRIPT_RELPATH = 'chriscarl/mod/lib/third/tomllib.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

dump = tomli_w.dump
dumps = tomli_w.dumps

setattr(tomllib, 'dump', dump)
setattr(tomllib, 'dumps', dumps)

# undo "shadow module" mods
if __old_path:
    sys.path = __old_path
