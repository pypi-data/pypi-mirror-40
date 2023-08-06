from subprocess import call
import sys
import logging

def run_cmd(name, cmd):
    """ Run a command and stdout print in console.
    ::
        from baseqCNV.command import run_cmd
        run_cmd("list files", "ls -l")
    """
    print("[RUN] COMMAND: {}".format(cmd))
    try:
        call(cmd, shell=True)
        print("[INFO] {} complete.".format(name, cmd))
    except:
        sys.exit("[ERROR] {} exit with error.".format(name))