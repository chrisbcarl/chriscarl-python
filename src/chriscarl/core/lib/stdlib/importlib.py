#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-25
Description:

core.lib.stdlib.importlib is... TODO: lorem ipsum
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Updates:
    2024-11-26 - core.lib.stdlib.importlib - refactored to call them 'walk' and added walk_dirpath_for_module_files
    2024-11-25 - core.lib.stdlib.importlib - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import importlib
from pathlib import Path
from types import ModuleType, TracebackType
from typing import Any, Tuple, List, Union, Callable, Generator, Type

# third party imports

# project imports
from chriscarl.core.lib.stdlib.typing import isinstance_raise

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/importlib.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def walk_dirpath_for_module_files(dirpath):
    # type: (str) -> Generator[Tuple[str, str], None, None]
    visited = set()
    python_path = os.path.dirname(dirpath)
    for dirpath, _, filenames in os.walk(dirpath):
        folder = Path(dirpath)
        if folder.name == '__pycache__':
            continue

        for filename in filenames:
            file_path = folder.joinpath(filename)
            file_name, file_ext = file_path.stem, file_path.suffix
            if file_ext.lower() != '.py':
                continue

            if file_name == '__init__':
                module_path = Path(dirpath).relative_to(python_path)
                module_path_parts = list(module_path.parts)
            else:
                module_path = Path(file_path).relative_to(python_path)
                if len(module_path.parts) > 1:
                    module_path_parts = list(module_path.parts)[0:-1] + [file_name]
                else:
                    module_path_parts = [file_name]
            module_name = '.'.join(module_path_parts)
            if module_name in visited:
                continue

            yield (module_name, str(file_path))
            visited.add(module_name)


def walk_module_names_filepaths(module=__name__):
    # type: (Union[ModuleType, str]) -> Generator[Tuple[str, str], None, None]
    '''
    Description:
        module: Union[ModuleType, str]
            either provide a module object or just provide the string and we'll import it by side effect.
    Yields:
        Tuple[str, str]
            module dot name
            module filepath
    '''
    isinstance_raise(module, Union[ModuleType, str])  # type: ignore
    if isinstance(module, str):
        module = importlib.import_module(module)

    path = Path(module.__path__[0])
    # now all will be commonly compared to /module
    for module_name, filepath in walk_dirpath_for_module_files(str(path)):
        yield module_name, filepath


def walk_module(module=__name__):
    # type: (Union[ModuleType, str]) -> Generator[Tuple[ModuleType, Union[Tuple[Type, Exception, TracebackType], Tuple[None, None, None]]], None, None]
    '''
    Description:
        module: Union[ModuleType, str]
            either provide a module object or just provide the string and we'll import it by side effect.
    Yields:
        Tuple[ModuleType, Union[Tuple[Type, Exception, TracebackType], Tuple[None, None, None]]]
        Module
        sys.exc_info() or (None, None, None)
    '''
    for module_name, _ in walk_module_names_filepaths(module=module):
        try:
            module = importlib.import_module(module_name)
            yield module, (None, None, None)
        except Exception:
            LOGGER.warning('%r wasnt importable for some reason!', module_name)
            yield module, sys.exc_info()  # type: ignore
