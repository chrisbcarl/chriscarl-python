#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@chriscarl.com
Date:           2024-11-22
Description:

Tool that is used to do lots of "dev" related things like git pushing, versioning, publishing, templating, conforming, etc.

Updates:
    2024-11-25 - tools.dev - this thing is practically a work of art (lol its late). create/run both work and do it well.
                 tools.dev - added --tool generation, logging reports the fullpath which is so much more satisfying
                 tools.dev - FIX: reruns when not in --force mode had a logic bug which caused tests to be dumped in the wrong place
                 tools.dev - added --no-test and dev create supports a list of modules
    2024-11-22 - tools.dev - initial commit

# TODO: add git commit shit
# TODO: add life cycle shit
# TODO: track which files were generated by this tool and which arent
# TODO: create an auditor that can scan and see who is out of spec wrt relpath, description, tests, what files dont have a counterpart, which do not import correclty, everyone imports instantly, etc.
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import importlib
from importlib import metadata
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Type
from argparse import _SubParsersAction, ArgumentParser, ArgumentError

# third party imports

# project imports
import chriscarl
from chriscarl.core.constants import DATE, TESTS_DIRPATH
from chriscarl.core.functors.misc import LOG_LEVELS, ArgparseNiceFormat
from chriscarl.core.functors.python import run_func_args_kwargs
from chriscarl.core.lib.stdlib.io import read_text_file, write_text_file
from chriscarl.core.lib.stdlib.os import make_dirpath, abspath
from chriscarl.core.lib.stdlib.json import read_json
import chriscarl.files
from chriscarl.files.manifest import (
    FILEPATH_DEFAULT_DESCRIPTIONS_JSON,
    FILEPATH_TEMPLATE,
    FILEPATH_MOD_LIB_TEMPLATE,
    FILEPATH_TEST_TEMPLATE,
    FILEPATH_TOOL_TEMPLATE,
)

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

# argument defaults
DEFAULT_ROOT_LIB = chriscarl.__name__
DEFAULT_METADATA = metadata.metadata(DEFAULT_ROOT_LIB)
DEFAULT_AUTHOR = DEFAULT_METADATA.json['author']
DEFAULT_EMAIL = DEFAULT_METADATA.json['author_email']


@dataclass
class Mode:
    '''
    Generic mode class, its got what everyone has in common.
    '''
    mode: str
    cwd: str
    root_module: str
    author: str
    email: str
    log_level: str

    @classmethod
    def main(cls):
        parser = cls.argparser()
        mode = cls.from_parser(parser)
        logging.basicConfig(format='%(asctime)s - %(levelname)10s - %(filename)s - %(funcName)s - %(message)s', level=mode.log_level)
        sys.exit(mode.run())

    @staticmethod
    def add_common_arguments(parser):
        # type: (ArgumentParser) -> ArgumentParser
        parser.add_argument('--cwd', type=str, default=os.getcwd(), help='cd to this directory')
        parser.add_argument('--root-module', type=str, default=DEFAULT_ROOT_LIB, help='change the default lib? all modes act on this "root".')
        parser.add_argument('--author', type=str, default=DEFAULT_AUTHOR, help='author first last no space')
        parser.add_argument('--email', type=str, default=DEFAULT_EMAIL, help='author email')
        parser.add_argument('--log-level', type=str, default='INFO', choices=LOG_LEVELS, help='log level?')
        return parser

    @classmethod
    def from_parser(cls, parser):
        # type: (ArgumentParser) -> Mode
        ns = parser.parse_args()
        return cls(**vars(ns))

    @classmethod
    def argparser(cls, subparser_root=None):
        # type: (Optional[_SubParsersAction[ArgumentParser]]) -> ArgumentParser
        if not subparser_root:
            mode = ArgumentParser(prog=SCRIPT_NAME, description=__doc__, formatter_class=ArgparseNiceFormat)
        else:
            mode = subparser_root.add_parser(cls.__name__.lower(), description=cls.__doc__, formatter_class=ArgparseNiceFormat)
        return mode

    def run(self):
        # type: () -> int
        LOGGER.info('%s running!', self.__class__.__name__)
        raise NotImplementedError()


DEFAULT_DESCRIPTIONS = read_json(FILEPATH_DEFAULT_DESCRIPTIONS_JSON)


