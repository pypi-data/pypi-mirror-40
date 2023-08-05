"""This module provides a decorator to perform external program calls in a
handy manner.
"""

import contextlib as cl
import functools as ft
import logging as lg
import os
import os.path as op
import shutil as su
import subprocess as sp
import sys
import tempfile as tf
import threading as th

log = lg.getLogger(__name__)


@cl.contextmanager
def _temporary_directory(dir=None):
    """This function returns a context to create a temporary directory and
    delete it when out of scope.

    :arg dir: The directory where to create a temporary directory. If 'None' or
              not set, it will be created at the system default temporary
              directory.
    """
    # Create the temporary directory
    temp = tf.mkdtemp(dir=dir)
    log.debug("Created temporary directory at: '{}'".format(temp))
    cwd = os.getcwd()
    # Move to the temporary directory
    try:
        os.chdir(temp)
        log.debug("Moved to temporary directory at: '{}'".format(temp))
        yield temp
    # Move back to cwd and remove temporary directory
    finally:
        os.chdir(cwd)
        log.debug("Moved to previous working directory at: '{}'".format(cwd))
        su.rmtree(temp)
        log.debug("Removed temporary directory at: '{}'".format(temp))


def _log_to_streams(ins, *outs):
    """This function allows a stream to be forwarded to multiple other ones.

    :arg ins:  The input stream.
    :arg outs: The output streams.

    :returns:  The forwarding thread.
    """
    # Check if each stream is a file-like object
    outm = [getattr(o, "mode", "w") for o in outs]

    # Function to forward input to output stream
    def forward():
        for l in iter(ins.readline, b""):
            for i, o in enumerate(outs):
                if "b" in outm[i]:
                    o.write(l)
                else:
                    o.write(l.decode("utf-8"))

    # Create the forwarding threads
    t = th.Thread(target=forward)
    t.daemon = True
    t.start()
    log.debug("Started forwarding thread")
    return t


def _check_cmd(cmd):
    """This functions checks wether cmd is a list of strings or not. If not, it
    tries to convert it.

    :arg cmd: The command to check.

    :returns: The formatted list of strings.
    """
    log.debug("Received command '{}'".format(cmd))
    if isinstance(cmd, str):
        cmd = cmd.split()
    elif isinstance(cmd, list):
        for i, s in enumerate(cmd):
            if not isinstance(s, str):
                cmd[i] = str(s)
    log.debug("Converted command to '{}'".format(cmd))
    return cmd


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
    tee = kwargs.get("tee", False)
    outl, errl = kwargs.get("log", (None, None))

    # Run command line
    proc = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    with _temporary_directory(dir=dir) as temp:
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
        if fmt == "-=" or fmt == "--=":
            return ["{}={}".format(arg[0], val)]
        else:
            arg.append(val)
            return arg
    return []
