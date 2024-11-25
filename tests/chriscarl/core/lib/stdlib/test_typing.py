#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Carl, Chris
Email:          chrisbcarl@outlook.com
Date:           2024-11-23
Description:

Unit test for chriscarl.core.lib.stdlib.typing

Updates:
    2024-11-23 - tests.core.lib.stdlib.test_typing - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import typing
import logging
import unittest

# third party imports

# project imports (expected to work)
from chriscarl.core.lib.stdlib.unittest import assert_null_hypothesis

# test imports
import chriscarl.core.lib.stdlib.typing as lib
import chriscarl.mod.python as mod

SCRIPT_RELPATH = 'tests/libraries/third/test_unittest.py'
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
        self.str = 'str'
        self.int = 69
        self.float = 3.14
        self.bool = False
        self.none = None
        self.tuple = (1, 2, 3, 4)
        self.list = [1, 2, 3, 4]
        self.dict = {'1': 2, '3': 4}
        self.set = {1, 2, 3, 4}
        self.callable = self.callable_vargs_vkwargs
        self.generator = self.generate_vargs_vkwargs()

        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def callable_vargs_vkwargs(self, *args, **kwargs):
        pass

    def generate_vargs_vkwargs(self, *args, **kwargs):
        for _ in range(10):
            yield

    def test_easy_true(self):
        variables = [
            (lib.isof, (self.str, str)),
            (lib.isof, (self.int, int)),
            (lib.isof, (self.float, float)),
            (lib.isof, (self.bool, bool)),
            (lib.isof, (self.none, None)),
            (lib.isof, (self.tuple, tuple)),
            (lib.isof, (self.tuple, typing.Tuple)),
            (lib.isof, (self.list, list)),
            (lib.isof, (self.list, typing.List)),
            (lib.isof, (self.dict, dict)),
            (lib.isof, (self.dict, typing.Dict)),
            (lib.isof, (self.set, set)),
            (lib.isof, (self.set, typing.Set)),
            (lib.isof, (self.callable, typing.Callable)),
            (lib.isof, (self.generator, typing.Generator)),
            (lib.isof, (self.str, (str, int, float))),
            (lib.isof, (self.int, (str, int, float))),
            (lib.isof, (self.float, (str, int, float))),
        ]
        controls = [True for _ in variables]
        assert_null_hypothesis(variables, controls)

    def test_easy_false(self):
        variables = [
            (lib.isof, (self.dict, str)),
            (lib.isof, (self.dict, int)),
            (lib.isof, (self.set, float)),
            (lib.isof, (self.set, bool)),
            (lib.isof, (self.callable, None)),
            (lib.isof, (self.generator, tuple)),
            (lib.isof, (self.str, typing.Tuple)),
            (lib.isof, (self.int, list)),
            (lib.isof, (self.float, typing.List)),
            (lib.isof, (self.str, dict)),
            (lib.isof, (self.int, typing.Dict)),
            (lib.isof, (self.float, set)),
            (lib.isof, (self.bool, typing.Set)),
            (lib.isof, (self.none, typing.Callable)),
            (lib.isof, (self.tuple, typing.Generator)),
            (lib.isof, (self.tuple, (str, int, float))),
            (lib.isof, (self.list, (str, int, float))),
            (lib.isof, (self.list, (str, int, float))),
        ]
        controls = [False for _ in variables]

        assert_null_hypothesis(variables, controls)

    def test_med_true(self):
        variables = [
            (lib.isof, (self.int, typing.Union[int, float, str])),
            (lib.isof, (self.float, typing.Union[int, float, str])),
            (lib.isof, (self.str, typing.Union[int, float, str])),
            (lib.isof, (self.tuple, typing.Tuple[int, int, int, int])),
            (lib.isof, (self.list, typing.List[int])),
            (lib.isof, (self.set, typing.Set[int])),
            (lib.isof, (self.dict, typing.Dict[str, int])),
        ]
        controls = [True for _ in variables]

        assert_null_hypothesis(variables, controls)

    def test_med_false(self):
        variables = [
            (lib.isof, (self.tuple, typing.Union[int, float, str])),
            (lib.isof, (self.list, typing.Union[int, float, str])),
            (lib.isof, (self.set, typing.Union[int, float, str])),
            (lib.isof, (self.dict, typing.Tuple[int, int, int, int])),
            (lib.isof, (self.int, typing.List[int])),
            (lib.isof, (self.float, typing.Set[int])),
            (lib.isof, (self.str, typing.Dict[str, int])),
        ]
        controls = [False for _ in variables]

        assert_null_hypothesis(variables, controls)

    def test_hard_true(self):
        variables = [
            (lib.isof, (self.str, typing.Any)),
            (lib.isof, (self.int, typing.Any)),
            (lib.isof, (self.float, typing.Any)),
            (lib.isof, (self.bool, typing.Any)),
            (lib.isof, (self.none, typing.Any)),
            (lib.isof, (self.tuple, typing.Any)),
            (lib.isof, (self.list, typing.Any)),
            (lib.isof, (self.dict, typing.Any)),
            (lib.isof, (self.set, typing.Any)),
            (lib.isof, (self.callable, typing.Any)),
            (lib.isof, (self.generator, typing.Any)),
            (lib.isof, (self.int, typing.Union[int, float])),
            (lib.isof, (self.float, typing.Union[int, float])),
            (lib.isof, ((self.list, self.dict, self.set), typing.Tuple[list, dict, set])),
            (lib.isof, (self.set, typing.Set[int])),
            (lib.isof, (set(), typing.Set[int])),
            (lib.isof, ([self.set, self.set, self.set], typing.List[typing.Set[int]])),
            (lib.isof, ([], typing.List[typing.Set[int]])),
            (lib.isof, ({
                'a': self.list,
                'b': self.list
            }, typing.Dict[str, typing.List[typing.Union[int, float]]])),
            (lib.isof, ({}, typing.Dict[str, typing.List[typing.Union[int, float]]])),
            (lib.isof, (self.callable, typing.Callable[[int, typing.List[float]], typing.Tuple[int, float]])),
            (lib.isof, (self.generator, typing.Generator[typing.Tuple[int, typing.List[float]], None, None])),
        ]
        controls = [True for _ in variables]

        assert_null_hypothesis(variables, controls)

    def test_hard_false(self):
        variables = [
            (lib.isof, (self.generator, typing.Union[int, float])),
            (lib.isof, (self.callable, typing.Union[int, float])),
            (lib.isof, (self.set, typing.Tuple[list, dict, set])),
            (lib.isof, (self.dict, typing.Set[int])),
            (lib.isof, (self.set, typing.List[typing.Set[int]])),
            (lib.isof, (self.list, typing.Dict[str, typing.List[typing.Union[int, float]]])),
            (lib.isof, (self.tuple, typing.Callable[[int, typing.List[float]], typing.Tuple[int, float]])),
            (lib.isof, (self.none, typing.Generator[typing.Tuple[int, typing.List[float]], None, None])),
            (lib.isof, (tuple(), typing.Tuple[list, dict, set])),
        ]
        controls = [False for _ in variables]

        assert_null_hypothesis(variables, controls)

    @unittest.skip('TODO: pytest freaks out on mod')
    def test_mod(self):
        with mod.Mod():
            pass


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)10s - %(filename)s - %(funcName)s - %(message)s', level=logging.DEBUG)
    tc = TestCase()
    tc.setUp()

    tc.test_easy_true()
    tc.test_easy_false()
    tc.test_med_true()
    tc.test_med_false()
    tc.test_hard_true()
    tc.test_hard_false()

    tc.tearDown()
