# Workflow for any python packaging project as I have come to understand the grind


## CI/CD - Each Step Per Commit
1. make your bloody changes
2. `pytest` as well as `for test in tests: python test.py`
3. `stubgen src\chriscarl -o dist/typing` - generate stubs and puts them where mypy can analyze them according to `.vscode/settings.json`
4. increment the version
5. change the changelog
6. `git add -A`
7. `git commit -m "message"`
8. `poetry build`



## Setup
This is from MY perspective, a retrospective history of how I started this whole thing.

1. `poetry new chriscarl --src`
    - creates a pyproject.toml and file structure in the `src/module` packaging vein
    - add `packages` in `[tools.poetry]`
2. rename to chriscarl-python
3. add some files, little stuff
4. create virtualenv in-dir
    ```powershell
    # https://python-poetry.org/docs/configuration/#virtualenvscreate
    $env:POETRY_VIRTUALENVS_CREATE = 1
    $env:POETRY_VIRTUALENVS_IN_PROJECT = 1
    poetry install

    # more permanently
    poetry config virtualenvs.in-project true
    poetry install
    ```
5. activate the .venv by setting .vscode/settings.json `"python.defaultInterpreterPath": "${workspaceFolder}\\.venv\\scripts\\python.exe",`
6. install project in editable mode
7. `pip install -e .`


## Additional Setup
1. configure `.vscode/settings.json`
    - set generic vscode settings
    - set the yapf formatter
    - set the default interpreter path
    - set the stub path
    - set the extra paths path
    - set the mypy type checker args
2. `mypy --install-types --non-interactive` install mypy types
3. change the toml and add `mypy` and `pytest` tool additions


## Reinstall
```powershell
Remove-Item -Recurse -Force -Path '.venv'

poetry install
```
