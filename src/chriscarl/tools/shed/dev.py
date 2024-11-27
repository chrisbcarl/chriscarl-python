#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-25
Description:

tools.shed.dev is the "shed" in which all of the "tools" go to pick one up.
tool are modules that define usually cli tools or mini applets that I or other people may find interesting or useful.

Updates:
    2024-11-26 - tools.shed.dev - renamed from lib to shed since pytest got confused with multiple test_lib's
                 tools.shed.dev - added audit_tdd
                 tools.shed.dev - FIX: if a dir already exists for a module, no action is taken rather than making a file as well
    2024-11-25 - tools.lib.dev - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import re
import pydoc
import logging
import importlib
from typing import List, Union, Tuple, Callable, Any, Optional

# third party imports

# project imports
import chriscarl
from chriscarl.core.constants import DATE, REPO_DIRPATH
from chriscarl.core.functors.python import run_func_args_kwargs
from chriscarl.core.lib.stdlib.io import read_text_file, write_text_file
from chriscarl.core.lib.stdlib.json import read_json
from chriscarl.core.lib.stdlib.os import make_dirpath, abspath, chdir
from chriscarl.core.lib.stdlib.importlib import walk_dirpath_for_module_files
from chriscarl.files import manifest

SCRIPT_RELPATH = 'chriscarl/tools/shed/dev.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def create_modules_and_tests(
    root_module, modules, descriptions=None, author='', email='', tests_dirname='tests', cwd=os.getcwd(), force=False, tool=False, no_test=False, no_module=False
):
    # type: (str, List[str], Optional[dict], str, str, str, str, bool, bool, bool, bool) -> List[Tuple[str, str, str]]
    pwd = os.getcwd()
    os.chdir(cwd)
    try:
        descriptions = descriptions or read_json(manifest.FILEPATH_DEFAULT_DESCRIPTIONS_JSON)
        created_type_module_filepaths: List[Tuple[str, str, str]] = []
        warnings = 0
        for m, module in enumerate(modules):
            if module.startswith(root_module):
                raise ValueError('you provided root module {} and module {}, you dont need the root in the 2nd.'.format(root_module, module))

            tokens = [root_module] + module.split('.')
            module_template = read_text_file(manifest.FILEPATH_TEMPLATE)
            test_template = read_text_file(manifest.FILEPATH_TEST_TEMPLATE)
            tool_template = read_text_file(manifest.FILEPATH_TOOL_TEMPLATE)

            LOGGER.info('inspecting ./src or ./src/%s convention', root_module)
            root_src_directory = 'src/{}'.format(root_module)
            root_directory = root_module
            if not any([os.path.isdir(root_src_directory), os.path.isdir(root_src_directory)]):
                LOGGER.critical('did not detect src directory or legacy directory! default creating src directory "%s"', root_src_directory)
                make_dirpath(root_src_directory)
                root_directory = 'src'
            elif os.path.isdir(root_src_directory):
                root_directory = 'src'
            else:
                root_directory = ''
            module_filename = '{}.py'.format(tokens[-1])
            module_filepath = '/'.join([root_directory, *tokens[:-1], module_filename])
            module_relpath = os.path.relpath(module_filepath, root_directory).replace('\\', '/')
            module_dirpath = '/'.join([root_directory, *tokens])

            if no_module:
                LOGGER.warning('skipping module generation!')
            else:
                # create directories
                LOGGER.info('module %d / %d - %s - step 1 - directories', m, len(modules) - 1, module)
                current_directory = root_directory
                for t, token in enumerate(tokens[:-1]):
                    current_directory = '{}/{}'.format(current_directory, token)
                    current_bad_relpath = '{}/{}.py'.format(root_directory, token)
                    LOGGER.info('module %d / %d - %s - step 1 - directory from %r - "%s"!', m, len(modules) - 1, module, token, current_directory)
                    if os.path.isfile(current_bad_relpath):
                        LOGGER.warning(
                            'module %d / %d - %s - step 1 - directory from %r - "%s" is a file "%s"!', m,
                            len(modules) - 1, module, token, current_directory, current_bad_relpath
                        )
                        if force:
                            LOGGER.critical(
                                'module %d / %d - %s - step 1 - directory from %r - "%s" is a file "%s"! FORCING!', m,
                                len(modules) - 1, module, token, current_directory, current_bad_relpath
                            )
                            os.remove(current_bad_relpath)
                        else:
                            warnings += 1
                            continue
                    make_dirpath(current_directory)

                # create inits
                LOGGER.info('module %d / %d - %s - step 2 - __init__.py', m, len(modules) - 1, module)
                current_directory = root_directory
                for t, token in enumerate(tokens[:-1]):
                    module_so_far = '.'.join(tokens[:t + 1])
                    current_directory = '{}/{}'.format(current_directory, token)
                    current_init_relpath = '{}/__init__.py'.format(current_directory)
                    LOGGER.info('module %d / %d - %s - step 2 - __init__.py from %r - "%s"', m, len(modules) - 1, module, token, current_init_relpath)
                    doit = True
                    if os.path.isfile(current_init_relpath):
                        LOGGER.warning('module %d / %d - %s - step 2 - __init__.py from %r - "%s" already exists!', m, len(modules) - 1, module, token, current_init_relpath)
                        if force:
                            LOGGER.critical(
                                'module %d / %d - %s - step 2 - __init__.py from %r - "%s" already exists! FORCING!', m,
                                len(modules) - 1, module, token, current_init_relpath
                            )
                        else:
                            doit = False
                            warnings += 1
                            continue
                    if doit:
                        write_text_file(current_init_relpath, '')
                        created_type_module_filepaths.append(('__init__', module_so_far, abspath(current_init_relpath)))

                # create module file
                if os.path.isdir(module_dirpath):
                    LOGGER.warning(
                        'module %d / %d - %s - step 3 - module %r - "%s" exists as a dir not a module! Not removing or altering at all!', m,
                        len(modules) - 1, module, token, module_dirpath
                    )
                    warnings += 1
                else:
                    LOGGER.info('module %d / %d - %s - step 3 - module', m, len(modules) - 1, module)
                    LOGGER.info('module %d / %d - %s - step 3 - module %r - "%s"', m, len(modules) - 1, module, token, module_filepath)
                    doit = True
                    if os.path.isfile(module_filepath):
                        LOGGER.warning('module %d / %d - %s - step 3 - module %r - "%s" exists!', m, len(modules) - 1, module, token, module_filepath)
                        if force:
                            LOGGER.critical('module %d / %d - %s - step 3 - module %r - "%s" exists! FORCING!', m, len(modules) - 1, module, token, module_filepath)
                        else:
                            doit = False
                            warnings += 1

                if doit:
                    description_key_length = -1
                    default_description = ''
                    for k, v in descriptions.items():
                        if k in module and len(k) > description_key_length:
                            description_key_length = len(k)
                            default_description = '{} are modules that {}'.format(k, v)

                    template_kwargs = dict(
                        author=author,
                        email=email,
                        module_dot_path=module,
                        date=DATE,
                        script_relpath=module_relpath,
                    )
                    template = module_template
                    if tool:
                        template = tool_template
                    else:
                        stdlib_import, third_import = '', ''
                        if 'stdlib.' in module:
                            stdlib_import = '\nimport {}'.format(tokens[-1])
                        elif 'third.' in module:
                            third_import = '\nimport {}'.format(tokens[-1])
                        template_kwargs.update(dict(default_description=default_description, stdlib_import=stdlib_import, third_import=third_import))

                    content = template.format(**template_kwargs)
                    write_text_file(module_filepath, content)
                    created_type_module_filepaths.append(('module', '.'.join(tokens), abspath(module_filepath)))

            if no_test:
                LOGGER.warning('skipping test generation!')
            else:
                # create test directories
                LOGGER.info('module %d / %d - %s - step 4 - test directories', m, len(modules) - 1, module)
                test_root_directory = abspath(tests_dirname)
                tests_base = os.path.basename(test_root_directory)
                make_dirpath(test_root_directory)

                current_directory = os.path.relpath(test_root_directory, '').replace('\\', '/')
                for t, token in enumerate(tokens[:-1]):
                    current_directory = '{}/{}'.format(current_directory, token)
                    LOGGER.info('module %d / %d - %s - step 4 - test directories from %r - "%s"!', m, len(modules) - 1, module, token, current_directory)
                    make_dirpath(current_directory)

                # create tests
                LOGGER.info('module %d / %d - %s - step 5 - tests')
                current_directory = os.path.relpath(test_root_directory, '').replace('\\', '/')
                for t, token in enumerate(tokens):
                    module_so_far = '.'.join(tokens[:t + 1])
                    test_relpath = '{}/test_{}.py'.format(current_directory, token)
                    # test_relpath = '{}/test_{}.py'.format(tests_base, module_so_far)
                    LOGGER.info('module %d / %d - %s - step 5 - tests from %r - "%s"!', m, len(modules) - 1, module, token, test_relpath)
                    doit = True
                    if os.path.isfile(test_relpath):
                        LOGGER.warning('module %d / %d - %s - step 5 - tests from %r - "%s" already exists!', m, len(modules) - 1, module, token, test_relpath)
                        if force:
                            LOGGER.critical('module %d / %d - %s - step 5 - tests from %r - "%s" already exists! FORCING!', m, len(modules) - 1, module, token, test_relpath)
                        else:
                            warnings += 1
                            doit = False

                    if doit:
                        test_module_dot_path = '{}.{}'.format(tests_base, module_so_far)
                        content = test_template.format(
                            author=author,
                            email=email,
                            date=DATE,
                            module_dot_path=module_so_far,
                            test_module_dot_path=test_module_dot_path,
                            script_relpath=test_relpath,
                        )
                        write_text_file(test_relpath, content)
                        created_type_module_filepaths.append(('test', module_so_far, abspath(test_relpath)))

                    current_directory = '{}/{}'.format(current_directory, token)

            if not no_module:
                LOGGER.info('module generated at: "%s"', module_filepath)
            if not no_test:
                LOGGER.info('test generated at:   "%s"', test_relpath)
        return created_type_module_filepaths
    finally:
        os.chdir(pwd)


