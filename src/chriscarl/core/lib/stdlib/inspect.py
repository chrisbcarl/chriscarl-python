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
    2024-11-26 - core.lib.stdlib.inspect - added FunctionSpecification
    2024-11-24 - core.lib.stdlib.inspect - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import inspect
import logging
from dataclasses import dataclass
from typing import Any, Set, Callable

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


def get_variable_names(var, stack_frames=-1):
    # type: (Any, int) -> Set[str]
    '''
    https://stackoverflow.com/a/18425523
    '''
    names = []
    if stack_frames < 1:
        for frame_tuple in inspect.stack():
            frame = frame_tuple[0]
            names += [k for k, v in frame.f_locals.items() if v is var]
    else:
        for i, frame_tuple in enumerate(inspect.stack()):
            frame = frame_tuple[0]
            if i == stack_frames:
                names = [k for k, v in frame.f_locals.items() if v is var]
                break
    if len(names) == 0:
        names.append('<anonymous>')
    return set(names)


@dataclass
class FunctionSpecification(object):
    _func: Callable
    name: str
    positional_arguments: tuple
    optional_arguments: dict
    varargs: tuple
    varkwargs: dict
    # typing: dict
    defaults: dict

    def __init__(self, func):
        super(FunctionSpecification, self).__init__()
        self._func = func
        self.name = func.__name__

        # TODO: which python versions trigger this?
        # try:
        #     args, varargs, varkw, defaults = inspect.getargspec(func)
        #     kwonlyargs, kwonlydefaults, annotations = (None, None, None)
        # except AttributeError:  # probably python 2
        (args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations) = inspect.getfullargspec(func)  # pylint: disable=no-member

        self.positional_arguments = args
        self.optional_arguments = kwonlydefaults
        if defaults is not None and len(defaults) > 0:
            self.positional_arguments = [a for a in args[:-len(defaults)]]
            for i, argname in enumerate(args[-len(defaults):]):
                if argname != 'self':
                    self.optional_arguments[argname] = defaults[i]
        self.varargs = varargs
        self.varkwargs = varkw
        # self.typing = {}
        self.defaults = {}
        if isinstance(kwonlydefaults, dict):
            self.defaults.update(kwonlydefaults)

    def __str__(self):
        return '{}(name="{}", positional={}, optional={}, varargs={}, varkwargs={})'.format(
            self.__class__.__name__, self.name, self.positional_arguments, unordered_dict(self.optional_arguments), repr(self.varargs), repr(self.varkwargs)
        )

    def to_invocation_string(self, ignore_self=False):
        # type: (bool) -> str
        if ignore_self:
            positionals = [e for e in self.positional_arguments if e == 'self']
        else:
            positionals = list(self.positional_arguments)
        return invocation_string(
            self._func,
            args=positionals,
            kwargs=self.optional_arguments,
            varargs=self.varargs,
            varkwargs=self.varkwargs,
            func_name=self.name,
        )

    @staticmethod
    def get(func):
        # type: (Callable) -> FunctionSpecification
        '''
        args, varargs, varkw, defaults

        ex)
        >>> def main(a, b, c=True, d=False, *args, **kwargs):
        ...     pass
        ...
        ... ArgSpec(args=['a', 'b', 'c', 'd'], varargs='args', keywords='kwargs', defaults=(True, False))
        '''
        if not inspect.isfunction(func) and not inspect.ismethod(func):
            raise ValueError('provided func {} is not a function, or at least it\'s not by inspect\'s standards'.format(repr(func)))
        return FunctionSpecification(func)
