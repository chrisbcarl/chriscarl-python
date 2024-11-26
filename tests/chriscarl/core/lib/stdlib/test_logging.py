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

    def test_get_log_func(self):
        sixtynine = lib.get_log_func(69)
        variables = [
            (lib.get_log_func, 'DEBUG'),
            (lib.get_log_func, 'INFO'),
            (lib.get_log_func, 'WARNING'),
            (lib.get_log_func, 'ERROR'),
            (lib.get_log_func, 'CRITICAL'),
            (sixtynine, 'plz'),
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


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)10s - %(filename)s - %(funcName)s - %(message)s', level=logging.DEBUG)
    tc = TestCase()
    tc.setUp()

    tc.test_get_log_func()

    tc.tearDown()
