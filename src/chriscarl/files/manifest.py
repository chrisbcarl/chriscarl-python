#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-24
Description:

files.manifest is literally what it says on the tin
files are modules that elevate files so they can be used in python, either registering the path name or actually interacting with them like data cabinets.

Updates:
    2024-11-24 - files.manifest - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/files/manifest.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

# ###

# ./
DIRPATH_ROOT = SCRIPT_DIRPATH
FILEPATH_DEFAULT_DESCRIPTIONS_JSON = os.path.join(DIRPATH_ROOT, 'default-descriptions.json')
FILEPATH_MANIFEST_PY = os.path.join(DIRPATH_ROOT, 'manifest.py')

# ./templates
DIRPATH_TEMPLATES = os.path.join(SCRIPT_DIRPATH, 'templates')
FILEPATH_MOD_LIB_TEMPLATE = os.path.join(DIRPATH_TEMPLATES, 'mod.lib.template')
FILEPATH_TEMPLATE = os.path.join(DIRPATH_TEMPLATES, 'template')
FILEPATH_TEST_TEMPLATE = os.path.join(DIRPATH_TEMPLATES, 'test.template')
FILEPATH_TOOL_TEMPLATE = os.path.join(DIRPATH_TEMPLATES, 'tool.template')

# ###


def _self_modify():
    # type: () -> bool
    '''
    Description:
        run this to update the DIRPATH_* and FILEPATH_* constants that represent actual file paths
    '''
    from chriscarl.core.functors.python import get_legal_python_name
    me_filepath = os.path.join(SCRIPT_DIRPATH, '{}.py'.format(SCRIPT_NAME))
    with open(me_filepath, 'r', encoding='utf-8') as r:
        lines = r.read().splitlines()
        indexes = [l for l, line in enumerate(lines) if line.startswith('# ###')]

    cwd = os.getcwd()
    os.chdir(SCRIPT_DIRPATH)
    tokens = []
    for d, _, fs in os.walk('./'):
        if '__pycache__' in d:
            continue
        dirname = os.path.basename(d)
        dupper = dirname.upper()
        tokens.append("# {}".format(d))
        if dupper:
            tokens.append("DIRPATH_{} = os.path.join(SCRIPT_DIRPATH, '{}')".format(dupper, dirname))
        else:
            dupper = 'ROOT'
            tokens.append("DIRPATH_ROOT = SCRIPT_DIRPATH")
        for f in fs:
            if '__init__' in f:
                continue
            pname = get_legal_python_name(f)
            tokens.append("FILEPATH_{} = os.path.join(DIRPATH_{}, '{}')".format(pname.upper(), dupper, f))

        tokens.append("")
    os.chdir(cwd)

    new_content = lines[0:indexes[0]] + ['# ###\n'] + tokens + lines[indexes[1]:]
    with open(me_filepath, 'w', encoding='utf-8') as w:
        w.write('\n'.join(new_content))
    return True


def _self_verify():
    # type: () -> bool
    '''
    Description:
        run this to check each of the DIRPATH_* and FILEPATH_* actually exist...
    '''
    lcls = dict(globals())
    for k, v in lcls.items():
        if k.startswith('DIRPATH') and not os.path.isdir(v):
            raise OSError('dir {} at "{}" does not exist!'.format(k, v))
    for k, v in lcls.items():
        if k.startswith('FILEPATH') and not os.path.isfile(v):
            raise OSError('file {} at "{}" does not exist!'.format(k, v))
    return True
