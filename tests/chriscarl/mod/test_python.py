#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-23
Description:

Unit test for mod.python

Updates:
    2024-11-23 - tests.mod.test_case_0_python - initial commit
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
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
from chriscarl.core.functors import python as cp
from chriscarl.mod import python as mp

SCRIPT_RELPATH = 'tests/chriscarl/mod/test_python.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class A():
    a = 1
    val = 1

    def __str__(self):
        return 'A<[{}]({})>'.format(self.a, self.val)


class B():
    b = 2
    val = 2

    def __str__(self):
        return 'B<[{}]({})>'.format(self.b, self.val)


class C(A, B):
    c = 3

    def __init__(self, a2val=1, b2val=2):
        super().__init__()
        self.a2 = A()
        self.a2.val = a2val
        self.b2 = B()
        self.b2.val = b2val

    def __str__(self):
        return 'A<[{},{},{}]({})+{}+{}>'.format(self.c, self.b, self.c, self.val, self.a2, self.b2)


class TestCase(UnitTest):

    def setUp(self):
        self.a = A()
        self.b = B()
        self.c = C()
        self.c1 = C()
        self.c2 = C(b2val=3)
        return super().setUp()

    def tearDown(self):
        mp.unmod(force=True)
        return super().tearDown()

    # @unittest.skip('TODO: pytest freaks out on mod')
    def test_case_0_hasgetset_attr_mod(self):
        assert hasattr.__name__ != cp.hasattr_deep.__name__, 'hack uninitiated'
        mp.mod(force=True)
        assert hasattr.__name__ == cp.hasattr_deep.__name__, 'hack complete'
        variables = [
            (hasattr, (self, 'c1.a2.val')),
            (setattr, (self, 'c1.a2.val', 70)),
            (getattr, (self, 'c1.a2.val')),
        ]
        controls = [
            True,
            None,
            70,
        ]
        self.assert_null_hypothesis(variables, controls)
        mp.unmod(force=True)

    # @unittest.skip('TODO: pytest freaks out on mod')
    def test_case_1_hasgetset_attr_mod_context(self):
        assert hasattr.__name__ != cp.hasattr_deep.__name__, 'hack uninitiated'
        with mp.Mod():
            assert hasattr.__name__ == cp.hasattr_deep.__name__, 'hack complete'
            variables = [
                (hasattr, (self, 'c2.b2.val')),
                (setattr, (self, 'c2.b2.val', 71)),
                (getattr, (self, 'c2.b2.val')),
            ]
            controls = [
                True,
                None,
                71,
            ]
            self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)10s - %(filename)s - %(funcName)s - %(message)s', level=logging.DEBUG)
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_hasgetset_attr_mod()
    tc.test_case_1_hasgetset_attr_mod_context()

    tc.tearDown()
