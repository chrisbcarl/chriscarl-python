#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-29
Description:

chriscarl.core.functors.parse unit test.

Updates:
    2024-11-29 - tests.chriscarl.core.functors.parse - initial commit
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
from chriscarl.core.lib.stdlib.unittest import UnitTest
from chriscarl.core.lib.stdlib.io import read_text_file
from chriscarl.core.lib.stdlib.os import abspath

# test imports
import chriscarl.core.functors.parse as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/functors/test_parse.py'
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

    def test_case_PytestCoverage(self):
        pytest_coverage_text = read_text_file(abspath(TEST_COLLATERAL_DIRPATH, 'pytest-coverage.txt'))
        pytest_coverages = lib.PytestCoverage.parse(pytest_coverage_text)
        for pytest_coverage in pytest_coverages:
            LOGGER.debug(pytest_coverage)
        self.assertGreater(len(pytest_coverages), 0)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)10s - %(filename)s - %(funcName)s - %(message)s', level=logging.DEBUG)
    tc = TestCase()
    tc.setUp()

    tc.test_case_PytestCoverage()

    tc.tearDown()
