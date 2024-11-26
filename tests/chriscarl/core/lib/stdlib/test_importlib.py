#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-25
Description:

chriscarl.core.lib.stdlib.importlib unit test.

Updates:
    2024-11-25 - tests.chriscarl.core.lib.stdlib.importlib - initial commit
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
import chriscarl.core.lib.stdlib.importlib as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/lib/stdlib/test_importlib.py'
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

    def test_walk_module_names_filepaths(self):
        known_libraries = ['logging', 'logging.config', 'logging.handlers']
        logging_libraries = [tpl[0] for tpl in lib.walk_module_names_filepaths(module=logging)]
        self.assert_subset(known_libraries, logging_libraries)

    def test_walk_module(self):
        from chriscarl.core.types.list import sorted_list_by_frequency
        exceptions = [tpl[1] for tpl in lib.walk_module(module=logging)]
        most_common_exceptions = sorted_list_by_frequency(exceptions)
        assert len(most_common_exceptions) == 1, 'how is that logging had a variety of import exceptions?'
        assert most_common_exceptions[0] == (None, None, None), 'how is that logging had an actual import exception?'


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)10s - %(filename)s - %(funcName)s - %(message)s', level=logging.DEBUG)
    tc = TestCase()
    tc.setUp()

    tc.test_walk_module_names_filepaths()
    tc.test_walk_module()

    tc.tearDown()
