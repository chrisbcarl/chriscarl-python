#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Carl, Chris
Email:          chrisbcarl@chriscarl.com
Date:           2024-11-22
Description:

"Shadow module" that "shadows" the "unittest" module with extra functionality via side effects.

Updates:
    2024-11-22 - chriscarl.libraries.uncore.stdlib.unittest - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import inspect
import logging
import subprocess
from typing import Callable, Tuple, Iterable, List, Any, Union

# third party imports

# project imports
from chriscarl.core.functors.python import conform_func_args_kwargs, invocation_string
from chriscarl.core.lib.stdlib.typing import isinstance_raise

SCRIPT_RELPATH = 'chriscarl/libraries/third/unittest.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def assert_null_hypothesis(variables, controls, break_idx=-1):
    # (List[Union[Callable, Tuple[Callable, Union[tuple, Any, None]], Tuple[Callable, Union[tuple, Any, None], dict]]], Tuple[Callable, tuple, dict]]], List[Any], int) -> bool
    '''
    Description:
        h0 (the "null" hypothesis) is that there is no relationship between the variables and the function, therefore the control group will reflect the experiment results
        the goal here is "fail to fail to reject the null hypothesis"
        >>> variables = [
        >>>     (sum, ([1, 2, 3],), {}),
        >>>     (len, ([1, 2, 3]), {}),
        >>>     (len, 1),
        >>> ]
        >>> controls = [6, 3, TypeError]
        >>> assert_null_hypothesis(variables, controls)
    Arguments:
        variables: List[Union[Callable, Tuple[Callable, Union[tuple, Any, None]], Tuple[Callable, Union[tuple, Any, None], dict]]]
            basically:
                (func)
                (func, arg)
                (func, kwargs)
                (func, arg, kwargs)
                (func, args tuple)
                (func, args tuple, kwargs)
        controls: List[Any]
        break_idx: int
            set this to get an input pause so that you can "catch yourself" kind of like print debugging.
    '''
    isinstance_raise(variables, List[Union[Callable, Tuple[Callable, Union[tuple, Any, None]], Tuple[Callable, Union[tuple, Any, None], dict]]])
    isinstance_raise(variables, List[Any])

    if len(variables) != len(controls):
        raise ValueError('len(variables) != len(controls): {} != {}'.format(len(variables), len(controls)))

    variables = conform_func_args_kwargs(variables)
    for e, tpl in enumerate(variables):
        func, args, kwargs = tpl
        control = controls[e]
        inv_str = invocation_string(func, args=args, kwargs=kwargs)
        status = 'experiment {} / {} - {}'.format(e, len(variables) - 1, inv_str)

        # stacklevel has a bug in it somewhere such that lazy formatting isnt correctly using THIS frame, but the stacklevel frame
        LOGGER.debug(status, stacklevel=2)

        if break_idx > -1 and break_idx == e:
            try:
                filepath = sys.modules[func.__module__].__file__
                # https://stackoverflow.com/questions/39453951/open-file-at-specific-line-in-vscode
                # TODO: code --goto "<filepath>:<linenumber>:<x-coordinates>"
                subprocess.Popen(['code', '--goto', filepath], shell=True)
                input('!!! BREAK IDX ENCOUNTERED - {} !!!\nPress any key to continue (or actually set breakpoints)...'.format(status))
            except KeyboardInterrupt:
                sys.exit(2)  # SIGINT-ish

        if inspect.isclass(control) and issubclass(control, Exception):
            try:
                experiment = func(*args, **kwargs)
                assert False, '{} failed to accept null hypothesis (experiment raises exception): {} not encountered, got a real result instead {}!'.format(
                    status, control, experiment
                )
            except Exception as ex:
                experiment = ex
            assert issubclass(type(experiment), control), '{} failed to accept null hypothesis (control != experiment): {} != {}!'.format(status, control, experiment)

        else:
            experiment = func(*args, **kwargs)
            if inspect.isgenerator(experiment) or isinstance(experiment, (map, filter)):
                LOGGER.debug('{} encountered a generator... expanding.'.format(status))
                experiment = list(experiment)  # expand it out
            assert experiment == control, '{} failed to accept null hypothesis (control != experiment): {} != {}'.format(status, control, experiment)

        # stacklevel has a bug in it somewhere such that lazy formatting isnt correctly using THIS frame, but the stacklevel frame
        LOGGER.info('{} = {}'.format(status, control), stacklevel=2)
    return True


def assert_subset(subset, superset):
    # (Iterable, Iterable) -> bool
    '''
    Description:
        assert that all of the elements of the left are in the elements on the left
    Arguments:
        subset: Iterable
        superset: Iterable
    '''
    isinstance_raise(subset, Iterable)
    isinstance_raise(superset, Iterable)

    subset = set(list(subset))
    superset = set(list(superset))

    assert subset.issubset(superset), 'failed to assert left set of {} elements is a subset of right set of {} elements!'.format(len(subset), len(superset))
    return True
