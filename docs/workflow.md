# Build
1. `poetry build`


# Setup
This is from MY perspective, a retrospective history of how I started this whole thing.

1. `poetry new chriscarl --src`
2. rename to chriscarl-python
3. add some files, little stuff
4. create virtualenv in-dir
    ```powershell
    # https://python-poetry.org/docs/configuration/#virtualenvscreate
    $env:POETRY_VIRTUALENVS_CREATE = 1
    $env:POETRY_VIRTUALENVS_IN_PROJECT = 1
    poetry install
    ```
5. activate the .venv by setting .vscode/settings.json `"python.defaultInterpreterPath": "${workspaceFolder}\\.venv\\scripts\\python.exe",`
6. install project in editable mode
7. `pip install -e .`

