# TODO
- dev
    version is fucked
    logging wrappers need to go everywhere shortly
    full / all
    new hermione
        scan for changes, make sure theres a documentation that correlates with that.
    commit, does all of the pre-commit and other shit i need to do
    implement the full workflow, partial workflow, etc.
    tdd add something to verify the main section includes all functions either commented or not
        ```python
        import tests
        from tests.chriscarl.mod.lib.stdlib.test_logging import TestCase
        tc = TestCase()
        [ele for ele in dir(tc) if ele.startswith('test')]
        ['test_case_0_ungabunga']
- on commit
    scan for and replace / remove
        f' strings - f'\w
    stubgen src\chriscarl -o dist/typing
    make sure all files in files have a corresponding constant
- logging
    ```python
    console_log(lognames=[__name__, 'chriscarl'], level=logging.VERBOSE)  # pylint: disable=no-member
    change to console_log()  # which defaults to __name__, level verbose
    LOGGER.info('this is a cannonical way of making files here.')
    ```
    - self modifying format that elongates its prints based on the last longest and internally justifies
- git workflow (cicd pipelining): https://github.com/chrisbcarl/chriscarl-python/new/main?filename=.github%2Fworkflows%2Fpython-app.yml&workflow_template=ci%2Fpython-app
- multiversion python package "workflow":https://github.com/chrisbcarl/chriscarl-python/new/main?filename=.github%2Fworkflows%2Fpython-package.yml&workflow_template=ci%2Fpython-package


- typing stub creation
    ```
    # https://stackoverflow.com/questions/76898602/mypy-stub-files-and-vs-code
    # https://stackoverflow.com/questions/41915404/packaging-stub-files
    ```
- look into requirement usages that i've used before and knock them out:
    - app dev: jinja2, xmljson, markdown, sqlalchemy, pyodbc, pywinauto, pywin32, libpqxx-dev, g++, unixodbc-dev, wxPython
    - python metatyping: mypy, pyinstaller, GitPython, pytest-cov,
    - python building: check-manifest
    - python 2 backports: future, pathlib, typing, configparser, enum-compat,funcsigs, regex