# TODO
- dev
    the last thing I was on is trying to compare one file to another via AST, see if functions were added / removed, so I can autogen the changelog
    dict probably should redo flatten in the context of walk to get all of the keys...

    dev new project
        creates a pre-commit
        creates the .vscode
        creates the extensions, etc.
        pyproj toml

    logging wrappers need to go everywhere shortly
    version class is fucked, please simplify
    some kind of exception class that is able to raise exceptions cleanly, with correct relevant traceback localization
        exc_info = sys.exc_info()
        traceback = exc_info[2]
        back_frame = traceback.tb_frame.f_back
        back_tb = TracebackType(tb_next=None, tb_frame=back_frame, tb_lasti=back_frame.f_lasti, tb_lineno=back_frame.f_lineno)
        .with_traceback(back_tb)
        .with_traceback(back_tb)
        .with_traceback(exe.__traceback__)
    audit imports
        test all imports this way:
            modules = walk_module_names_filepaths
            for modules in modules:
                subprocess.popen(python -c import module)
    do pyi stubgen myself with AST analysis and figure out what i've added or changed and then modify the ast directly and THEN print it out.
        basically analyze the AST of original module
        analyze AST of shadow module
        combine what has been changed or added in the new ast
        import ast
        with open(r'C:\Users\chris\src\chriscarl-python\dist\typing\logging\__init__.pyi') as r:
            content = r.read()
        parsed = ast.parse(content)
        print(ast.dump(parsed, indent=4))
        print(ast.unparse(parsed))
    mod.all created
        on new mod.something, add it to all
        edit the templates so that they use all
    mod.logging needs to modify all previously instantiated loggers with the new logger class so they get all level functions...
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