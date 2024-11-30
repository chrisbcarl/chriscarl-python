#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@chriscarl.com
Date:           2024-11-24
Description:


core.lib.stdlib.inspect is all about the framerate
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Updates:
    2024-11-27 - core.lib.stdlib.inspect - simplified get_variable_names_linenos and FunctionSpecification
    2024-11-26 - core.lib.stdlib.inspect - added FunctionSpecification
                 core.lib.stdlib.inspect - added get_variable_name_lineno
    2024-11-24 - core.lib.stdlib.inspect - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import inspect
import logging
from dataclasses import dataclass
from typing import Any, Optional, Callable, List, Tuple

# third party imports

# project imports
from chriscarl.core.functors.python import invocation_string
from chriscarl.core.lib.stdlib.collections import unordered_dict

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/inspect.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def get_variable_names_linenos(var, stack_frames=-1, ignore_frames=None):
    # type: (Any, int, Optional[List[int]]) -> List[Tuple[str, int]]
    '''
    https://stackoverflow.com/a/18425523
    '''
    name_lineno: List[Tuple[str, int]] = []
    ignore_frames = ignore_frames or []
    for i, frame_tuple in enumerate(inspect.stack()):
        if i in ignore_frames:
            continue
        frame = frame_tuple[0]
        lineno = frame_tuple[2]
        name_lineno += [(k, lineno) for k, v in frame.f_locals.items() if v is var]
        if i == stack_frames:
            break
    if len(name_lineno) == 0:
        name_lineno.append(('<anonymous>', -1))
    return name_lineno


def get_variable_name_lineno(var, stack_frames=-1):
    # type: (Any, int) -> Tuple[str, int]
    '''
    the most likely variable name is the last one from get_variable_names_linenos limited up to the stack frames
    '''
    names_linenos = get_variable_names_linenos(var, stack_frames=stack_frames + 1 if stack_frames != -1 else stack_frames, ignore_frames=[0, 1])
    return names_linenos[-1]


@dataclass
class FunctionSpecification(object):
    func: Callable
    name: str
    positional: List[str]
    optional: dict
    varargs: Optional[str]
    varkwargs: Optional[str]

    def __str__(self):
        return '{}(name="{}", positional={}, optional={}, varargs={}, varkwargs={})'.format(
            self.__class__.__name__, self.name, self.positional, unordered_dict(self.optional), repr(self.varargs), repr(self.varkwargs)
        )

    def to_invocation_string(self, ignore_self=False):
        # type: (bool) -> str
        if ignore_self:
            positionals = [e for e in self.positional if e == 'self']
        else:
            positionals = list(self.positional)
        return invocation_string(
            self.func,
            args=positionals,
            kwargs=self.optional,
            varargs=self.varargs,
            varkwargs=self.varkwargs,
            func_name=self.name,
        )

    @staticmethod
    def get(func):
        # type: (Callable) -> FunctionSpecification
        '''
        Description:
            >>> def main(a, b, *args, c=True, d=False, **kwargs):
            ...     pass
            ...
            ... FunctionSpecification(func)
        Raises:
            ValueError if not a function or method
        '''
        if not inspect.isfunction(func) and not inspect.ismethod(func):
            raise ValueError('provided func {} is not a function, or at least its not by inspect standards'.format(repr(func)))
        name = func.__name__

        # TODO: which python versions trigger this?
        # try:
        #     args, varargs, varkw, defaults = inspect.getargspec(func)
        #     kwonlyargs, kwonlydefaults, annotations = (None, None, None)
        # except AttributeError:  # probably python 2
        (args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations) = inspect.getfullargspec(func)  # pylint: disable=no-member

        positional = args
        optional = kwonlydefaults or {}
        if defaults is not None and len(defaults) > 0:
            positional = [a for a in args[:-len(defaults)]]
            for i, argname in enumerate(args[-len(defaults):]):
                if argname != 'self':
                    optional[argname] = defaults[i]
        varargs = varargs
        varkwargs = varkw
        fs = FunctionSpecification(func=func, name=name, positional=positional, optional=optional, varargs=varargs, varkwargs=varkwargs)
        return fs
