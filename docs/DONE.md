# DONE
The opposite of todo!

- is this python 2 compatible, should I make it so...?
    solved via [philosophy\2-vs-3.md](philosophy\2-vs-3.md)
- typing using mypy api to do simple stuff but without using subprocess calls to the api
    - solved via `isof` in `chriscarl.core.lib.stdlib.typing`
    ```python
    # see .venv\Lib\site-packages\mypy\api.py -> .venv\Lib\site-packages\mypy\main.py
    # https://stackoverflow.com/questions/37973820/how-to-perform-type-checking-with-the-typing-python-module
    # https://mypy.readthedocs.io/en/stable/running_mypy.html
    import mypy.api

    def check_type(value, typ):
        program_text = 'from typing import *; v: {} = {}'.format(typ, repr(value))
        normal_report, error_report, exit_code = mypy.api.run(['-c', program_text])
        return exit_code == 0

    int_ = 1
    str_ = 'a'
    list_str_ = ['a']
    list_int_ = [1]
    tuple_int_ = (1,)

    assert check_type(int_, 'int')
    assert not check_type(str_, 'int')
    assert check_type(list_int_, 'List[int]')
    assert not check_type(list_str_, 'List[int]')
    assert check_type(list_int_, 'List[Any]')
    assert check_type(tuple_int_, 'Tuple[int]')
    ```