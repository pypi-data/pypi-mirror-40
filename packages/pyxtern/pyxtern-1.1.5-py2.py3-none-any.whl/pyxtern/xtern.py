"""This module provides a decorator to perform external program calls in a
handy manner.
"""

import functools as ft
import logging as lg
import os.path as op
import subprocess as sp
import sys

from .utils import _temporary_directory, _log_to_streams, _check_cmd

log = lg.getLogger(__name__)


class Cmd(list):

    def __init__(self, cmd=None):
        super().__init__()
        self.append(cmd)

    def append(self, object):
        super().append(object)
        return self

    def extend(self, iterable):
        super().extend(iterable)
        return self

    def add_arg(
            self,
            kwargs=None,
            val=None,
            arg=None,
            alias=None,
            prefix="",
            suffix=None,
            flag=False,
            default=None):
        param = "{}{}".format(prefix, arg)
        if kwargs or val:
            # Get value
            if kwargs and not val:
                if alias:
                    val = kwargs.pop(alias, default)
                else:
                    val = kwargs.pop(arg, default)
            if flag:
                # Create arg string
                if val:
                    self.append(param)
            else:
                # Format value
                if val:
                    if isinstance(val, list):
                        val = " ".join(list(map(str, val)))
                    else:
                        val = str(val)
                    # Create arg string
                    if suffix:
                        param = "{}{}{}".format(param, suffix, val)
                        self.append(param)
                    else:
                        self.extend([param, val])
        return self

    def add_args(
            self,
            kwargs=None,
            args=None,
            prefix="",
            suffix=None,
            flag=False,
            default=None):
        if kwargs:
            if isinstance(args, list):
                for arg in args:
                    self.add_arg(
                        kwargs=kwargs,
                        arg=arg,
                        prefix=prefix,
                        suffix=suffix,
                        flag=flag,
                        default=default
                    )
            elif isinstance(args, dict):
                for alias, arg in args.items():
                    self.add_arg(
                        kwargs=kwargs,
                        arg=arg,
                        alias=alias,
                        prefix=prefix,
                        suffix=suffix,
                        flag=flag,
                        default=default
                    )
        return self

    def run(self, **kwargs):
        return run(self, **kwargs)


def run(cmd, **kwargs):
    """This function runs a command line in a temporary directory.

    : arg cmd: The packed command line strings.
    : arg dir: The directory where to create a temporary directory. If set
              to'None', it will be created at the system default temporary
              directory. (Default: None)
    : arg tee: If set to 'True', stdout and stderr streams are logged in files
              and duplicated in the current process. If set to 'False', the
              streams are only logged in files. (Default: False)
    : arg log: A tuple containing(stdout, stderr) streams for the caller. If
              not provided, those streams are simply ignored.
              (Default: (None, None))

    :returns: - exit: The exit code of the external command.
              - stdo: The stdout of the external command.
              - stde: The stderr of the external command.
    """
    # Read args and kwargs
    cmd = _check_cmd(cmd)
    dir = kwargs.get("dir", None)
    save = kwargs.get("save", None)
    ignore = kwargs.get("ignore", None)
    tee = kwargs.get("tee", False)
    outl, errl = kwargs.get("log", (None, None))

    # Run command line
    proc = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    with _temporary_directory(dir=dir, save=save, ignore=ignore) as temp:
        # Temporary files
        outf = op.join(temp, "std.out")
        errf = op.join(temp, "std.err")
        with open(outf, "wb") as stdout, open(errf, "wb") as stderr:
            outs = [stdout]
            errs = [stderr]
            # Add process streams
            if tee:
                outs.append(sys.stdout)
                errs.append(sys.stderr)
            # Add caller streams
            if outl:
                outs.append(outl)
            if errl:
                errs.append(errl)
            # Log to streams
            outt = _log_to_streams(proc.stdout, *outs)
            errt = _log_to_streams(proc.stderr, *errs)
            # Wait the end of the forwarding threads
            log.info("Running command '{}'".format(" ".join(cmd)))
            outt.join()
            errt.join()
            proc.communicate()
        # Read stdout and stderr
        with open(outf, "rb") as f:
            stdo = f.read()
        with open(errf, "rb") as f:
            stde = f.read()
    return proc.returncode, stdo.decode("utf-8"), stde.decode("utf-8")


def xtern(func):
    """This decorator is used to run external command line in a proper manner.
    """
    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        cmd = func(*args, **kwargs)
        return run(cmd, **kwargs)
    return wrapper


def format_arg(name, val=None, fmt=None, noval=False):
    """This function formats command lines arguments.

    :arg name: The name of the argument.
    :arg val:  The value of the argument.
    :arg fmt:  The format to use. Accepted formats are:
               "- ", "-- ", "-=", "--="
    :arg noval: If set to 'True', the function only requires a name. If set to
                'False', the function requires a name and a value.

    :returns:  The formated argument name and value.
    """
    arg = []
    if noval and not val:
        return []
    # Add name
    if fmt == "- " or fmt == "-=":
        # -name
        arg.append("-{}".format(name))
    elif fmt == "-- " or fmt == "--=":
        # --name
        arg.append("--{}".format(name))
    else:
        # name
        arg.append(name)
    if noval:
        return arg
    # Add value
    if val:
        val = " ".join(
            list(
                map(
                    str, val
                    if isinstance(val, list) or isinstance(val, tuple)
                    else [val]
                )
            )
        )
        if fmt == "-=" or fmt == "--=":
            return ["{}={}".format(arg[0], val)]
        else:
            arg.append(val)
            return arg
    return []
