#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Carl, Chris
Email:          chrisbcarl@chriscarl.com
Date:           2024-11-22
Description:

"Shadow module" that "shadows" the "parameterized" module with extra functionality via side effects.

Updates:
    2024-11-22 - chriscarl.libraries.uncore.third.parameterized - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import Any, Tuple, Dict, Callable

# third party imports
try:
    import parameterized
except ImportError:
    pass  # these are mostly used for typehints only

# project imports

SCRIPT_RELPATH = 'chriscarl/libraries/third/parameterized.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def parameterized_name_func(func, param_num, param):
    # type: (Callable, int, parameterized.param) -> str
    '''
    Description:
        used during parameterized.expand and in my test cases.
            >>> class AddTestCase(unittest.TestCase):
            >>>     @parameterized.expand([
            >>>         (2, 3, 5),
            >>>         (2, 4, 5),
            >>>         (2, 3, 5),
            >>>     ], name_func=parameterized_name_func)
            >>>     def test_add(self, a, b, expected):
            >>>         self.assertEqual(a + b, expected)
    '''
    return f"{func.__name__}[{param_num}]{param.args}"
