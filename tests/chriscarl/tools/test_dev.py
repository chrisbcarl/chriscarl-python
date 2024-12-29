#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-26
Description:

chriscarl.tools.dev unit test.

Updates:
    2024-11-26 - tests.chriscarl.tools.dev - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest

# third party imports

# project imports (expected to work)
from chriscarl.core.lib.stdlib.os import make_dirpath
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.tools.dev as lib

SCRIPT_RELPATH = 'tests/chriscarl/tools/test_dev.py'
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
        setUp = super().setUp()
        from chriscarl.core.lib.stdlib.io import write_text_file
        make_dirpath(self.tempdir, 'src/test')
        make_dirpath(self.tempdir, 'tests')
        write_text_file('{}/src/test/a.py'.format(self.tempdir), '')

        self.audit_kwargs = dict(
            mode='audit',
            cwd=self.tempdir,
            module='test',
            author='',
            email='',
            log_level='INFO',
            log_filepath=lib.DEFAULT_LOG_FILEPATH,
            dry=True,
            dirpath=self.tempdir,
            no_modify=True,
            no_verify=True,
        )
        return setUp

    def tearDown(self):
        return super().tearDown()

    def test_case_0_no_arg_conflicts(self):
        lib.Mode.argparser()
        lib.Create.argparser()
        lib.Run.argparser()
        lib.Audit.argparser()

    def test_case_1_audit_clean(self):
        lib.Audit(func=lib.dev.audit_clean, **self.audit_kwargs).run()

    def test_case_2_audit_banned(self):
        lib.Audit(func=lib.dev.audit_banned, **self.audit_kwargs).run()

    def test_case_3_audit_manifest(self):
        lib.Audit(func=lib.dev.audit_manifest, **self.audit_kwargs).run()

    def test_case_5_audit_relpath(self):
        lib.Audit(func=lib.dev.audit_relpath, **self.audit_kwargs).run()

    def test_case_6_audit_stubs(self):
        lib.Audit(func=lib.dev.audit_stubs, **self.audit_kwargs).run()

    def test_case_7_audit_tdd(self):
        lib.Audit(func=lib.dev.audit_tdd, **self.audit_kwargs).run()

    def test_case_8_main(self):
        try:
            sys.argv += ['audit', 'manifest-verify']
            print(sys.argv)
            lib.main()
        except SystemExit:
            pass


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_no_arg_conflicts()
    tc.test_case_1_audit_clean()
    tc.test_case_2_audit_banned()
    tc.test_case_3_audit_manifest()

    tc.test_case_5_audit_relpath()
    tc.test_case_6_audit_stubs()
    tc.test_case_7_audit_tdd()
    tc.test_case_8_main()

    tc.tearDown()
