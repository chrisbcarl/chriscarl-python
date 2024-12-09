#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-25
Description:

chriscarl.tools.shed.dev unit test.

Updates:
    2024-11-25 - tests.chriscarl.tools.shed.dev - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging

# third party imports

# project imports (expected to work)
from chriscarl.core.lib.stdlib.unittest import UnitTest
from chriscarl.core.lib.stdlib.os import abspath, make_dirpath
from chriscarl.core.constants import REPO_DIRPATH, PYPA_SRC_DIRPATH, TESTS_DIRPATH

# test imports
import chriscarl.tools.shed.dev as lib

SCRIPT_RELPATH = 'tests/chriscarl/tools/shed/test_dev.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class TestCase(UnitTest):

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_case_0_create_modules_and_tests(self):
        from chriscarl.core.lib.stdlib.io import write_text_file
        write_text_file('{}/test/a.py'.format(self.tempdir), '')
        write_text_file('{}/test/b/__init__.py'.format(self.tempdir), '')
        variables = [
            (lib.create_modules_and_tests, (
                'test',
                ['a.b.c'],
            ), dict(tests_dirname='tests', cwd=self.tempdir, force=True, launch=False)),
            (lib.create_modules_and_tests, (
                'test',
                ['a.b.c'],
            ), dict(tests_dirname='tests', cwd=self.tempdir, force=False, launch=False)),
            (lib.create_modules_and_tests, (
                'test',
                ['a.b.c'],
            ), dict(tests_dirname='tests', cwd=self.tempdir, force=True, launch=False, no_module=True)),
            (lib.create_modules_and_tests, (
                'test',
                ['a.b.c'],
            ), dict(tests_dirname='tests', cwd=self.tempdir, force=True, launch=False, no_test=True)),
            (lib.create_modules_and_tests, (
                'test',
                ['mod.lib.stdlib.plz'],
            ), dict(tests_dirname='tests', cwd=self.tempdir, force=True, launch=False)),
        ]
        controls = [
            [
                ('__init__', 'test', abspath(self.tempdir, 'src/test/__init__.py')),
                ('__init__', 'test.a', abspath(self.tempdir, 'src/test/a/__init__.py')),
                ('__init__', 'test.a.b', abspath(self.tempdir, 'src/test/a/b/__init__.py')),
                ('module', 'test.a.b.c', abspath(self.tempdir, 'src/test/a/b/c.py')),
                ('test', 'test', abspath(self.tempdir, 'tests/test_test.py')),
                ('test', 'test.a', abspath(self.tempdir, 'tests/test/test_a.py')),
                ('test', 'test.a.b', abspath(self.tempdir, 'tests/test/a/test_b.py')),
                ('test', 'test.a.b.c', abspath(self.tempdir, 'tests/test/a/b/test_c.py')),
            ],
            [],
            [
                ('test', 'test', abspath(self.tempdir, 'tests/test_test.py')),
                ('test', 'test.a', abspath(self.tempdir, 'tests/test/test_a.py')),
                ('test', 'test.a.b', abspath(self.tempdir, 'tests/test/a/test_b.py')),
                ('test', 'test.a.b.c', abspath(self.tempdir, 'tests/test/a/b/test_c.py')),
            ],
            [
                ('__init__', 'test', abspath(self.tempdir, 'src/test/__init__.py')),
                ('__init__', 'test.a', abspath(self.tempdir, 'src/test/a/__init__.py')),
                ('__init__', 'test.a.b', abspath(self.tempdir, 'src/test/a/b/__init__.py')),
                ('module', 'test.a.b.c', abspath(self.tempdir, 'src/test/a/b/c.py')),
            ],
            [
                ('__init__', 'test', abspath(self.tempdir, 'src/test/__init__.py')),
                ('__init__', 'test.mod', abspath(self.tempdir, 'src/test/mod/__init__.py')),
                ('__init__', 'test.mod.lib', abspath(self.tempdir, 'src/test/mod/lib/__init__.py')),
                ('__init__', 'test.mod.lib.stdlib', abspath(self.tempdir, 'src/test/mod/lib//stdlib/__init__.py')),
                ('module', 'test.mod.lib.stdlib.plz', abspath(self.tempdir, 'src/test/mod/lib/stdlib/plz.py')),
                ('test', 'test', abspath(self.tempdir, 'tests/test_test.py')),
                ('test', 'test.mod', abspath(self.tempdir, 'tests/test/test_mod.py')),
                ('test', 'test.mod.lib', abspath(self.tempdir, 'tests/test/mod/test_lib.py')),
                ('test', 'test.mod.lib.stdlib', abspath(self.tempdir, 'tests/test/mod/lib/test_stdlib.py')),
                ('test', 'test.mod.lib.stdlib.plz', abspath(self.tempdir, 'tests/test/mod/lib/stdlib/test_plz.py')),
            ],
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_run_functions_by_dot_path(self):
        variables = [
            (lib.run_functions_by_dot_path, ('builtins', ['vars'])),
            (lib.run_functions_by_dot_path, ('not_real', ['print'])),
            (lib.run_functions_by_dot_path, ('builtins', ['not_real'])),
        ]
        controls = [
            0,
            1,
            2,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2_audit_manifest(self):
        from chriscarl.core.lib.stdlib.io import read_bytes_file
        original = read_bytes_file(lib.__file__)

        variables = [
            (lib.audit_manifest),
        ]
        controls = [
            0,
        ]
        self.assert_null_hypothesis(variables, controls)

        new = read_bytes_file(lib.__file__)
        self.assertEqual(original, new, '_self_modify should take effect but be idempotent! something changed, check the git diff?')

    def test_case_4_audit_relpath(self):
        from chriscarl.core.lib.stdlib.io import write_text_file
        lol_py = abspath(self.tempdir, 'lol.py')
        write_text_file(lol_py, "SCRIPT_RELPATH = 'False.py'")
        variables = [
            (lib.audit_relpath, (), dict(dirpath=REPO_DIRPATH, included_dirs=[PYPA_SRC_DIRPATH, TESTS_DIRPATH])),
            (lib.audit_relpath, (), dict(dirpath=self.tempdir)),
        ]
        controls = [
            0,
            0,
        ]
        self.assert_null_hypothesis(variables, controls)
        os.remove(lol_py)

    def test_case_5_audit_tdd(self):
        variables = [
            (lib.audit_tdd, (), dict(dirpath=REPO_DIRPATH, dry=False, tests_dirname='tests', force=True)),
        ]
        controls = [
            0,
        ]
        self.assert_null_hypothesis(variables, controls)

        self.tearDown()
        self.setUp()
        from chriscarl.core.lib.stdlib.io import write_text_file
        write_text_file(abspath(self.tempdir, 'src/test/lol.py'), "SCRIPT_RELPATH = 'False.py'")
        make_dirpath(self.tempdir, 'tests')
        variables = [
            (lib.audit_tdd, (), dict(dirpath=self.tempdir, dry=False, tests_dirname='tests', module_name='test', cwd=self.tempdir)),
        ]
        controls = [
            3,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_6_audit_banned(self):
        import re
        from chriscarl.core.lib.stdlib.io import read_text_file, write_text_file
        from chriscarl.core.lib.stdlib.os import abspath
        from chriscarl.core.constants import REPO_DIRPATH
        _banned = abspath(REPO_DIRPATH, 'ignoreme/_banned')
        included_dirs = ['src/', 'tests']
        words = []
        if os.path.isfile(_banned):
            words_content = read_text_file(_banned)
            words.extend([ele.strip() for ele in re.split(r'\s+', words_content) if ele.strip()])
        variables = [
            (lib.audit_banned, (REPO_DIRPATH, words), dict(include=included_dirs)),
        ]
        controls = [
            {},
        ]

        words = ['SUPERBANNED']
        write_text_file(abspath(self.tempdir, 'src/test/lol.py'), 'SUPERBANNED')
        variables = [
            (lib.audit_banned, (self.tempdir, words), dict(include=included_dirs)),
        ]
        controls = [
            {
                'src/test/lol.py': {
                    'SUPERBANNED': [(1, 1), ],
                }
            },
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_7_audit_stubs(self):
        lib.create_modules_and_tests('test', ['mod.lib.stdlib.logging'], tests_dirname='tests', cwd=self.tempdir, force=True, launch=False)
        variables = [
            (lib.audit_stubs, (), dict(dirpath=self.tempdir, module_name='test')),
        ]
        controls = [
            0,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_8_audit_clean(self):
        from chriscarl.core.lib.stdlib.os import walk
        current_pycs = len(list(walk(REPO_DIRPATH, extensions=['.pyc'])))
        variables = [
            (lib.audit_clean, (), dict(dirpath=self.tempdir)),
            (lib.audit_clean, (), dict(dirpath=REPO_DIRPATH)),
        ]
        controls = [
            0,
            current_pycs,
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_create_modules_and_tests()
    tc.test_case_1_run_functions_by_dot_path()
    tc.test_case_2_audit_manifest()

    tc.test_case_4_audit_relpath()
    tc.test_case_5_audit_tdd()
    tc.test_case_6_audit_banned()
    tc.test_case_7_audit_stubs()
    tc.test_case_8_audit_clean()

    tc.tearDown()
