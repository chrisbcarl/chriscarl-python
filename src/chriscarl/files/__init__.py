#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Carl, Chris
Email:          chrisbcarl@outlook.com
Date:           2024-11-24
Description:

files - glorified file to constant manifest

Updates:
    2024-11-24 - chriscarl.files - initial commit
'''

# stdlib imports
import os
import sys
import logging

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/libraries/third/parameterized.py'
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

# ./templates
DIRPATH_TEMPLATES = os.path.join(SCRIPT_DIRPATH, 'templates')
FILEPATH_DEV_MODULE_TEMPLATE_PY = os.path.join(DIRPATH_TEMPLATES, 'dev-module.template.py')
FILEPATH_DEV_SHADOW_TEMPLATE_PY = os.path.join(DIRPATH_TEMPLATES, 'dev-shadow.template.py')

# ###


def _self_modify():
    '''
    Description:
        run this to self-analyze and print what you wanna see
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
        tokens.add("# {}".format(d))
        if dupper:
            tokens.add("DIRPATH_{} = os.path.join(SCRIPT_DIRPATH, '{}')".format(dupper, dirname))
        else:
            dupper = 'ROOT'
            tokens.add("DIRPATH_ROOT = SCRIPT_DIRPATH")
        for f in fs:
            if '__init__' in f:
                continue
            pname = get_legal_python_name(f)
            tokens.add("FILEPATH_{} = os.path.join(DIRPATH_{}, '{}')".format(pname.upper(), dupper, f))

        tokens.add("")
    os.chdir(cwd)

    new_content = lines[0:indexes[0]] + ['# ###\n'] + tokens + ['\n# ###\n']
    with open(me_filepath, 'w', encoding='utf-8') as w:
        w.write('\n'.join(new_content))


def _self_verify():
    lcls = dict(globals())
    for k, v in lcls.items():
        if k.startswith('DIRPATH') and not os.path.isdir(v):
            raise OSError('dir {} at "{}" does not exist!'.format(k, v))
    for k, v in lcls.items():
        if k.startswith('FILEPATH') and not os.path.isfile(v):
            raise OSError('file {} at "{}" does not exist!'.format(k, v))
