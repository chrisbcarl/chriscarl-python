#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-26
Description:

chriscarl.core.lib.stdlib.collections unit test.

Updates:
    2024-11-26 - tests.chriscarl.core.lib.stdlib.collections - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest
import collections

# third party imports

# project imports (expected to work)
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.lib.stdlib.collections as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/lib/stdlib/test_collections.py'
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
        self.od = collections.OrderedDict([(1, 1), (2, 2)])
        self.ud = {1: 1, 2: 2}
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_case_0_unordered_dict(self):
        variables = [
            (lib.unordered_dict, self.od),
            (lib.unordered_dict, [self.od, self.od]),
            (lib.compare_ordered_dict, (self.od, self.ud)),
            (lib.compare_ordered_dict, ([self.od, self.od], [self.ud, self.ud])),
        ]
        controls = [
            self.ud,
            [self.ud, self.ud],
            True,
            True,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_namedtuple_with_defaults(self):
        Node = lib.namedtuple_with_defaults('Node', 'val left right', [1, 2, 3])
        n = Node()

        variables = [
            (getattr, 'val'),
            (getattr, 'left'),
            (getattr, 'right'),
        ]
        controls = [
            1,
            2,
            3,
        ]


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)10s - %(filename)s - %(funcName)s - %(message)s', level=logging.DEBUG)
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_unordered_dict()
    tc.test_case_1_namedtuple_with_defaults()

    tc.tearDown()
