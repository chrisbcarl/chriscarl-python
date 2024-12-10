#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-12-09
Description:

core.lib.stdlib.ast is about Abstract Syntax Trees and the neat things you can do when you self-analyze.
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Updates:
    2024-12-09 - core.lib.stdlib.ast - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import ast
from typing import Union, Optional, Dict, Iterable

# third party imports

# project imports
from chriscarl.core.lib.stdlib.typing import isinstance_raise

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/ast.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

FUNCTION_GRAPH = Dict[str, Optional['FUNCTION_GRAPH']]


def get_function_graph(node):
    # type: (Union[str, ast.Module, ast.FunctionDef, ast.ClassDef]) -> FUNCTION_GRAPH
    '''
    Description:
        given a string or ast object
    '''
    isinstance_raise(node, Union[str, ast.Module, ast.FunctionDef, ast.ClassDef])
    if isinstance(node, str):
        node = ast.parse(node)
    graph = {}  # type: FUNCTION_GRAPH
    for subnode in node.body:
        if isinstance(subnode, ast.FunctionDef):
            graph[subnode.name] = get_function_graph(subnode)
        elif isinstance(subnode, ast.ClassDef):
            graph[subnode.name] = get_function_graph(subnode)
    return graph


# def diff_function_graphs(a, b):
#     # type: (FUNCTION_GRAPH, FUNCTION_GRAPH) -> dict
#     # TODO: not sure how to do this one...
#     # "key": type(a) != type(b)
#     # "key": value(a) != value(b)
#     return {}
