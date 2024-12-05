#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-12-04
Description:

core.types.version is my conceptions around semantic versioning
core.types are modules that pertain to data structures, algorithms, conversions. non-self-referential, low-import, etc.

Updates:
    2024-12-04 - core.types.version - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import re
import copy
import logging
from dataclasses import dataclass
from typing import Union, Tuple

# third party imports
from six import string_types

# project imports

SCRIPT_RELPATH = 'chriscarl/core/types/version.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

REGEX_VERSION = re.compile(r'^(?P<major>\d+) \. (?P<minor>\d+) (?P<patch>\. (\d+))? ((?P<label>[-ab])([\d\.\-\w]+))?$', flags=re.VERBOSE)
REGEX_LABEL = re.compile(r'^\-?(?P<label>[\d\.\-\w]+)?$', flags=re.VERBOSE)
REGEX_PRERELEASE = re.compile(r'^[ab](?P<prerelease>[\d\.\-\w]+)?$', flags=re.VERBOSE)


@dataclass
class Version(object):
    '''
    Description:
        Heavily reimplemented from C:/Python27/Lib/distutils/version.py
            - 1.0.0 > 1.0.0a1
            - 1.0.0-beta > 1.0.0-alpha
            - 1.0.0 < 1.1.0
        Examples:
            >>> Version('1.0.0')
            >>> Version('0.0.25-alpha')  # label alpha, 0
            >>> Version('0.5.3-rc1')  # label rc, 1
            >>> Version('0.5.3a69')  # prerelease a, 69
            >>> Version('1.-2.-3-alpha')  # throws
            >>> Version('1.-2.-3a1')  # throws
    '''
    major: int
    minor: int
    patch: int
    label: Tuple[str, int]
    prerelease: Tuple[str, int]

    @staticmethod
    def parse(version):
        # type: (str) -> Version
        match = REGEX_VERSION.match(version)
        if not match:
            raise ValueError('invalid version number {!r}'.format(version))

        (major, minor, patch, prerelease, prerelease_num) = match.group(1, 2, 4, 6, 7)
        label = None

        tokens = [major, minor, patch, prerelease_num]
        for i, token in enumerate(tokens[0:3]):
            if token is not None:
                tokens[i] = int(token, base=0)

        try:
            tokens[3] = int(tokens[3], base=0)
        except (ValueError, TypeError):
            pass

        if prerelease is not None:
            if prerelease == '-':
                # not a real prerelease like '-2021.10.02'
                prerelease = None
                label = (tokens[3], 0)
            else:
                # not a real prerelease like 'a1'
                prerelease = (prerelease, tokens[3])
                label = None

        major, minor, patch = int(tokens[0]), int(tokens[1]), int(tokens[2])
        return Version(major=major, minor=minor, patch=patch, label=label, prerelease=prerelease)

    @property
    def version(self):
        return [self.major, self.minor, self.patch, self.prerelease or self.label]

    def update(self, arg, value=0):
        # type: (str, Union[str, int]) -> Version
        '''Args:
            arg (str): must be one of the following values
                'major', 'minor', 'patch', 'label', 'prerelease'
            value (str, int):
                if the value is an int it's gonna be added to the current ver
                else, it'll replace the preexisting tag, unless if the value
                    was a flag like 0, false, None which will remove the tag
        '''
        if arg == 'major':
            assert isinstance(value, int)
            self.major += value
            self.minor = 0
            self.patch = 0
        elif arg == 'minor':
            assert isinstance(value, int)
            self.minor += value
            self.patch = 0
        elif arg == 'patch':
            assert isinstance(value, int)
            self.patch += value
        elif arg == 'label' or arg == 'prerelease':
            if self.prerelease is not None and arg == 'label':
                raise TypeError('{} is a prerelease, not a label version!'.format(self))
            elif self.label is not None and arg == 'prerelease':
                raise TypeError('{} is a label, not a prerelease version!'.format(self))

            if arg == 'prerelease':
                if self.prerelease is None:
                    if isinstance(value, string_types):
                        match = REGEX_PRERELEASE.match(value)
                        if not match:
                            raise ValueError('invalid prerelease number {!r}'.format(value))
                        (prerelease, prerelease_num) = match.group(1, 2)
                        try:
                            prerelease_num = int(prerelease_num, base=0)
                        except ValueError:
                            raise ValueError('provided {!r} is not a valid prerelease!'.format(value))
                        self.prerelease = (prerelease, prerelease_num)
                elif isinstance(value, type(self.prerelease[1])):
                    if isinstance(value, int):
                        self.prerelease[1] += value
                    elif isinstance(value, string_types):
                        self.prerelease[1] = value
                elif value is None:
                    self.prerelease = value
                else:
                    raise TypeError('conflicting types between current and update prerelease value! {!r} vs {!r}!'.format(self.prerelease[1], value))
            else:
                if self.label is None:
                    if isinstance(value, string_types):
                        match = REGEX_LABEL.match(value)
                        if not match:
                            raise ValueError('invalid label number {!r}'.format(value))
                        (label, label_num) = match.group(1, 2)
                        try:
                            label_num = int(label_num, base=0)
                        except ValueError:
                            raise ValueError('provided {!r} is not a valid label!'.format(value))
                        self.label = (label, label_num)
                elif isinstance(value, type(self.label)):
                    if isinstance(value, int):
                        self.label += value
                    elif isinstance(value, string_types):
                        self.label = value
                elif value is None:
                    self.label = value
                else:
                    raise TypeError('conflicting types between current and update label value! {!r} vs {!r}!'.format(self.label, value))

        return copy.deepcopy(self)

    def __repr__(self):
        if self.label is not None:
            pre = '(label)'
        elif self.prerelease is not None:
            pre = '(prerelease)'
        else:
            pre = ''
        return 'Version{}<{}>'.format(pre, str(self))

    def __str__(self):
        vstring = '.'.join(map(lambda x: str(x), self.version[0:3]))
        if self.prerelease is not None:
            vstring = '{}{}{}'.format(vstring, self.prerelease[0], str(self.prerelease[1]))
        elif self.label is not None:
            vstring = '{}-{}'.format(vstring, self.label)
        return vstring

    def _cmp(self, other):
        if isinstance(other, string_types):
            other = Version.parse(other)

        if self.version[0:3] == other.version[0:3]:
            vcmp = 0
        elif self.version[0:3] < other.version[0:3]:
            vcmp = -1
        else:
            vcmp = 1

        if vcmp != 0:
            return vcmp
        else:
            if ((self.prerelease is None and other.prerelease is None) and (self.label is None and other.label is None)):
                # case 1: both have no prerelease and no label
                return 0
            # compare the pre-releaseness
            elif self.prerelease is not None or other.prerelease is not None:
                if self.prerelease and not other.prerelease:
                    # case 2: self has prerelease, other doesn't; other is greater
                    return -1
                elif other.prerelease and not self.prerelease:
                    # case 3: self doesn't have prerelease, other does: self is greater
                    return 1
                else:
                    # case 4: both have prerelease: must compare them!
                    if self.prerelease == other.prerelease:
                        return 0
                    elif self.prerelease < other.prerelease:
                        return -1
                    else:
                        return 1
            # compare the labelness
            elif self.label is not None or other.label is not None:
                if self.label and not other.label:
                    # case 2: self has label, other doesn't; other is greater
                    return -1
                elif other.label and not self.label:
                    # case 3: self doesn't have label, other does: self is greater
                    return 1
                else:
                    # case 4: both have label: must compare them!
                    if self.label == other.label:
                        return 0
                    elif self.label < other.label:
                        return -1
                    else:
                        return 1
            else:
                assert False, 'never get here'

    def __eq__(self, other):
        c = self._cmp(other)
        return c == 0

    def __lt__(self, other):
        c = self._cmp(other)
        return c < 0

    def __le__(self, other):
        c = self._cmp(other)
        return c <= 0

    def __gt__(self, other):
        c = self._cmp(other)
        return c > 0

    def __ge__(self, other):
        c = self._cmp(other)
        return c >= 0
