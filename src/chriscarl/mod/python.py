#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-22
Description:

mod files are usually clever and brittle hacks that modify the behavior of python at runtime through the use of shadow techniques or otherwise.
mod "python" does exceptionally dangerous stuff like overriding the default hasattr and getattr functions and other wild shit

Updates:
    2024-11-22 - chriscarl.mod.python - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import atexit
import logging
import builtins

# third party imports

# project imports
from chriscarl.core.functors import python as ccf_python
from chriscarl.core.lib.stdlib import typing as cls_typing

SCRIPT_RELPATH = 'chriscarl/mod/python.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

_MODDED = False
MOD_FUNCS = {
    'hasattr': ccf_python.hasattr_deep,
    'getattr': ccf_python.getattr_deep,
    'setattr': ccf_python.setattr_deep,
    'isinstance': cls_typing.isof,
}
STD_FUNCS = {k: getattr(builtins, k) for k in MOD_FUNCS}
_setattr = setattr
_isinstance = isinstance


def mod(force=False):
    # type: (bool) -> None
    global _MODDED
    if not _MODDED or force:
        for k, v in MOD_FUNCS.items():
            _setattr(builtins, k, v)
        _MODDED = True


def unmod(force=False):
    # type: (bool) -> None
    global _MODDED
    if _MODDED or force:
        for k, v in STD_FUNCS.items():
            _setattr(builtins, k, v)
        _MODDED = False


class Mod(object):
    '''
    >>> with Mod():
    ...     pass
    '''

    def __init__(self):
        pass

    def __enter__(self):
        mod(force=True)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        unmod(force=True)


atexit.register(lambda: unmod(force=True))
