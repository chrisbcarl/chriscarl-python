#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-12-04
Description:

core.lib.third.git wraps GitPython which installs the "git" library and is only depended on by the "dev git" scriplet.
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Updates:
    2024-12-04 - core.lib.third.git - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import datetime
from typing import Generator, Tuple, List, Union, Optional

# third party imports
try:
    from git import Actor, Repo
    from git.exc import InvalidGitRepositoryError, NoSuchPathError  # pylint: disable=unresolved-import  # noqa: E402
except ImportError:
    print('git package not installed, please run "pip install GitPython" or "poetry add GitPython --group dev" or "poetry install --with dev"')
    sys.exit(1)

# project imports
from chriscarl.core.constants import NOW
from chriscarl.core.lib.stdlib.typing import isinstance_raise
from chriscarl.core.lib.stdlib.os import abspath, make_dirpath, as_posix
from chriscarl.core.types.version import Version
from chriscarl.files.manifest import FILEPATH_CHANGELOG_MD, FILEPATH_README_MD

SCRIPT_RELPATH = 'chriscarl/core/lib/third/git.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

DEFAULT_VERSION = Version.parse('0.0.0')
DEFAULT_DESCRIPTION = 'default description'
DEFAULT_AUTHORS = ['Your Name <here@plz.com>']


def add_changelog_readme_pyproject(dirpath, name='', version=DEFAULT_VERSION, authors=None, codeword='', created=NOW, modified=NOW, force=False):
    # type: (str, str, Union[str, Version], Optional[List[str]], str, datetime.datetime, datetime.datetime, bool) -> List[str]
    '''
    Description:
        create a CHANGELOG.md, README.md, and pyproject.toml if they do not yet exist
    Returns:
        List[str]
            a list of the added files
    '''
    isinstance_raise(version, Union[str, Version])
    dirpath = abspath(dirpath)
    version = version if isinstance(version, Version) else Version.parse(version)
    name = name or os.path.basename(dirpath)
    authors = authors or DEFAULT_AUTHORS

    changelog_filepath = os.path.join(dirpath, 'CHANGELOG.md')
    readme_filepath = os.path.join(dirpath, 'README.md')
    pyproject_filepath = os.path.join(dirpath, 'pyproject.toml')

    changed_files = []

    make_dirpath(dirpath)
    try:
        _ = Repo(dirpath)
    except InvalidGitRepositoryError:
        LOGGER.warning('"%s" is not a valid git repository', dirpath)
        if force:
            LOGGER.warning('FORCE - initializing git repository "%s"', dirpath)
            _ = Repo.init(dirpath)

    # if not os.path.isfile(dirpath_ABOUT) or force:
    #         LOGGER.debug('creating about file "%s"')
    #     if not dry:
    #         template = file_text(ABOUT_TEMPLATE)
    #         with open(dirpath_ABOUT, 'w') as w:
    #             w.write(template.format(name=dirpath_NAME))
    #         changed_files.append(dirpath_ABOUT)
    #     LOGGER.info('created {}'.format(dirpath_ABOUT))
    # else:
    #     LOGGER.verbose('{} exists'.format(dirpath_ABOUT))
    # if not os.path.isfile(dirpath_CHANGELOG):
    #     if not dry:
    #         template = file_text(CHANGELOG_TEMPLATE)
    #         with open(dirpath_CHANGELOG, 'w') as w:
    #             w.write(template.format(name=dirpath_NAME))
    #         changed_files.append(dirpath_CHANGELOG)
    #     LOGGER.info('created {}'.format(dirpath_CHANGELOG))
    # else:
    #     LOGGER.verbose('{} exists'.format(dirpath_CHANGELOG))
    # if not os.path.isfile(dirpath_README):
    #     if not dry:
    #         template = file_text(README_TEMPLATE)
    #         with open(dirpath_README, 'w') as w:
    #             w.write(template.format(name=dirpath_NAME))
    #         changed_files.append(dirpath_README)
    #     LOGGER.info('created {}'.format(dirpath_README))
    # else:
    #     LOGGER.verbose('{} exists'.format(dirpath_README))

    return changed_files