@dataclass
class Create(Mode):
    '''
    Create is one of the CRUD modes allows you to "create" new modules.
    Based on predefined templates, it will create directories, __init__'s, module file, and test cases for you.

    Examples:
    1. dev create lib.whatever
        # creates the following directory structure:
            - src/chriscarl/__init__.py
            - src/chriscarl/lib/__init__.py
            - src/chriscarl/lib/whatever.py
            - tests/chriscarl/test_lib.py
            - tests/chriscarl/lib/test_whatever.py
    2. dev create lib
        # given you ran the above already which assumes certain things, creates the following directory structure:
            - SKIP: src/chriscarl/__init__.py
            - SKIP: src/chriscarl/lib/__init__.py
            - SKIP: src/chriscarl/lib/whatever.py
            - SKIP: tests/chriscarl/lib/test_whatever.py
    2. dev create tools.fib --tool
        # generate a tool with the following files
            - SKIP: src/chriscarl/__init__.py
            - src/chriscarl/tools/__init__.py
            - src/chriscarl/tools.fib.py
            - tests/chriscarl/test_tools.py
            - tests/chriscarl/tools/test_fib.py
    '''
    modules: List[str] = field(default_factory=lambda: [])
    tests_dirpath: str = TESTS_DIRPATH
    force: bool = False
    tool: bool = False
    no_test: bool = False

    @classmethod
    def argparser(cls, subparser_root=None):
        # type: (Optional[_SubParsersAction[ArgumentParser]]) -> ArgumentParser
        mode = super().argparser(subparser_root=subparser_root)

        mode.add_argument('modules', type=str, nargs='+', default=[], help='space-separated, dot-separated module names, ex) "core.lib.stdlib.os" "core.lib.stdlib.sys"')
        mode.add_argument('--tests-dirpath', type=str, default=TESTS_DIRPATH, help='where should the tests go? core.lib will get a tests/module/core/test_lib.py')
        mode.add_argument('--force', '-f', action='store_true', help='overwrite file if exists?')
        mode.add_argument('--tool', '-t', action='store_true', help='make a tool out of this rather than a module (it still gets tests)')
        mode.add_argument('--no-test', '-n', action='store_true', help='do not generate the test')
        Mode.add_common_arguments(mode)

        return mode

    def run(self):
        # type: () -> int
        warnings = 0
        for m, module in enumerate(self.modules):
            if module.startswith(self.root_module):
                raise ValueError('you provided root module {} and module {}, you dont need the root in the 2nd.'.format(self.root_module, module))

            tokens = [self.root_module] + module.split('.')
            module_template = read_text_file(FILEPATH_TEMPLATE)
            test_template = read_text_file(FILEPATH_TEST_TEMPLATE)
            tool_template = read_text_file(FILEPATH_TOOL_TEMPLATE)

            LOGGER.info('inspecting ./src or ./src/%s convention', self.root_module)
            root_src_directory = 'src/{}'.format(self.root_module)
            root_directory = self.root_module
            if not any([os.path.isdir(root_src_directory), os.path.isdir(root_src_directory)]):
                raise OSError('did not detect ./src/{} or ./{} directory! fix this and use either or convention!'.format(self.root_module, self.root_module))
            elif os.path.isdir(root_src_directory):
                root_directory = 'src'
            else:
                root_directory = ''
            module_filename = '{}.py'.format(tokens[-1])
            module_filepath = '/'.join([root_directory, *tokens[:-1], module_filename])
            module_relpath = os.path.relpath(module_filepath, root_directory).replace('\\', '/')

            # create directories
            LOGGER.info('module %d / %d - %s - step 1 - directories', m, len(self.modules) - 1, module)
            current_directory = root_directory
            for t, token in enumerate(tokens[:-1]):
                current_directory = '{}/{}'.format(current_directory, token)
                current_bad_relpath = '{}/{}.py'.format(root_directory, token)
                LOGGER.info('module %d / %d - %s - step 1 - directory from %r - "%s"!', m, len(self.modules) - 1, module, token, current_directory)
                if os.path.isfile(current_bad_relpath):
                    LOGGER.warning(
                        'module %d / %d - %s - step 1 - directory from %r - "%s" is a file "%s"!', m,
                        len(self.modules) - 1, module, token, current_directory, current_bad_relpath
                    )
                    if self.force:
                        LOGGER.critical(
                            'module %d / %d - %s - step 1 - directory from %r - "%s" is a file "%s"! FORCING!', m,
                            len(self.modules) - 1, module, token, current_directory, current_bad_relpath
                        )
                        os.remove(current_bad_relpath)
                    else:
                        warnings += 1
                        continue
                make_dirpath(current_directory)

            # create inits
            LOGGER.info('module %d / %d - %s - step 2 - __init__.py', m, len(self.modules) - 1, module)
            current_directory = root_directory
            for t, token in enumerate(tokens[:-1]):
                current_directory = '{}/{}'.format(current_directory, token)
                current_init_relpath = '{}/__init__.py'.format(current_directory)
                LOGGER.info('module %d / %d - %s - step 2 - __init__.py from %r - "%s"', m, len(self.modules) - 1, module, token, current_init_relpath)
                doit = True
                if os.path.isfile(current_init_relpath):
                    LOGGER.warning('module %d / %d - %s - step 2 - __init__.py from %r - "%s" already exists!', m, len(self.modules) - 1, module, token, current_init_relpath)
                    if self.force:
                        LOGGER.critical(
                            'module %d / %d - %s - step 2 - __init__.py from %r - "%s" already exists! FORCING!', m,
                            len(self.modules) - 1, module, token, current_init_relpath
                        )
                    else:
                        doit = False
                        warnings += 1
                        continue
                if doit:
                    write_text_file(current_init_relpath, '')

            # create module file
            LOGGER.info('module %d / %d - %s - step 3 - module', m, len(self.modules) - 1, module)
            LOGGER.info('module %d / %d - %s - step 3 - module %r - "%s"', m, len(self.modules) - 1, module, token, module_filepath)
            doit = True
            if os.path.isfile(module_filepath):
                LOGGER.warning('module %d / %d - %s - step 3 - module %r - "%s" exists!', m, len(self.modules) - 1, module, token, module_filepath)
                if self.force:
                    LOGGER.critical('module %d / %d - %s - step 3 - module %r - "%s" exists! FORCING!', m, len(self.modules) - 1, module, token, module_filepath)
                else:
                    doit = False
                    warnings += 1

            if doit:
                description_key_length = -1
                default_description = ''
                for k, v in DEFAULT_DESCRIPTIONS.items():
                    if k in module and len(k) > description_key_length:
                        description_key_length = len(k)
                        default_description = '{} are modules that {}'.format(k, v)

                template_kwargs = dict(
                    author=self.author,
                    email=self.email,
                    module_dot_path=module,
                    date=DATE,
                    script_relpath=module_relpath,
                )
                if self.tool:
                    template = tool_template
                else:
                    template_kwargs.update(dict(default_description=default_description, ))
                    template = module_template

                content = template.format(**template_kwargs)
                write_text_file(module_filepath, content)

            if self.no_test:
                LOGGER.warning('skipping test generation!')
            else:
                # create test directories
                LOGGER.info('module %d / %d - %s - step 4 - test directories', m, len(self.modules) - 1, module)
                test_root_directory = abspath(self.tests_dirpath)
                tests_base = os.path.basename(test_root_directory)
                make_dirpath(test_root_directory)

                current_directory = os.path.relpath(test_root_directory, '').replace('\\', '/')
                for t, token in enumerate(tokens[:-1]):
                    current_directory = '{}/{}'.format(current_directory, token)
                    LOGGER.info('module %d / %d - %s - step 4 - test directories from %r - "%s"!', m, len(self.modules) - 1, module, token, current_directory)
                    make_dirpath(current_directory)

                # create tests
                LOGGER.info('module %d / %d - %s - step 5 - tests')
                current_directory = os.path.relpath(test_root_directory, '').replace('\\', '/')
                for t, token in enumerate(tokens):
                    module_so_far = '.'.join(tokens[:t + 1])
                    test_relpath = '{}/test_{}.py'.format(current_directory, token)
                    LOGGER.info('module %d / %d - %s - step 5 - tests from %r - "%s"!', m, len(self.modules) - 1, module, token, test_relpath)
                    doit = True
                    if os.path.isfile(test_relpath):
                        LOGGER.warning('module %d / %d - %s - step 5 - tests from %r - "%s" already exists!', m, len(self.modules) - 1, module, token, test_relpath)
                        if self.force:
                            LOGGER.critical('module %d / %d - %s - step 5 - tests from %r - "%s" already exists! FORCING!', m, len(self.modules) - 1, module, token, test_relpath)
                        else:
                            warnings += 1
                            doit = False

                    if doit:
                        test_module_dot_path = '{}.{}'.format(tests_base, module_so_far)
                        content = test_template.format(
                            author=self.author,
                            email=self.email,
                            date=DATE,
                            module_dot_path=module_so_far,
                            test_module_dot_path=test_module_dot_path,
                            script_relpath=test_relpath,
                        )
                        write_text_file(test_relpath, content)

                    current_directory = '{}/{}'.format(current_directory, token)

        LOGGER.info('module generated at: "%s"', module_filepath)
        if not self.no_test:
            LOGGER.info('test generated at:   "%s"', test_relpath)
        return warnings


