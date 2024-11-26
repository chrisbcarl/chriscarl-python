#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-25
Description:

chriscarl.files.manifest unit test.

Updates:
    2024-11-25 - tests.chriscarl.files.manifest - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest

# third party imports

# project imports (expected to work)
from chriscarl.core.lib.stdlib.unittest import assert_null_hypothesis

# test imports
import chriscarl.files.manifest as lib

SCRIPT_RELPATH = 'tests/chriscarl/files/test_manifest.py'
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

    def test_self_verify(self):
        variables = [
            (lib._self_verify),
        ]
        controls = [
            True,
        ]
        assert_null_hypothesis(variables, controls)

    def test_self_modify(self):
        from chriscarl.core.lib.stdlib.io import read_bytes_file
        original = read_bytes_file(lib.__file__)
        lib._self_modify()
        new = read_bytes_file(lib.__file__)
        self.assertEqual(original, new, '_self_modify should take effect but be idempotent! something changed, check the git diff?')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)10s - %(filename)s - %(funcName)s - %(message)s', level=logging.DEBUG)
    tc = TestCase()
    tc.setUp()

    tc.test_self_verify()

    tc.tearDown()
