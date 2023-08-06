import os
import re


class Project:
    def __init__(self, name):
        self.name = name


def read(directory="."):
    setup_path = os.path.abspath(os.path.join(directory, "setup.py"))
    with open(setup_path, "r") as setup_file:
        raw_content = setup_file.read()
        raw_setup_call = _get_setup_call(raw_content)
        name = _get_key_("name", raw_setup_call)
    return Project(name)


def _get_key_(key, raw_setup_call):
    match = re.search(r"%s\s*=\s*[\'\"](.+?)[\'\"]" % key, raw_setup_call, re.DOTALL)
    return match.group(1)


def _get_setup_call(raw_content):
    match = re.search(r"setup\(.*\)", raw_content, re.DOTALL)
    return match.group(0)