def git_tracked_and_untracked_files(repository_path):
    # type: (str) -> List[Tuple[str, str, str]]
    '''
    Description:
        given a repository path, hopefully a real git repository, return all untracked, tracked, and staged files
    Returns:
        List[Tuple[str, str, str]]
            status letter
                M/D/U
            current file name
            prior file name
    '''
    true_path = os.path.abspath(repository_path)
    repo = Repo(true_path)
    tracked = [(item.change_type, item.a_path, item.b_path) for item in repo.index.diff(None)]
    untracked = [('U', item, item) for item in repo.untracked_files]
    if untracked:
        LOGGER.warning('there are some untracked files: {}'.format(untracked))
    staged = []
    try:
        staged = [(item.change_type, item.a_path, item.b_path) for item in repo.index.diff(repo.head.commit)]
    except Exception as e:
        LOGGER.warning('its possible this repo has never had a commit, so theres nothing staged yet. MESSAGE: {}'.format(e))

    relevant = tracked + untracked + staged
    relevant = list(filter(lambda x: x[1].find('CHANGELOG.md') == -1 and x[1].find('ABOUT') == -1, relevant))
    return relevant


def git_history_tracked_and_untracked_files(repository_path, start_commit='tail', end_commit='head'):
    # type: (str, str, str) -> Generator[Tuple[datetime.datetime, str, List[Tuple[str, str, str]]]]
    true_path = os.path.abspath(repository_path)
    repo = Repo(true_path)

    start_i = None
    end_i = None

    commits = []
    commit_stack = list(repo.iter_commits('head'))
    for i, commit in enumerate(commit_stack):
        if commit.hexsha == start_commit:
            start_i = len(commit_stack) - i - 1  # since the indexes will be reversed
        elif commit.hexsha == end_commit:
            end_i = len(commit_stack) - i - 1  # since the indexes will be reversed
        commits.insert(0, commit)

    if start_commit == 'tail':
        start_i = 0
        # because at the tail commit, the diff of the tail and 'null' is everything in the tail
        yield datetime.datetime.fromtimestamp(commits[0].committed_date), 'uninitialized', [('A', key, key) for key in commits[0].stats.files.keys()]
    if end_commit == 'head':
        end_i = len(commits) - 1

    if start_i == end_i:
        raise ValueError('start and end commits are the same... operation cannot continue: "{}" == "{}"'.format(start_commit, end_commit))
    if start_i > end_i:
        raise ValueError('start commit is more recent than end commit... operation cannot continue: "{}" > "{}"'.format(start_commit, end_commit))
    if start_i is None:
        raise ValueError('could not find start commit "{}"'.format(start_commit))
    if end_i is None:
        raise ValueError('could not find end commit "{}"'.format(end_commit))

    for i in range(start_i, end_i):
        first_commit = commits[i]
        second_commit = commits[i + 1]

        file_changes = [(item.change_type, item.a_path, item.b_path) for item in second_commit.diff(first_commit)]
        yield datetime.datetime.fromtimestamp(second_commit.committed_date), second_commit.message, file_changes


def modify_about(about_file, version, value, date, change_created=False, dry=False):
    config = configparser.ConfigParser()

    # else, update the version
    config.read(about_file)
    if change_created:
        config.set('about', 'created', date)
    config.set('about', 'modified', date)
    try:
        semver = config.get('about', 'version')
        semantic_version = SemanticVersion(semver) if semver is not None else '0.0.0'
        semantic_version.update(version, value)
        config.set('about', 'version', str(semantic_version))
    except Exception:
        LOGGER.warning('Exception in {} trying to increment the version. Skipping...'.format(about_file))
        reraise(*sys.exc_info())

    if not dry:
        with open(about_file, 'w') as w:
            config.write(w)
    LOGGER.verbose('updated ABOUT to version {}'.format(semantic_version))

    return semantic_version


