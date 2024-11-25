# Shadow Modules


## Discussion
"Shadow Modules" are modules that "shadow" other modules. In effect, they modifies an original stdlib or third party module by side effect and "graft" extra functionality, backports, bugfixes, etc on top of it.

NOTE: This is not a "good" thing since improvements to a module ought to be in the source where it's written, but sometimes you DONT HAVE A CHOICE because:
1. you're version locked - say in a situation where you're not allowed to use a different version of a runtime or library
2. dont have an internet connection and can't just upgrade whenever you want
3. upgrading would cause new unintentional side effects like removing features you do like or requiring a refactor that upends the original code philosophy or
4. Sometimes you just dont like the way the original stuff behaves but want to change just that ONE thing and leave the rest.

Most people would simply make their own other module, name it something different, and then import from there, but that would likely mean copying and pasting the entire source of the original and spending a lot of time fine tuning. I've found that its a lot more intuitive *for me* to graft the functionality I want because the rest of the core is pretty friggen solid.


## How to accomplish
Say you want to modify the `logging` library.
1. create a file called `logging.py`
    - normally this causes a huge problem. say you have a root that looks like this:
        ```
        root
            - logging.py
        ```
    - and then `cd root` and run `python -c "import logging; logging.basicConfig(level=logging.DEBUG)"`. You will get an attribute error because this NEW `logging.py` is empty! It doesnt know that you MEANT to ask the stdlib logging library for `basicConfig` because the top of the import stack via `sys.path` is always the current working directory. So the solution is that during import (aka execution by side effect) you actually tell the interpeter to not look in the current directory (which is autoloaded to the top of the `sys.path` stack), make your adjustments, and then undo the path modifications, the import completes, and nobody is the wiser.

2. stick this code in there
    ```python
    # "shadow module" hack
    if sys.path[0] == '':  # occurs in interactive mode
        __old_path = sys.path
        sys.path = sys.path[1:] + ['']
    else:
        __old_path = []

    # import the original unmodified module which can be used in modifications below
    import logging
    # polutes this "shadow module" locals with the original locals, allowing it to behave as normal
    from logging import *

    ### INSERT CODE HERE ###

    # undo "shadow module" mods
    if __old_path:
        sys.path = __old_path
    ```

## Usage
there are three types of usage models:
1. explitly show in code that it's a side effect and overrides
    ```python
    import chriscarl.shadow.stdlib.library as library
    library.custom_function()
    ```
2. implicitly cause side effects and override
    ```python
    from chriscarl.shadow.stdlib.library import custom_function
    import library
    custom_function()
    library.custom_function()
    ```
3. compromise and import the original module, realizing it's been overridden
    ```python
    from chriscarl.shadow.stdlib.library import library
    library.custom_function()
    ```
