#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-26
Description:

chriscarl.core.lib.stdlib.io unit test.

Updates:
    2024-11-26 - tests.chriscarl.core.lib.stdlib.io - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest

# third party imports

# project imports (expected to work)
from chriscarl.core.constants import TEST_COLLATERAL_DIRPATH
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.lib.stdlib.io as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/lib/stdlib/test_io.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class TestCase(UnitTest):

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_case_0_unicode_throw(self):
        utf8 = abspath(TEST_COLLATERAL_DIRPATH, 'utf-8')
        utf16le = abspath(TEST_COLLATERAL_DIRPATH, 'utf-16-le')
        self.assertRaises(UnicodeDecodeError, lib.read_text_file, utf16le)
        variables = [
            (lib.read_text_file, (utf8, ), dict(encoding='utf-8')),
            (lib.read_text_file, (utf16le, ), dict(encoding='utf-16-le')),
        ]
        controls = [
            'hello world',
            '\ufeffhello world',
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_unicode_throw()

    tc.tearDown()
