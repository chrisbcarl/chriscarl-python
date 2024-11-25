# TODO
DO NOT COMMIT THIS SHIT AS IS YET DO NOT FUCKING DO IT
- dev
    define the templates, check that everything matches the templates based on the path of the file
    create module, therefore creates a test case for it
    commit, does all of the pre-commit and other shit i need to do
    implement the full workflow, partial workflow, etc.
    create a service which runs stubgen continually
        stubgen src\chriscarl -o dist/typing
- on commit
    scan for and replace / remove
        f' strings
    stubgen src\chriscarl -o dist/typing
    make sure all files in files have a corresponding constant
- logging
    ```python
    console_log(lognames=[__name__, 'chriscarl'], level=logging.VERBOSE)  # pylint: disable=no-member
    change to console_log()  # which defaults to __name__, level verbose
    LOGGER.info('this is a cannonical way of making files here.')
    ```
    - self modifying format that elongates its prints based on the last longest and internally justifies


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