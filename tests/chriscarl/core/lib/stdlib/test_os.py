#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-26
Description:

chriscarl.core.lib.stdlib.os unit test.

Updates:
    2024-11-26 - tests.chriscarl.core.lib.stdlib.os - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging

# third party imports

# project imports (expected to work)
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.lib.stdlib.os as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/lib/stdlib/test_os.py'
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

    def test_case_0_abspath(self):
        variables = [
            (lib.abspath, ('/tmp', 'hello', 'world')),
            (lib.abspath, ('~/tmp', 'hello', 'world')),
        ]
        controls = [
            os.path.abspath('/tmp/hello/world'),
            os.path.abspath(os.path.expanduser('~/tmp/hello/world')),
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_chdir(self):
        variables = [
            (lib.abspath, ('/tmp', 'hello', 'world')),
            (lib.abspath, ('~/tmp', 'hello', 'world')),
        ]
        controls = [
            os.path.abspath('/tmp/hello/world'),
            os.path.abspath(os.path.expanduser('~/tmp/hello/world')),
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)10s - %(filename)s - %(funcName)s - %(message)s', level=logging.DEBUG)
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_abspath()
    tc.test_case_1_chdir()

    tc.tearDown()
