#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-29
Description:

chriscarl.mod.lib.stdlib.logging unit test.

Updates:
    2024-11-29 - tests.chriscarl.mod.lib.stdlib.logging - initial commit
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
import chriscarl.mod.lib.stdlib.logging as lib

SCRIPT_RELPATH = 'tests/chriscarl/mod/lib/stdlib/test_logging.py'
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

    def test_case_0_new_levels(self):
        variables = [
            # usual
            (logging.debug, 'plz'),
            (logging.info, 'plz'),
            (logging.warning, 'plz'),
            (logging.error, 'plz'),
            (logging.critical, 'plz'),
            # mine
            (logging.diffuse, 'plz'),
            (logging.verbose, 'plz'),
            (logging.important, 'plz'),
            (logging.inform, 'plz'),
            (logging.success, 'plz'),
            # usual
            (LOGGER.debug, 'plz'),
            (LOGGER.info, 'plz'),
            (LOGGER.warning, 'plz'),
            (LOGGER.error, 'plz'),
            (LOGGER.critical, 'plz'),
            # mine
            (LOGGER.diffuse, 'plz'),
            (LOGGER.verbose, 'plz'),
            (LOGGER.important, 'plz'),
            (LOGGER.inform, 'plz'),
            (LOGGER.success, 'plz'),
        ]
        controls = [None for _ in variables]
        if sys.version_info[0] == 2:
            new_variables = [(logging._levelNames.__contains__, k) for k in lib.NEW_NAME_TO_LEVEL] + [(logging._levelNames.__contains__, v) for v in lib.NEW_NAME_TO_LEVEL.values()]
            variables += new_variables
            controls += [True for _ in new_variables]
        else:
            new_variables = [(logging._nameToLevel.__contains__, k)
                             for k in lib.NEW_NAME_TO_LEVEL] + [(logging._levelToName.__contains__, v) for v in lib.NEW_NAME_TO_LEVEL.values()]
            variables += new_variables
            controls += [True for _ in new_variables]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_new_levels()

    tc.tearDown()