def run_functions_by_dot_path(root_module, func_names, print_help=False, log_level='DEBUG'):
    # type: (str, List[str], bool, Union[str, int]) -> int
    try:
        full_names = ['{}.{}'.format(root_module, func_name) for func_name in func_names]
        funcs: List[Union[Callable, Tuple[Callable, Any]]] = []
        for full_name in full_names:
            tokens = full_name.split('.')
            module = importlib.import_module('.'.join(tokens[:-1]))
            func = getattr(module, tokens[-1])
            if print_help:
                funcs.append((pydoc.render_doc, (func, )))
            else:
                funcs.append(func)

        LOGGER.info('running %d funcs %s!', len(funcs), len(funcs))
        results = list(run_func_args_kwargs(funcs, log_level=log_level))  # type: ignore
        return 0 if all(results) else 1
    except ModuleNotFoundError as mnfe:
        LOGGER.error('could not find module %r based on provided root %r and funcs!', mnfe.name, root_module)
        LOGGER.debug('exception', exc_info=True)
        return 1
    except AttributeError as ae:
        LOGGER.error('%s, perhaps a mispelled or stale function name %r?', ' '.join(ae.args), ae.name)
        LOGGER.debug('exception', exc_info=True)
        return 1


def audit_manifest_modify():
    # type: () -> bool
    '''
    Description:
        update the files manifest
        run this to update the DIRPATH_* and FILEPATH_* constants that represent actual file paths
    '''
    from chriscarl.core.functors.python import get_legal_python_name
    importlib.reload(manifest)
    LOGGER.info('analyzing "%s"', manifest.__file__)
    manifest_filepath = abspath(manifest.__file__)
    with open(manifest_filepath, 'r', encoding='utf-8') as r:
        lines = r.read().splitlines()
        indexes = [l for l, line in enumerate(lines) if line.startswith('# ###')]

    with chdir(os.path.dirname(manifest.__file__)):
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

    new_content = lines[0:indexes[0]] + ['# ###\n'] + tokens + lines[indexes[1]:]
    LOGGER.info('writing %d lines of filepath content', len(tokens))
    with open(manifest_filepath, 'w', encoding='utf-8') as w:
        w.write('\n'.join(new_content))
    return True