def modify_changelog(repository_path, changelog_file, relevant_files, semantic_version, date, message, dry=False):
    true_path = os.path.abspath(repository_path)
    string = ''
    with open(changelog_file) as md:
        string = md.read()
    bang_bang_index = string.find('##')
    pre_bang_bang = ''
    post_bang_bang = ''
    if bang_bang_index != -1:
        pre_bang_bang = string[0:bang_bang_index]
        post_bang_bang = string[bang_bang_index:]
    else:
        pre_bang_bang = string
        post_bang_bang = ''

    for i, tpl in enumerate(relevant_files):
        change, path_a, path_b = tpl
        path_a = os.path.abspath(os.path.join(true_path, path_a)) if path_a is not None else path_a
        path_b = os.path.abspath(os.path.join(true_path, path_b)) if path_b is not None else path_b
        relevant_files[i] = (change, as_posix(path_a), as_posix(path_b))

    insert_string = '## [{}] - {}\n{}\n'.format(semantic_version, date, message)
    added_files = [tup for tup in relevant_files if tup[0] == 'A' or tup[0] == 'U']
    if len(added_files) > 0:
        insert_string += '''### ADDED
{}\n'''.format('\n'.join(['- {}: `{}`'.format(tup[0], tup[1]) for tup in added_files]))

    changed_files = [tup for tup in relevant_files if tup[0] == 'M']
    if len(changed_files) > 0:
        insert_string += '''### CHANGED
{}\n'''.format('\n'.join(['- {}: `{}`'.format(tup[0], tup[1]) for tup in changed_files]))

    renamed_files = [tup for tup in relevant_files if tup[0] == 'R']
    if len(renamed_files) > 0:
        insert_string += '''### RENAMED
{}\n'''.format('\n'.join(['- {}: `{}` -> `{}`'.format(tup[0], tup[2], tup[1]) for tup in renamed_files]))

    removed_files = [tup for tup in relevant_files if tup[0] == 'D']
    if len(removed_files) > 0:
        insert_string += '''### REMOVED
{}\n'''.format('\n'.join(['- {}: `{}`'.format(tup[0], tup[1]) for tup in removed_files]))

    if not dry:
        with open(changelog_file, 'w') as md_w:
            hash_pound_bang = '{}{}\n\n{}'.format(pre_bang_bang, insert_string, post_bang_bang)
            md_w.write(hash_pound_bang)
    LOGGER.verbose('updated CHANGELOG with {} files'.format(len(relevant_files)))


def initialize_repository(
    path,
    message,
    recursive=False,
    dry=False,
    ignore_dir=None,
    force=False,
):
    ignore_dir = ignore_dir or []

    LOGGER.important('initializing')
    changed_files = set()

    repository_path = as_posix(path)
    changelog_file = os.path.join(path, 'CHANGELOG.md')
    new_changes = add_changelog_readme_pyproject(repository_path, dry=dry)
    changed_files = changed_files.union(set(new_changes))
    if recursive:
        for about_file in walk(
            path=path,
            find_file=['ABOUT'],
            ignore_dir=IGNORING + ignore_dir,
            relpath=False,
        ):
            try:
                repository_path = as_posix(os.path.dirname(about_file))
                new_changes = add_changelog_readme_pyproject(repository_path, dry=dry)
                changed_files = changed_files.union(set(new_changes))
            except Exception:
                LOGGER.error('no repository found at {}'.format(repository_path), exc_info=True)

    LOGGER.verbose('processing unstaged changes')
    date = str(datetime.datetime.now())
    relevant_files = git_tracked_and_untracked_files(repository_path, dry=dry)

    # if there aren't any relevant files, don't bother!
    if len(relevant_files) > 0 or force:
        about_file = os.path.join(path, 'ABOUT')
        semantic_version = modify_about(about_file, 'patch', 0, date, dry=dry)
        modify_changelog(repository_path, changelog_file, relevant_files, semantic_version, date, message, dry=dry)
        changed_files.add(about_file)
        changed_files.add(changelog_file)
    else:
        LOGGER.verbose('no relevant files')

    return changed_files


