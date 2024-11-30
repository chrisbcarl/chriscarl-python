#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-29
Description:

core.functors.parse is... TODO: lorem ipsum
core.functor are modules that functions that are usually defined as lambdas, but i like to hold onto them as named funcs. non-self-referential, low-import, etc.

Updates:
    2024-11-29 - core.functors.parse - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import re
import logging
from dataclasses import dataclass, field
from typing import List

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/functors/parse.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


@dataclass
class PytestCoverage:
    name: str
    stmts: int
    miss: int
    cover: float
    missing: List[str] = field(default_factory=lambda: [])

    @staticmethod
    def parse(text):
        # type: (str) -> List[PytestCoverage]
        coverages = []
        coverage_encountered = False
        for l, line in enumerate(text.splitlines()):
            if not coverage_encountered and line.startswith('---------- coverage:'):
                coverage_encountered = True
            elif coverage_encountered and line.startswith('-----------') or line.startswith('Name'):
                pass
            elif coverage_encountered and line.startswith('TOTAL'):
                coverage_encountered = False
            elif coverage_encountered:
                # src\chriscarl\__init__.py                           0      0   100%
                # src\chriscarl\core\lib\stdlib\json.py              29      7    76%   33, 49-50, 55-57, 61
                tokens = re.split(r'\s{2,}', line)
                if len(tokens) != 5 and len(tokens) != 4:
                    raise ValueError('expected 4 or 5 tokens, got {} out of line {} - {!r}!'.format(len(tokens), l + 1, line))
                if len(tokens) == 4:
                    missing = []
                else:
                    missing = [ele.strip() for ele in tokens[4].split(',')]
                pc = PytestCoverage(name=tokens[0], stmts=int(tokens[1]), miss=int(tokens[2]), cover=int(tokens[3].replace('%', '')) / 100, missing=missing)
                coverages.append(pc)
            print(line)

        return coverages
