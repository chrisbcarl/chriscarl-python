#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-25
Description:

chriscarl.core.types.list unit test.

Updates:
    2024-11-25 - tests.chriscarl.core.types.list - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest

# third party imports

# project imports (expected to work)
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.types.list as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/types/test_list.py'
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
        self.num_list = [1, 2, 2, 3, 3, 3]
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_case_0_dedupe(self):
        variables = [
            (lib.dedupe, self.num_list),
        ]
        controls = [
            [1, 2, 3],
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_find_index(self):
        variables = [
            (lib.find_index, (lambda x: x > 0, self.num_list)),
            (lib.find_index, (lambda x: x > 1, self.num_list)),
            (lib.find_index, (lambda x: x > 2, self.num_list)),
        ]
        controls = [
            [i for i, ele in enumerate(self.num_list) if ele > 0],
            [i for i, ele in enumerate(self.num_list) if ele > 1],
            [i for i, ele in enumerate(self.num_list) if ele > 2],
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2_sorted_list_by_frequency(self):
        variables = [
            (lib.sorted_list_by_frequency, self.num_list, dict(ascending=True)),
            (lib.sorted_list_by_frequency, self.num_list, dict(ascending=False)),
        ]
        controls = [
            [1, 2, 3],
            [3, 2, 1],
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)10s - %(filename)s - %(funcName)s - %(message)s', level=logging.DEBUG)
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_dedupe()
    tc.test_case_1_find_index()
    tc.test_case_2_sorted_list_by_frequency()

    tc.tearDown()
