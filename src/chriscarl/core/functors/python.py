#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@chriscarl.com
Date:           2024-11-22
Description:

Python is lots of deep nerdy python shit that usually involves runtime fuckery.
chriscarl.core files are non-self-referential, do very little importing, and define the bedrock from which other things do import.

Updates:
    2024-11-22 - chriscarl.core.python - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import re
import sys
import logging
import subprocess
from typing import Any, Tuple, Dict, List, Set, Union, Callable, Generator

# third party imports

# project imports
from chriscarl.core.functors.misc import get_log_func

SCRIPT_RELPATH = 'chriscarl/core/functors/python.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

_hasattr = hasattr
_getattr = getattr
_setattr = setattr


def invocation_arg_string(args):
    return ', '.join(str(a) for a in args)


def invocation_kwarg_string(kwargs):
    return ', '.join('{}={!r}'.format(str(k), v) for k, v in kwargs.items())


def invocation_vararg_string(varargs=None, varkwargs=None):
    if varargs is not None and varkwargs is not None:
        return '*{}, **{}'.format(varargs, varkwargs)
    elif varargs is not None:
        return '*{}'.format(varargs)
    else:
        return '**{}'.format(varkwargs)


def invocation_just_arg_string(func, args, kwargs, varargs=None, varkwargs=None):
    arglist = invocation_arg_string(args)
    kwarglist = invocation_kwarg_string(kwargs)
    varlist = invocation_vararg_string(varargs=varargs, varkwargs=varkwargs)
    tokens = []
    if args:
        tokens.append(arglist)
    if kwargs:
        tokens.append(kwarglist)
    if varargs is not None or varkwargs is not None:
        tokens.append(varlist)

    return '{}'.format(', '.join(tokens))


def invocation_string(func, args=None, kwargs=None, varargs=None, varkwargs=None, func_name=None):
    if args is None:
        args = tuple()
    if kwargs is None:
        kwargs = dict()
    if func_name is None:
        func_name = ''
        try:
            func_name = func.__name__
        except Exception:
            pass

        try:
            func_name = func._Method__name  # sys.version_info[0] == 2:
        except Exception:
            pass

        if not func_name:
            raise NotImplementedError('couldnt find the funcs name for {}!?'.format(func))

    return '{}({})'.format(func_name, invocation_just_arg_string(func, args, kwargs, varargs=varargs, varkwargs=varkwargs))


def hasattr_deep(obj, key):
    # type: (Any, str) -> bool
    '''
    Description:
        test if an object has a deeply nested attribute
        >>> hasattr_deep(obj, 'attr.member')
    '''
    subobj = obj
    for token in key.split('.'):
        if _hasattr(subobj, token):
            subobj = _getattr(subobj, token)
        else:
            return False
    return True


def hasattr_cmp(key, *objs):
    # type: (str, Any) -> Tuple[bool, bool]
    '''
    Description:
        if the first object has or doesnt have the deeply nested attribute:
            are ALL of the rest of the objects the same way?
        >>> hasattr_deep('attr.member', obj0, obj1, obj2)
        >>> (True, True)  # obj0 has attr.member, [obj1, obj2] does all have attr.member
        >>> (True, False)  # obj0 has attr.member, [obj1, obj2] does not all have attr.member
        >>> (False, True)  # obj0 does not have attr.member, [obj1, obj2] does not all have attr.member
        >>> (False, False)  # obj0 does not have attr.member, [obj1, obj2] does all have attr.member
    Returns:
        Tuple
            bool - whether the FIRST object had the deeply nested attribute
            bool - whether all objects are the same way as the first object
    '''
    if not len(objs) > 1:
        raise ValueError('must supply multiple objects')

    A = objs[0]
    B = objs[1:]

    if hasattr_deep(A, key):
        return (True, all(hasattr_deep(obj, key) for obj in B))
    else:
        return (False, all(not hasattr_deep(obj, key) for obj in B))


def getattr_deep(obj, key, default=None):
    # type: (Any, str, Any) -> Any
    '''
    Description:
        get an object's deeply nested attribute or raise AttributeError
        >>> getattr_deep(obj, 'attr.member')
        >>> 69
        >>> getattr_deep(obj, 'attr.member2') -> attribute error
        >>> getattr_deep(obj, 'attr.member2', False)
        >>> False
    Raises:
        AttributeError
    '''
    subobj = obj
    try:
        for token in key.split('.'):
            subobj = _getattr(subobj, token)
    except AttributeError as ae:
        if default is not None:
            return default
        raise AttributeError('{} instance has no attribute {}'.format(obj.__class__.__name__, key)) from ae

    return subobj


