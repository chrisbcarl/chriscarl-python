# Philosophy - File Structure
Since dependency management is a big deal and I want to do things cleverly, this is my working theory about what goes where and why and use cases.

## File Structure
```text
core - non-self-referential code that everybody else depends on--basically the bedrock on which all other things come
    functors - simple functions that everyone in this codebase is going to use
    types - simple types, complex classes, etc.
    lib - code that USES existing library code, usually as an intermediary for app development
        stdlib
        third
files - literally files that the modules need or use, will be bundled with the wheel
mod - code that OVERWRITES existing library code and modifies it by side effect
    lib
        stdlib
        third
tools - literally tools that are most likely exposed as cli tools

```

## Internal Dependency Resolution Order
- `files` - supreme, not importable, just files
- `core` - supreme, contains code that everyone else will use
    - `core.functors`
        - `core.types`
            - `core.lib` -
                - `mod.lib`
                    - `tools`


## Use Cases
- boolean functors
    - `chriscarl-python` - main repo
    - `src/chriscarl/types/bool.py`
- new algorithms and data structures related to graphs
    - `chriscarl-python` - main repo
    - `src/chriscarl/types/graphs.py`
        - class called `GraphNode`
        - put your algorithms and data structures all in here.
- create a function called `make_loggers` or `add_logging_arguments`
    - `chriscarl-python` - main repo
    - `src/chriscarl/lib/use/stdlib/logging.py`
- augment the original stdlib `subprocess` module
    - `chriscarl-python` - main repo
    - `src/chriscarl/lib/mod/stdlib/subprocess.py`
- make little functions that are related to a third party lib `parameterized` but DO NOT DEPEND on it
    - `chriscarl-python` - main repo
    - `src/chriscarl/lib/use/third/parameterized.py`
- augment the third party `flask` library
    - `chriscarl-python-flask` - new repo "extension"
    - `src/chriscarl/lib/mod/third/flask.py`
- create a tool that can launch an api to expose a SQL DB
    - `chriscarl-python-sql-api` - new repo "extension"
    - `src/chriscarl/tools/sql_api.py`
- create a tool that can assist in development like templating, git pushing, etc
    - this actually breaks the mold, and will be included in the base so that every extension can also use it.
    - `chriscarl-python` - main repo
    - `src/chriscarl/tools/dev.py`