def historize_repository(
    path,
    message,
    type='patch',
    value=1,
    start='tail',
    end='head',
    recursive=False,
    dry=False,
    ignore_dir=None,
    force=False,
):
    ignore_dir = ignore_dir or []

    LOGGER.important('historizing')
    changed_files = set()

    try:
        repository_path = as_posix(path)
        about_file = os.path.join(path, 'ABOUT')
        changelog_file = os.path.join(path, 'CHANGELOG.md')
        changed_files = changed_files.union(set(add_changelog_readme_pyproject(repository_path, dry=dry)))

        LOGGER.verbose('processing between commits "{}" and "{}"'.format(start, end))
        for i, tpl in enumerate(git_history_tracked_and_untracked_files(repository_path, start, end)):
            date, msg, relevant_files = tpl
            # if there aren't any relevant files, don't bother!
            if len(relevant_files) > 0 or force:
                semantic_version = modify_about(about_file, type, value, str(date), change_created=(i == 0 and start == 'tail'), dry=dry)
                modify_changelog(repository_path, changelog_file, relevant_files, semantic_version, str(date), msg, dry=dry)
                changed_files.add(about_file)
                changed_files.add(changelog_file)
            else:
                LOGGER.verbose('no relevant files')

        if end == 'head':
            LOGGER.verbose('processing unstaged changes between {} -> {}'.format(start, end))
            date = str(datetime.datetime.now())
            relevant_files = git_tracked_and_untracked_files(repository_path, dry=dry)

            # if there aren't any relevant files, don't bother!
            if len(relevant_files) > 0 or force:
                semantic_version = modify_about(about_file, type, value, date, dry=dry)
                modify_changelog(repository_path, changelog_file, relevant_files, semantic_version, date, message, dry=dry)
                changed_files.add(about_file)
                changed_files.add(changelog_file)

    except Exception:
        LOGGER.error('problem processing {}'.format(repository_path), exc_info=True)

    return changed_files


def increment_repository(
    path,
    message,
    type='patch',
    value=1,
    recursive=False,
    dry=False,
    ignore_dir=None,
    force=False,
):
    ignore_dir = ignore_dir or []

    LOGGER.important('incrementing')
    date = str(datetime.datetime.now())
    changed_files = set()

    # for all folders that keep an ABOUT ini format
    # counter = Counter('traversing {} tree... '.format(path))
    for about_file in walk(
        path=path,
        find_file=['ABOUT'],
        ignore_dir=IGNORING + ignore_dir,
        relpath=False,
    ):
        # counter.next()
        try:
            repository_path = as_posix(os.path.dirname(about_file))
            REPO = os.path.abspath(repository_path)
            changed_files = changed_files.union(set(add_changelog_readme_pyproject(repository_path, dry=dry)))
            changelog_file = os.path.join(REPO, 'CHANGELOG.md')
            relevant_files = git_tracked_and_untracked_files(repository_path, dry=dry)

            # if there aren't any relevant files, don't bother!
            if len(relevant_files) > 0 or force:
                semantic_version = modify_about(about_file, type, value, date, dry=dry)
                modify_changelog(repository_path, changelog_file, relevant_files, semantic_version, date, message, dry=dry)
                changed_files.add(about_file)
                changed_files.add(changelog_file)
            else:
                LOGGER.important('there were no unstaged files, it looks like there is no diff, so we will just get the last '
                                 'commit to current head')

            if not recursive:
                break
        except Exception:
            LOGGER.error('problem processing {}'.format(repository_path), exc_info=True)

    return changed_files


def init(path):
    return Repo.init(path, bare=True)


def add(path, all=True):
    r = Repo(path)
    r.git.add(A=all)


def commit(path, message, username=None, email=None, date=None):
    r = Repo(path)
    try:
        commit = r.head.commit
        if date is not None:
            commit.authored_date = commit.committed_date = int(date)
        if username is not None and email is not None:
            author = Actor(username, email)
            committer = author
        else:
            LOGGER.warning('using default author, committer')
            author = commit.author
            committer = commit.committer
        r.index.commit(message, author=author, committer=committer)
    except ValueError:
        LOGGER.important('no initial commit, using global user')
        reader = r.config_reader()
        author = Actor(reader.get_value('user', 'name'), reader.get_value('user', 'email'))
        committer = author
        r.index.commit(message, author=author, committer=committer)


def push(path, origin=True):
    try:
        r = Repo(path)
        if origin:
            r.remotes.origin.push()
    except Exception as e:
        LOGGER.warning('Likely no remote has been set up for this yet. Please do that. MESSAGE: {}'.format(e))


def tag(path, name, message, origin=True):
    try:
        r = Repo(path)
        tag = r.create_tag(name, message=message)  # , ref=r.head.commit
        # r.remotes.origin.push(tags=True) all tags
        if origin:
            r.remotes.origin.push(tag)
    except Exception as e:
        LOGGER.warning('Likely no remote has been set up for this yet or that tag already exists. Please do that. MESSAGE: {}'.format(e))