def getattr_cmp(key, *objs):
    # type: (str, Any) -> bool
    '''
    Description:
        Are all of the deeply nested attributes equal among the objects?
        >>> getattr_cmp('attr.member', obj0, obj1, obj2)
        >>> True  # they are all equal
        >>> False  # one or more is not equal
    Returns:
        bool
    '''
    if not len(objs) > 1:
        raise ValueError('must supply multiple objects')

    A = objs[0]
    B = objs[1:]

    value = getattr_deep(A, key)  # raises: AttributeError
    for obj in B:
        try:
            if value != getattr_deep(obj, key):
                return False
        except AttributeError:
            return False
    return True


def setattr_deep(obj, key, value):
    # type: (Any, str, Any) -> None
    '''
    Description:
        set an object's deeply nested attribute or raise AttributeError
        >>> setattr_deep(obj, 'attr.member')
    Raises:
        AttributeError
    '''
    subobj = obj
    try:
        tokens = key.split('.')
        for token in tokens[:-1]:
            subobj = _getattr(subobj, token)
        _setattr(subobj, tokens[-1], value)
    except AttributeError as ae:
        raise AttributeError('{} instance has no attribute {}'.format(obj.__class__.__name__, key)) from ae


def conform_func_args_kwargs(func_args_kwargs):
    # type: (List[Union[Callable, Tuple[Callable, Union[tuple, Any, None]], Tuple[Callable, Union[tuple, Any, None], dict]]]) -> List[Tuple[Callable, tuple, dict]]
    sanitized = []
    for e, tpl in enumerate(func_args_kwargs):
        if callable(tpl):
            func, args, kwargs = tpl, tuple(), dict()  # type: ignore
        elif len(tpl) == 1:
            func, args, kwargs = tpl[0], tuple(), dict()
        elif len(tpl) == 2:
            func, args = tpl[0], tpl[1]  # type: ignore
            kwargs = dict()
        elif len(tpl) == 3:
            func, args, kwargs = tpl[0], tpl[1], tpl[2]  # type: ignore
        else:
            raise ValueError('variable {} is expected to be a 1-3 nary tuple of func, args, kwargs!'.format(e))
        if not isinstance(args, tuple):
            args = (args, )
        if not isinstance(kwargs, dict):
            raise TypeError('variable {} kwargs is not of type dict! it is expected to be a 1-3 nary tuple of func, args, kwargs!'.format(e))
        sanitized.append((func, args, kwargs))
    return sanitized


def run_func_args_kwargs(func_args_kwargs, break_idx=-1, log_level=logging.DEBUG):
    # type: (List[Union[Callable, Tuple[Callable, Union[tuple, Any, None]], Tuple[Callable, Union[tuple, Any, None], dict]]], int, Union[str, int]) -> Generator[Any, None, List[Any]]
    log_func = get_log_func(log_level)
    variables = conform_func_args_kwargs(func_args_kwargs)
    results = []
    for e, tpl in enumerate(variables):
        func, args, kwargs = tpl
        inv_str = invocation_string(func, args=args, kwargs=kwargs)
        log_func('%s / %s - %s', e, len(variables) - 1, inv_str)

        if break_idx > -1 and break_idx == e:
            try:
                filepath = sys.modules[func.__module__].__file__
                # https://stackoverflow.com/questions/39453951/open-file-at-specific-line-in-vscode
                # TODO: code --goto "<filepath>:<linenumber>:<x-coordinates>"
                if filepath:  # wont be in in an interpreter
                    subprocess.Popen(['code', '--goto', filepath], shell=True)
                input('!!! BREAK IDX ENCOUNTERED !!!\nPress any key to continue (or actually set breakpoints)...')
            except KeyboardInterrupt:
                break
        result = func(*args, **kwargs)
        yield result
        log_func('%s / %s - %s = %s', e, len(variables) - 1, inv_str, result)
        results.append(result)

    return results


def is_legal_python_name(text):
    # type: (str) -> bool
    return not any([
        re.search(r'[^A-Za-z0-9_]', text),
        re.search(r'\s', text),
        re.match(r'^\d', text),
    ])


def get_legal_python_name(text):
    # type: (str) -> str
    sofar = re.sub(r'[^A-Za-z0-9_]', '_', text)
    sofar = re.sub(r'\s{1,}', '_', sofar)
    sofar = re.sub(r'_{2,}', '_', sofar)
    if re.match(r'^\d', sofar):
        sofar = '_{}'.format(sofar)
    return sofar
