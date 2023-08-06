import os
from subprocess import Popen, PIPE, check_output
from charmer.constants import (
    OS_IS_WINDOWS,
    VENV_NAME,
    VENV_PATH_SUFFIX_PIP,
    VENV_PATH_SUFFIX_PYTHON,
    PIP_EXC,
    PYTHON_EXC,
)


def exec_python(*args, working_dir=".", print_output=True):
    python_cmd = PYTHON_EXC
    if VENV_NAME in os.listdir(working_dir):
        python_cmd = os.path.abspath(os.path.join(VENV_NAME, VENV_PATH_SUFFIX_PYTHON))
    return exec(python_cmd, *args, print_output=print_output)


def exec_pip(*args, working_dir=".", print_output=True):
    pip_cmd = PIP_EXC
    if VENV_NAME in os.listdir(working_dir):
        pip_cmd = os.path.abspath(os.path.join(VENV_NAME, VENV_PATH_SUFFIX_PIP))
    return exec(pip_cmd, *args, print_output=print_output)


def exec(*commands, print_output=True):
    with Popen(commands, shell=OS_IS_WINDOWS, stdout=PIPE, stderr=PIPE) as proc:
        outb, errb = proc.communicate()
        out = outb.decode("utf8")
        err = errb.decode("utf8")
        if print_output:
            if out:
                print(out)
            if err:
                print(err)
        if proc.returncode:
            msg = "Command failed: %s" % " ".join(commands)
            if out:
                msg += "\n" + out
            if err:
                msg += "\n" + err
            raise Exception(msg)
        return out, err, proc.returncode
