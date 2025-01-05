import os
import datetime
import pprint
from chriscarl.core.lib.stdlib.ast import is_python, diff_python_strings
from chriscarl.core.lib.stdlib.io import read_bytes_file, write_bytes_file, read_text_file, write_text_file
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.fnmatch import walk
from chriscarl.core.lib.stdlib.subprocess import launch_editor
from chriscarl.core.lib.third.git import get_repo_changes
from chriscarl.core.functors.python import ModuleDocumentation
from chriscarl.core.lib.stdlib.re import find_index
from git import Actor, Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError  # pylint: disable=unresolved-import  # noqa: E402
from git.diff import Diff
from typing import List, Tuple, Optional, Dict
import ast


'''
overall algo:
    --commit-prior HEAD[default]
    --commit-current None[default]

    cmds
        dev vca docs
    algo
        unstage everything
        for file in changed
            if the file is in the module tree and valid python:
                diff ast
                generate a docstring with the new additions

    cmds
        dev vca cl (changelog)
        dev vca cl (assumes a patch increase, rather than minor increase)
    algo
        stage everything
        for file in added/removed/changed/moved
            add to the changelog
        unstage everything

    cmds
        dev vca ver
        dev vca ver --type patch[default],major,minor,label,prerelease --value 1[default] --action increment[default]
    algo
        run docs, ensure no changes need to be flushed, otherwise tell user to run docs if not --force
        run cl, ensure no changes need to be flushed, otherwise tell user to run docs if not --force
        if minor or greater
            run the test suite, there must not be a single problem in the coverage
        bump the pyproj.toml
        go through all docs, get any docstrings modified between last commit date and now
        git add -A
        git commit -m messages
        git push
        if minor or greater
            publish to pypi

    cmds
        dev vca init
    algo
        git init
        changelog add
        pyproj add
        readme add
        if 3 commits:
            for 0->1, 1->2, 2->unstaged
            run docs

    cmds
        dev vca history
    algo


    for file in CHANGED
    if the file is in the module tree, is valid python,
update the changelog with
  changed, added, deleted, moved
bump the version
figure out a way to analyze this all the way in reverse from commit to commit
'''

def update_docstrings_based_on_git_changes(dirpath, dry=False, launch=True):
    # type: (str, bool, bool) -> Dict[str, List[str]]
    changelog = {'added': [], 'removed': [], 'changed': []}
    relevant_files = set(walk(dirpath, include='src/**', exclude=abspath(dirpath, '.gitignore'), relpath=True))
    changes = get_repo_changes(dirpath)
    for tpl in changes.get('M', []):
        relpath = tpl[0]
        if relpath not in relevant_files:
            continue
        old_content = tpl[2].decode('utf-8')
        if not is_python(old_content):
            continue
        filepath = abspath(dirpath, relpath)
        new_content = read_text_file(filepath)
        added, removed, changed = diff_python_strings(old_content, new_content)
        if not any((added, removed, changed)):
            continue
        diffs = {'added': added, 'removed': removed, 'changed': changed}
        last_modified = datetime.datetime.fromtimestamp(os.stat(filepath).st_mtime)
        last_modified_date = datetime.datetime(year=last_modified.year, month=last_modified.month, day=last_modified.day)
        tree = ast.parse(new_content)
        docstring = ast.get_docstring(tree)
        md = ModuleDocumentation.parse(docstring)
        module_tokens = relpath.split('/')
        module_tokens[-1] = module_tokens[-1].replace('.py', '')
        module_name = '.'.join(module_tokens[2:])
        last_updated = max(md.updates)
        texts = []
        for key, values in diffs.items():
            if not values:
                continue
            changelog[key].append('{} - {}'.format(module_name, ', '.join(values)))
            value_tokens = []
            for value in values:
                if not any(value in update for update in md.updates[last_updated]):
                    value_tokens.append(value)
            if value_tokens:
                texts.append('{} - {} {}'.format(module_name, key, ', '.join(value_tokens)))
        if texts:
            if last_modified_date != last_updated:
                md.updates[last_modified_date] = texts
            else:
                md.updates[last_modified_date].extend(texts)

            if not dry:
                docstring_indexes = list(find_index("'''", new_content))
                actual_new_content = new_content[0:docstring_indexes[0] + 3] + md.to_string() + new_content[docstring_indexes[1]:]
                write_text_file(filepath, actual_new_content)
                if launch:
                    launch_editor(filepath)
    return changelog


update_docstrings_based_on_git_changes('./', dry=True)