@dataclass
class Read(Mode):
    pass


@dataclass
class Update(Mode):
    pass


@dataclass
class Delete(Mode):
    pass


SUB_OPERATIONS = [
    'files._self_modify',
    'files._self_verify',
]


@dataclass
class Run(Mode):
    '''
    Run is an expansion on CRUD, since CRUD is state-less, "Run" adds state.
    Basically "run" any number of functions--things like linting, word replacing, swear jar, etc.

    Examples:
    1. dev run --funcs "files._self_modify" "files._self_verify"
        # runs the following code in the default root module
            - chriscarl.files._self_modify()
            - chriscarl.files._self_verify()
    2. dev run --funcs "vars" "locals" "globals" --root-module "builtins"
        # runs the following code from a different module
            - builtins.vars()
            - builtins.locals()
            - builtins.globals()
    '''
    func_help: str
    funcs: List[str]

    @classmethod
    def argparser(cls, subparser_root=None):
        # type: (Optional[_SubParsersAction[ArgumentParser]]) -> ArgumentParser
        mode = super().argparser(subparser_root=subparser_root)

        muex = mode.add_mutually_exclusive_group(required=True)
        muex.add_argument(
            '--funcs', type=str, nargs='+', default=[], help='module.func_name where full will be <--root-module>.module.func_name, provide multiple to run in series'
        )
        muex.add_argument('--func-help', type=str, help='print the help of a function rather than run it')
        Mode.add_common_arguments(mode)

        return mode

    def run(self):
        # type: () -> int
        try:
            if self.func_help:
                full_name = '{}.{}'.format(self.root_module, self.func_help)
                tokens = full_name.split('.')
                module = importlib.import_module('.'.join(tokens[:-1]))
                func = getattr(module, tokens[-1])
                help(func)
                return 0
            else:
                full_names = ['{}.{}'.format(self.root_module, func) for func in self.funcs]
                funcs = []
                for full_name in full_names:
                    tokens = full_name.split('.')
                    module = importlib.import_module('.'.join(tokens[:-1]))
                    func = getattr(module, tokens[-1])
                    funcs.append(func)

            LOGGER.info('running %d funcs %s!', len(funcs), len(self.funcs))
            results = list(run_func_args_kwargs(funcs, log_level=self.log_level))
            return 0 if all(results) else 1
        except ModuleNotFoundError as mnfe:
            print('ERROR: could not find module {!r} based on provided root {!r} and funcs!'.format(mnfe.name, self.root_module))
            return 1
        except AttributeError as ae:
            print('ERROR: {}, perhaps a mispelled or stale function name {!r}?'.format(' '.join(ae.args), ae.name))
            return 1