def audit_manifest_verify():
    # type: () -> int
    '''
    Description:
        verify the files manifest
        run this to check each of the DIRPATH_* and FILEPATH_* actually exist...
    '''
    importlib.reload(manifest)
    lcls = dict(vars(manifest))
    for k, v in lcls.items():
        if k.startswith('DIRPATH') and not os.path.isdir(v):
            raise OSError('dir {} at "{}" does not exist!'.format(k, v))
    for k, v in lcls.items():
        if k.startswith('FILEPATH') and not os.path.isfile(v):
            raise OSError('file {} at "{}" does not exist!'.format(k, v))
    return 0


SCRIPT_RELPLATH_REGEX = re.compile(r"SCRIPT_RELPATH = r?'[\d\w\-\\\/\.]+\.py'")
IGNORED_DIRS = ['ignoreme', 'node_modules', '.git', '__pycache__', 'build', 'dist', 'venv', '.venv', '.pytest_cache']
DEFAULT_EXTENSIONS = ['.py']


def audit_relpath(dirpath=os.getcwd(), extensions=DEFAULT_EXTENSIONS, included_dirs=None, ignored_dirs=IGNORED_DIRS, dry=False):
    # type: (str, List[str], Optional[List[str]], List[str], bool) -> int
    '''
    Description:
        find every file that contains        SCRIPT_RELPATH = 'chriscarl/tools/shed/dev.py'
        and convert them into something like SCRIPT_RELPATH = 'chriscarl/tools/shed/dev.py'

    Arguments:
        dirpath: str
            where do we start crawling?
        extensions: List[str]
            which files should we look at?
        included_dirs: List[str]
            any directories that you do care about, and run them relatively to dirpath?
        ignored_dirs: List[str]
            any directories you dont care about?
        dry: bool
            do not write?
    '''
    original_dirpath = abspath(dirpath)
    included_dirs = included_dirs or []
    included_dirs = [abspath(dp) for dp in included_dirs]
    LOGGER.debug('going through "%s"...', original_dirpath)
    extensions = extensions or []
    chars = 128  # if verbose else 16
    changes = 0

    try:
        filepaths = []
        for dirpath, dirnames, filenames in os.walk(original_dirpath):
            # https://stackoverflow.com/questions/31449731/how-to-skip-directories-in-os-walk-python-2-7
            skip_these = []
            for dirname in dirnames:
                if dirname in ignored_dirs:
                    skip_these.append(dirname)
            for skip in skip_these:
                dirnames.remove(skip)
            if not any(included_dir in dirpath for included_dir in included_dirs):
                continue
            for filename in filenames:
                _, ext = os.path.splitext(filename)
                if ext not in extensions:
                    continue
                filepath = os.path.join(dirpath, filename)
                filepaths.append(filepath)

        for filepath in filepaths:
            use_filepath = filepath
            basename = os.path.basename(filename)
            relpath = os.path.relpath(use_filepath, original_dirpath).replace('\\', '/')
            if 'src/' in relpath:
                relpath = relpath.replace('src/', '')
            with open(filepath) as r:
                contents = r.read()
            search = SCRIPT_RELPLATH_REGEX.search(contents)
            LOGGER.debug('%s: "%s"', 'something' if bool(search) else 'notathing', filepath)
            if search:
                replacement = replacement_preview = "SCRIPT_RELPATH = '{}'".format(relpath)
                original = original_preview = search.string[search.start():search.end()]
                if len(original) > chars:
                    original_preview = original_preview[0:chars - 3] + '...'
                if len(replacement_preview) > chars:
                    replacement_preview = replacement_preview[0:chars - 3] + '...'

                if replacement != original_preview:
                    LOGGER.debug('replacing %s %r %r', relpath, replacement, original_preview)
                    lines = contents[:search.end()].splitlines()
                    lineno = len(lines) + 1
                    charno = len(lines[-1])  # just a best effort
                    changes += 1
                    if not dry:
                        LOGGER.info('replacing %s %r -> %r', '{} [line:{}; char:{}]: '.format(basename, lineno, charno), original_preview, replacement_preview)
                        new_contents = SCRIPT_RELPLATH_REGEX.sub(replacement, contents)
                        with open(filepath, 'w') as w:
                            w.write(new_contents)
        LOGGER.info('%d changes', changes)
        if dry and changes > 0:
            LOGGER.warning('remember to remove --dry if youd like to flush these changes.')
    except Exception:
        LOGGER.error('something happened trying to replace relpaths on filename {!r}'.format(filename), exc_info=True)
        LOGGER.debug(locals())
        return 1
    return 0


