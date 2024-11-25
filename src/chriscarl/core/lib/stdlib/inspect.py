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
import inspect
import logging
from typing import Any, Set

# third party imports

# project imports

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


def get_variable_names(var, stack_frames=-1):
    # type: (Any, int) -> Set[str]
    '''
    https://stackoverflow.com/a/18425523
    '''
    names = []
    if stack_frames < 1:
        for frame_tuple in inspect.stack():
            frame = frame_tuple[0]
            names += [k for k, v in frame.f_locals.items() if v is var]
    else:
        for i, frame_tuple in enumerate(inspect.stack()):
            frame = frame_tuple[0]
            if i == stack_frames:
                names = [k for k, v in frame.f_locals.items() if v is var]
                break
    if len(names) == 0:
        names.append('<anonymous>')
    return set(names)
