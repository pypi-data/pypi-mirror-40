import os
from charmer.questionnaire import PreferenceInput


if os.name == "nt":
    _python_exc = "python"
    ENV_USER = "USERNAME"
else:
    _python_exc = "python3"
    ENV_USER = "USER"


PREFERENCE_INPUTS = [
    PreferenceInput(
        "name",
        "Project name",
        default_value=os.getcwd().split(os.sep)[-1].replace("-", "_"),
        regex="[a-zA-Z_]\w*",
        requirements="A project name must be a word; it must start with a "
        "letter or underscore and may contain only letters, "
        "underscores and numbers in the remainder.",
    ),
    PreferenceInput(
        "description", "Description", default_value="My awesome Python project"
    ),
    PreferenceInput(
        "version",
        "Initial version",
        default_value="0.1.0",
        regex="[0-9]\.[0-9]\.[0-9]",
        requirements="A version must have the form: x.y.z where x, y and z are all whole numbers.",
    ),
    PreferenceInput(
        "author", "Author", default_value=os.getenv(ENV_USER), regex="([a-zA-Z_]\w*)?"
    ),
    PreferenceInput("dir", "Output directory", default_value="./"),
    PreferenceInput(
        "runnable", "Is the application runnable?", default_value="yes", yes_or_no=True
    ),
    PreferenceInput(
        "create venv",
        "Create virtual environment?",
        default_value="yes",
        yes_or_no=True,
    ),
    PreferenceInput("use conf", "Use conf?", default_value="yes", yes_or_no=True),
    PreferenceInput("use pylint", "Use Pylint?", default_value="yes", yes_or_no=True),
]