MODE_MAP: Dict[str, Type[Mode]] = {
    'create': Create,
    'read': Read,
    'update': Update,
    'delete': Delete,
    'run': Run,
}


def main():
    # type: () -> int
    try:
        parser = ArgumentParser(prog=SCRIPT_NAME, description=__doc__, formatter_class=ArgparseNiceFormat)

        example_mode = list(MODE_MAP)[0]
        modes = parser.add_subparsers(help='which mode do you want? run "{} {} -h" to get help on the {!r} mode'.format(SCRIPT_NAME, example_mode, example_mode))

        for mode_name, Class in MODE_MAP.items():
            mode_parser = Class.argparser(subparser_root=modes)  # type: ignore
            mode_parser.set_defaults(mode=mode_name)
        subparser = [action for action in parser._actions if isinstance(action, _SubParsersAction)][0]
        ns = parser.parse_args()
    except ArgumentError as ae:
        print('ERROR:', ae, file=sys.stderr)
        sys.exit(1)

    if not hasattr(ns, 'mode'):
        raise ArgumentError(subparser, 'you have to provide an mode')

    Class = MODE_MAP[ns.mode]
    mode = Class(**(vars(ns)))

    logging.basicConfig(format='%(asctime)s - %(levelname)10s - %(filename)s - %(funcName)s - %(message)s', level=mode.log_level)
    LOGGER.debug(vars(mode))

    pwd = os.getcwd()
    try:
        if abspath(mode.cwd) != abspath(pwd):
            LOGGER.debug('changing directory to "%s" from "%s"', mode.cwd, pwd)
            os.chdir(mode.cwd)
        return mode.run()
    finally:
        if abspath(mode.cwd) != abspath(pwd):
            LOGGER.debug('changing directory back to "%s" from "%s"', pwd, mode.cwd)
            os.chdir(pwd)


if __name__ == '__main__':
    sys.exit(main())
