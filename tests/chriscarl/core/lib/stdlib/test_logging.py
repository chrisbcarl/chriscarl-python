#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-26
Description:

chriscarl.core.lib.stdlib.logging unit test.

Updates:
    2024-11-26 - tests.chriscarl.core.lib.stdlib.logging - initial commit
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
import chriscarl.core.lib.stdlib.logging as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/lib/stdlib/test_logging.py'
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

    def test_case_0_get_log_func_from_level(self):
        seventyone = lib.get_log_func_from_level(71)
        variables = [
            (lib.get_log_func_from_level, 'DEBUG'),
            (lib.get_log_func_from_level, 'INFO'),
            (lib.get_log_func_from_level, 'WARNING'),
            (lib.get_log_func_from_level, 'ERROR'),
            (lib.get_log_func_from_level, 'CRITICAL'),
            (seventyone, 'plz'),
        ]
        controls = [
            logging.debug,
            logging.info,
            logging.warning,
            logging.error,
            logging.critical,
            None,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_int_levels(self):
        variables = [
            (lib.level_to_int, 1),
            (lib.level_to_int, 'DEBUG'),
            (lib.level_to_int, 'INFO'),
            (lib.level_to_int, 'WARNING'),
            (lib.level_to_int, 'ERROR'),
            (lib.level_to_int, 'CRITICAL'),
            (lib.level_to_int, 'PLZ'),
            (lib.levels_to_ints, [1, 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']),
            (lib.levels_to_ints, [1, 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'PLZ']),
        ]
        controls = [
            1,
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
            ValueError,
            [1, logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL],
            ValueError,
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_get_log_func_from_level()
    tc.test_case_1_int_levels()

    tc.tearDown()
