#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-12-09
Description:

core.types.iterable is actually a lot of list and dict stuff combined, but since its not mutually exclusive, i figured I'd put them here.
core.types are modules that pertain to data structures, algorithms, conversions. non-self-referential, low-import, etc.

Updates:
    2024-12-11 - core.types.iterable - added keys
    2024-12-09 - core.types.iterable - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import Optional, Union, Any, Iterable, List, Dict, Generator, Tuple
from collections import OrderedDict

# third party imports

# project imports
from chriscarl.core.constants import SENTINEL
from chriscarl.core.lib.stdlib.inspect import get_variable_name_lineno
from chriscarl.core.lib.stdlib.typing import isinstance_raise

SCRIPT_RELPATH = 'chriscarl/core/types/iterable.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

Keyable = Union[Dict, List, Tuple]


def get(key, iterable, split='.', default=SENTINEL):
    # type: (str, Keyable, str, Any) -> Any
    iterable_name = get_variable_name_lineno(iterable)[0]
    current_value = iterable
    key_so_far = []
    try:
        if not isinstance(key, str):
            return iterable[key]

        for key in key.split(split):
            key_so_far.append(key)
            try:
                int_key = int(key, base=0)
                current_value = current_value[int_key]  # type: ignore
                continue
            except ValueError:
                pass

            current_value = current_value[key]  # type: ignore
    except (IndexError, KeyError, TypeError) as ike:
        if default != SENTINEL:
            return default
        raise KeyError('key "{}" for provided object "{}" does not exist because of {!r}!'.format(split.join(key_so_far), iterable_name, ike)) from ike
    return current_value


def keys(value, prepend=None):
    # type: (Keyable, Optional[str]) -> Generator[str, None, None]
    '''
    Description:
        given a dictionary like this: {'a': 0, 'b': [1, 2]}
        yield a generator of: ['a', 'b.0', 'b.1']

    Arguments:
        value: Keyable
        prepend: Optional[str]
            if you want the keys to start with something
            >>> keys({'a': 0, 'b.0': 1, 'b.1': 2}, prepend='whatever')
            >>> yields ['whatever.a', 'whatever.b.0', 'whatever.b.1']

    Returns:
        Generator[str, None, None]
    '''
    isinstance_raise(value, Keyable)
    if isinstance(value, dict):
        for k, v in value.items():
            if prepend is None:
                key = k
            else:
                key = '{}.{}'.format(prepend, k)
            yield key
            for key in keys(v, prepend=key):
                yield key
    elif isinstance(value, (list, tuple, set)):
        for i, v in enumerate(value):
            if prepend is None:
                key = str(i)
            else:
                key = '{}.{}'.format(prepend, i)
            for key in keys(v, prepend=key):
                yield key


def flatten_iterable(value, prepend=None, _flattened=None):
    # type: (Union[Iterable, Any], Optional[str], Optional[dict]) -> Union[dict, Any]
    '''
    Description:
        given a dictionary like this: {'a': 0, 'b': [1, 2]}
        return a dictionary like this: {'a': 0, 'b.0': 1, 'b.1': 2}

    Arguments:
        value: Union[Iterable, Any]
            give anything, if iterable, takes it seriously, if just a primitive, returns the primitive
        prepend: Optional[str]
            if you want the keys to start with something
            >>> flatten_iterable({'a': 0, 'b.0': 1, 'b.1': 2}, prepend='whatever')
            >>> {'whatever.a': 0, 'whatever.b.0': 1, 'whatever.b.1': 2}
        _flattened: Optional[dict]
            do not provide this, its to facilitate the recursion

    Returns:
        Union[dict, Any]
    '''
    if _flattened is None:
        if not isinstance(value, Iterable):
            return value
        _flattened = OrderedDict()

    if isinstance(value, dict):
        if len(value) == 0:
            _flattened[prepend] = type(value)()

        for k, v in value.items():
            if prepend is None:
                key = k
            else:
                key = '{}.{}'.format(prepend, k)
            flatten_iterable(v, prepend=key, _flattened=_flattened)
    elif isinstance(value, (list, tuple, set)):
        if len(value) == 0:
            _flattened[prepend] = type(value)()  # type: ignore

        for i, v in enumerate(value):
            if prepend is None:
                key = str(i)
            else:
                key = '{}.{}'.format(prepend, i)
            flatten_iterable(v, prepend=key, _flattened=_flattened)
    else:
        _flattened[prepend] = value
    return _flattened


def unflatten_iterable(flat, split='.'):
    # type: (Union[dict, Any], str) -> Union[dict, list]
    '''
    Description:
        (inverse of flatten_iterable)
        given a dictionary like this: {'a': 0, 'b.0': 1, 'b.1': 2}
        return a dictionary like this: {'a': 0, 'b': [1, 2]}

    Arguments:
        flat: Union[dict, Any]
            give anything, if iterable, takes it seriously, if just a primitive, returns the primitive

    Returns:
        Union[dict, list]
    '''
    flat_keys = {}  # type: Dict[str, List[Union[str, int]]]
    if not isinstance(flat, dict):
        return flat
    shortest = 9999999
    for key in flat:
        short = len(key.split(split))
        if short < shortest:
            shortest = short
    for key in flat:
        # TODO: to account for pre-prepended flattened_iterables splicing by [0 if shortest == 1 else 1:] doesnt work...
        tokens = key.split(split)
        new_tokens = []  # type: List[Union[str, int]]
        for token in tokens:
            try:
                new_tokens.append(int(token, base=0))
            except ValueError:
                new_tokens.append(token)
        flat_keys[key] = new_tokens

    iterable: Union[dict, list]
    obj: Union[dict, list]
    new: Union[dict, list]
    if all(isinstance(tokens[0], int) for tokens in flat_keys.values()):
        iterable = obj = []
    else:
        iterable = obj = {}

    objs_so_far = {'': iterable}  # type: Dict[str, Union[dict, list]]

    for flat_key, tokens in flat_keys.items():
        obj = iterable
        for t, token in enumerate(tokens):
            if t < len(tokens) - 1:
                flat_so_far = split.join(str(ele) for ele in tokens[:t + 1])
                path_minus_the_end = split.join(str(ele) for ele in tokens[:t])
                obj = objs_so_far[path_minus_the_end]
                if isinstance(obj, dict):
                    if flat_so_far not in objs_so_far:
                        new = {} if isinstance(tokens[t + 1], str) else []
                        obj[token] = objs_so_far[flat_so_far] = new
                else:
                    if flat_so_far not in objs_so_far:
                        new = {} if isinstance(tokens[t + 1], str) else []
                        objs_so_far[flat_so_far] = new
                        obj.append(objs_so_far[flat_so_far])
            else:
                path_minus_the_end = split.join(str(ele) for ele in tokens[:t])
                obj = objs_so_far[path_minus_the_end]
                if isinstance(obj, dict):
                    obj[token] = flat[flat_key]
                else:
                    obj.append(flat[flat_key])

    return iterable
