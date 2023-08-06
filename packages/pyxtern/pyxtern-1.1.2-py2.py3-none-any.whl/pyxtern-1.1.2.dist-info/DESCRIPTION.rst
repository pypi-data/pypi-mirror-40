# pyxtern

This package provides decorators and methods to run any external command line in a proper maner. It allows the creation of any command line python interface with ease.

## How to install

Since `pyxtern` is hosted on [PyPI](https://pypi.org/project/pyxtern/), it can be installed using:
```shell
pip install pyxtern
```

## How to use

The package offers two different ways to run a command line through python script:

1. Use the `run()` function:  
```python
from pyxtern import run
# To run the following command:
# $ find . -name *.py
# Use either:
exit, stdout, stderr = run("find . -name *.py")
# Or:
exit, stdout, stderr = run(["find", ".", "-name", "*.py"])
```

2. Use the `@xtern` decorator:
```python
from pyxtern import xtern, format_arg
# To wrap the 'find' command:
# $ find . -name *.py
@xtern
def cmd_find(*args, **kwargs):
        cmd = ["find"]
        cmd.append(kwargs.get("path", "."))
        cmd.extend(
            format_arg(
                "name",
                val=kwargs.get("expr", None),
                fmt="- "))
        return cmd
# Now to use it simply write:
cmd_find(expr="*.py")
```

The more complete example for the `find` command is available [here](https://gitlab.com/mar.grignard/pyxtern/blob/master/examples/example_find.py).

## Arguments
The `run()` function accepts some arguments:
- `dir`: The directory where you want to create the temporary directory in which the external command will be ran. If `None`, the system default temporary directory is used.
- `tee`: If set to `True`, the stdout and stderr streams of the external command are rederected to the current stdout and stderr.
- `log`: A tuple givind (stdout, stderr) for the caller. If they are provided, the stdout and stderr streams of the external command are rederected to these.

Both `tee` and `log` can be used at the same time.  
When you use the `@xtern` decorator, these arguments can be passed to the function through `**kwargs`.

## Returns
As shown before, the `run()` function has 3 return values:
- `exit`: The exit code of the external command.
- `stdo`: The stdout of the external command.
- `stde`: The stderr of the external command.


