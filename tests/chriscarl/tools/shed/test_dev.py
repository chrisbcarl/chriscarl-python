#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-25
Description:

chriscarl.tools.shed.dev unit test.

Updates:
    2024-11-25 - tests.chriscarl.tools.shed.dev - initial commit
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
import chriscarl.tools.shed.dev as lib

SCRIPT_RELPATH = 'tests/chriscarl/tools/shed/test_dev.py'
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

    def test_create_modules_and_tests(self):
        variables = [
            (sum, [0, 1, 2, 3]),
            (sum, [0, 1, 2, 3]),
        ]
        controls = [
            6,
            6,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_audit_manifest_verify(self):
        variables = [
            (lib.audit_manifest_verify),
        ]
        controls = [
            True,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_audit_manifest_modify(self):
        from chriscarl.core.lib.stdlib.io import read_bytes_file
        original = read_bytes_file(lib.__file__)
        lib.audit_manifest_modify()
        new = read_bytes_file(lib.__file__)
        self.assertEqual(original, new, '_self_modify should take effect but be idempotent! something changed, check the git diff?')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)10s - %(filename)s - %(funcName)s - %(message)s', level=logging.DEBUG)
    tc = TestCase()
    tc.setUp()

    tc.test_create_modules_and_tests()
    tc.test_audit_manifest_verify()
    tc.test_audit_manifest_modify()

    tc.tearDown()
