#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Carl, Chris
Email:          chrisbcarl@outlook.com
Date:           2024-11-23
Description:

Unit test for chriscarl.core.lib.stdlib.unittest

Updates:
    2024-11-23 - tests.core.lib.stdlib.test_unittest - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import time
import logging
import unittest

# third party imports

# project imports (expected to work)
from chriscarl.core.lib.stdlib.unittest import assert_null_hypothesis

# test imports

SCRIPT_RELPATH = 'tests/libraries/third/test_unittest.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class TestCase(unittest.TestCase):

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_assert_null_hypothesis(self):
        variables = [
            (print),
            (print, ''),
            (sum, ([1, 2, 3], ), {}),
            (len, ([1, 2, 3]), {}),
            (len, 1),
        ]
        controls = [
            None,
            None,
            6,
            3,
            TypeError,
        ]
        assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)10s - %(filename)s - %(funcName)s - %(msg)s', level=logging.DEBUG)
    tc = TestCase()
    tc.setUp()

    tc.test_assert_null_hypothesis()

    tc.tearDown()
