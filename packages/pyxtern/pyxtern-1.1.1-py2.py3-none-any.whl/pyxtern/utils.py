import contextlib as cl
import logging as lg
import os
import os.path as op
import shutil as su
import tempfile as tf
import threading as th

log = lg.getLogger(__name__)


@cl.contextmanager
def _temporary_directory(dir=None, save=None, ignore=None):
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
    if save:
        save = op.abspath(save)
    # Move to the temporary directory
    try:
        os.chdir(temp)
        log.debug("Moved to temporary directory at: '{}'".format(temp))
        yield temp
    # Move back to cwd and remove temporary directory
    finally:
        if save:
            su.copytree(temp, save, ignore)
            log.info("Saved result at: '{}'".format(save))
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
