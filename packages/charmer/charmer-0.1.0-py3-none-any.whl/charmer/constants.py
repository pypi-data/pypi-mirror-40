import os


if os.name == "nt":
    PYTHON_EXC = "python"
    PIP_EXC = "pip"
    ENV_USER = "USERNAME"
    VENV_PATH_SUFFIX_PIP = "Scripts/pip"
    VENV_PATH_SUFFIX_PYTHON = "Scripts/python"
    OS_IS_WINDOWS = True
else:
    PYTHON_EXC = "python3"
    PIP_EXC = "pip3"
    ENV_USER = "USER"
    VENV_PATH_SUFFIX_PIP = "bin/pip3"
    VENV_PATH_SUFFIX_PYTHON = "bin/python3"
    OS_IS_WINDOWS = False
VENV_NAME = "virtual_env"
