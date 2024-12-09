#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-12-09
Description:

mod.all is... TODO: lorem ipsum
mod are modules that use clever and brittle hacks that modify behavior at runtime via side effect through the use of eval, exec, shadow techniques, and otherwise.

Updates:
    2024-12-09 - mod.all - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import importlib

# third party imports

# project imports
[importlib.import_module(__mod) for __mod in [
    'chriscarl.mod.python',
    'chriscarl.mod.lib.stdlib.logging',
    'chriscarl.mod.lib.third.tomllib',
]]

SCRIPT_RELPATH = 'chriscarl/mod/all.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

# THIS IS IT, THERE IS NOTHING MORE