def audit_tdd(
    dirpath=REPO_DIRPATH,
    module_name=chriscarl.__name__,
    tests_dirname='tests',
    dry=True,
    author='',
    email='',
    descriptions=None,
    cwd=os.getcwd(),
    force=False,
    tool=False,
    no_test=False,
    no_module=False,
):
    # type: (str, str, str, bool, str, str, Optional[dict], str, bool, bool, bool, bool) -> int
    '''
    Description:
        check to see which files have a corresponding test, which files do not, and which tests are abandoned
        this wont work on non-pypa repo packages like installed or .pyc packaged packages.
    '''
    top_module_name = module_name
    src_to_test = {}
    src_to_file = {}
    test_to_src = {}
    test_to_file = {}
    # test_module_prepend = 'tests.test_'
    with chdir(dirpath):
        # src
        for module_name, filepath in walk_dirpath_for_module_files(module_name):
            tokens = module_name.split('.')
            tokens[-1] = 'test_{}'.format(tokens[-1])
            test_module_tokens = [tests_dirname] + tokens
            test_module = '.'.join(test_module_tokens)
            # test_module = '{}{}'.format(test_module_prepend, module_name)
            src_to_test[module_name] = test_module
            src_to_file[module_name] = filepath
        for module_name, filepath in walk_dirpath_for_module_files('src/{}'.format(module_name)):
            tokens = module_name.split('.')
            tokens[-1] = 'test_{}'.format(tokens[-1])
            test_module_tokens = [tests_dirname] + tokens
            test_module = '.'.join(test_module_tokens)
            # test_module = '{}{}'.format(test_module_prepend, module_name)
            src_to_test[module_name] = test_module
            src_to_file[module_name] = filepath

        # test
        for module_name, filepath in walk_dirpath_for_module_files(tests_dirname):
            tokens = module_name.split('.')
            tokens[-1] = tokens[-1][5:]  # get rid of the test_ prepend
            src_module_tokens = tokens[1:]
            src_module = '.'.join(src_module_tokens)
            # src_module = module_name[len(test_module_prepend):]
            test_to_src[module_name] = src_module
            test_to_file[module_name] = filepath

    src_without_tests = set(k for k, v in src_to_test.items() if v not in test_to_src)
    orphaned_tests = set(test_to_file[k] for k, v in test_to_src.items() if v not in src_to_test)

    ret = 0
    create_these_modules = [x[len(top_module_name) + 1:] for x in sorted(src_without_tests)]

    if src_without_tests:
        LOGGER.info('recommendation: run the following command line:\n\n    dev create %s --module "%s"\n\n', ' '.join(create_these_modules), top_module_name)
        ret += len(src_without_tests)
        LOGGER.critical('%d src files detected without equivalent tests! %s', len(src_without_tests), sorted(src_without_tests))
    if orphaned_tests:
        LOGGER.info('recommendation: refactor and then remove with the following command lines:\n\n%s\n\n', '\n'.join('    rm "{}"'.format(ele) for ele in orphaned_tests))
        ret += len(orphaned_tests)
        LOGGER.critical('%d orphaned tests detected! %s', len(orphaned_tests), sorted(orphaned_tests))

    if dry:
        LOGGER.critical('skipping test creation for the %d modules that are missing them! pass dry=True to generate them!', len(create_these_modules))
    else:
        LOGGER.critical('creating tests for the %d modules that are missing them!', len(create_these_modules))
        results = create_modules_and_tests(
            top_module_name,
            create_these_modules,
            descriptions=descriptions or read_json(manifest.FILEPATH_DEFAULT_DESCRIPTIONS_JSON),
            author=author,
            email=email,
            tests_dirname=tests_dirname,
            cwd=cwd,
            force=force,
            tool=tool,
            no_test=no_test,
            no_module=no_module,
        )
        return len(results)

    return ret
