# TODO
- dev
    full
        scan for changes, make sure theres a documentation that correlates with that.
        audit manifest-modify
        audit relpath
        audit tdd
        audit banned
        remove .pyc
        stubgen src\chriscarl -o dist/typing
        pytest --cov=chriscarl tests/ --cov-report term-missing
            ---------- coverage:
            TOTAL                                            1333    695    48%
            =========================================================================================================== short test summary info ============================================================================================================
            FAILED tests/chriscarl/core/lib/stdlib/test_importlib.py::TestCase::test_walk_module - assert False
            =================================================================================================== 1 failed, 21 passed, 13 skipped in 1.82s ===

    commit, does all of the pre-commit and other shit i need to do
    implement the full workflow, partial workflow, etc.
    create a service which runs stubgen continually
        stubgen src\chriscarl -o dist/typing
    ideally I would make shadow modules and when they make a stubgen, rename them as follows:
        stubgenning logging:
            stubgen -m logging -o dist/typing
            Processed 1 modules
            Generated dist/typing\logging/__init__.pyi
        stubgenning an individual file:
            stubgen .\src\chriscarl\core\lib\stdlib\os.py -o dist/typing
            Processed 1 modules
            Generated dist/typing\chriscarl/core/lib/stdlib/os.pyi
        therefore
            for mod.lib.stdlib.logging, copy dist/typing\chriscarl/core/lib/stdlib/logging.pyi -> dist/typing\logging/__init__.pyi
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