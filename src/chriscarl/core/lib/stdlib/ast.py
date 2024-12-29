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
    2024-12-28 - core.lib.stdlib.ast - added diff_python_strings
    2024-12-11 - core.lib.stdlib.ast - added visit, merge_python
                 core.lib.stdlib.ast - added get__all__, updated merge_python to account for __all__
    2024-12-09 - core.lib.stdlib.ast - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import ast
from typing import Union, Optional, Dict, List, Tuple

# third party imports

# project imports
from chriscarl.core.types.iterable import get, keys, isleaf
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

FUNCTION_GRAPH = Dict[str, Union[str, 'FUNCTION_GRAPH']]


def get_function_graph(node, as_str=False):
    # type: (Union[str, ast.Module, ast.FunctionDef, ast.ClassDef], bool) -> FUNCTION_GRAPH
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
            graph[subnode.name] = ast.unparse(subnode) if as_str else get_function_graph(subnode, as_str=as_str)
        elif isinstance(subnode, ast.ClassDef):
            graph[subnode.name] = get_function_graph(subnode, as_str=as_str)
    return graph


def visit(node, visited=None, names=None):
    # type: (ast.AST, Optional[Dict[tuple, ast.AST]], Optional[List[str]]) -> Dict[tuple, ast.AST]
    '''# C:/Python312/Lib/ast.py'''
    visited = visited if visited is not None else {}  # Dict[tuple, ast.AST]
    names = names if names is not None else []  # List[str]
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        names.append(node.name)
        visited[tuple(names)] = node
    elif isinstance(node, (ast.Constant, ast.Assign, ast.AnnAssign)):
        if len(names) == 0:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    visited[(target.id, )] = node  # type: ignore
            elif isinstance(node, ast.AnnAssign):
                visited[(node.target.id, )] = node  # type: ignore
            # elif isinstance(node, ast.Constant):
            #     visited[(node.value, )] = node
    for _, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    visit(item, visited=visited, names=names)
        elif isinstance(value, ast.AST):
            visit(value, visited=visited, names=names)
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        names.pop()
    return visited


def merge_python(l, r):
    # type: (Union[ast.AST, str], Union[ast.AST, str]) -> str
    '''
    Description:
        given a string or ast of python on the left, add the NEW stuff from the right on top of the left
        >>> merge_python('a = 1', 'b=2')
        >>> ... 'a = 1\nb = 2'

    # TODO: doesnt merge comments for some reason...
    '''
    isinstance_raise(l, Union[str, ast.AST])
    isinstance_raise(r, Union[str, ast.AST])
    l_root, r_root = ast.parse(l) if isinstance(l, str) else l, ast.parse(r) if isinstance(r, str) else r
    l_visited = visit(l_root)
    r_visited = visit(r_root)

    totally_new = [k for k in r_visited if k not in l_visited]
    unnested = []
    nested = []
    for new in totally_new:
        if len(new) > 1:
            nested.append(new)
        else:
            unnested.append(new)
    # handle constants and globals and loose functions first
    for new in unnested:
        l_root.body.append(r_visited[new])  # type: ignore
    # classes and other stuff later.
    for new in nested:
        new_node = r_visited[new]
        old_class_key = (new[0], )
        old_class_node = l_visited[old_class_key]
        old_class_node.body.append(new_node)  # type: ignore

    # if there's an __all__ in the original and its a list
    all_ = l_visited.get(('__all__', ))
    if isinstance(all_, ast.Assign) and hasattr(all_, 'value') and hasattr(all_.value, 'elts'):
        prior = set(ele.value for ele in all_.value.elts)
        for new in unnested + list(set(map(lambda x: x[0], nested))):
            value = new[0]
            if value not in prior:
                all_.value.elts.append(ast.Constant(value=value))

    new_tree = ast.fix_missing_locations(l_root)
    return ast.unparse(new_tree)


def get__all__(root):
    # type: (Union[ast.AST, str]) -> List[str]
    '''
    Description:
        get back a list of all globally available exposed stuff that is either an assignment, class, or function def
    '''
    if isinstance(root, str):
        root = ast.parse(root)
    all_ = []
    visited = visit(root)
    for key in visited:
        if len(key) > 1:
            continue
        all_.append(key[0])
    return all_



def diff_python_strings(l, r):
    # type: (Union[ast.AST, str], Union[ast.AST, str]) -> Tuple[list, list, list]
    '''
    Description:
        diff l r, so if new stuff is in r, they'll be treated as added
    Returns:
        Tuple[list, list, list]
            added
            removed
            changed
    '''
    lg = get_function_graph(l, as_str=True)
    lk = {key for key in keys(lg)}
    rg = get_function_graph(r, as_str=True)
    rk = {key for key in keys(rg)}

    added = rk.difference(lk)
    rmed = lk.difference(rk)
    same = rk.intersection(lk)
    changed = []
    for k in sorted(same):
        lv = get(k, lg)
        rv = get(k, rg)
        if not isleaf(lv) or not isleaf(rv):
            continue
        if lv != rv:
            changed.append(k)
    return list(sorted(added)), list(sorted(rmed)), changed
