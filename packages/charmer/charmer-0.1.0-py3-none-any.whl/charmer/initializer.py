import os
import sys
from charmer import cmd, questionnaire
from charmer.constants import VENV_NAME
from charmer.inputs import PREFERENCE_INPUTS
from charmer.templates import (
    get_main,
    get_init,
    get_readme,
    get_setup,
    get_context,
    get_main_test_suite,
    get_conf,
    get_dev_requirements,
)


def start(args):
    preferences_by_name = questionnaire.get_preferences(PREFERENCE_INPUTS, args)
    verbose = args.verbose
    name = preferences_by_name["name"].value
    output_dir = preferences_by_name["dir"].value
    description = preferences_by_name["description"].value
    version = preferences_by_name["version"].value
    author = preferences_by_name["author"].value
    runnable = preferences_by_name["runnable"].value
    create_venv = preferences_by_name["create venv"].value
    use_conf = preferences_by_name["use conf"].value
    use_pylint = preferences_by_name["use pylint"].value

    if os.listdir(output_dir):
        print(
            "Could not initialize project. The output directory ('%s') is not empty."
            % output_dir
        )
        return 1

    start_str = "Initializing project '%s'" % name
    print("")
    print(start_str)
    print(len(start_str) * "-")

    main_package = os.path.join(output_dir, name)
    tests_package = os.path.join(output_dir, "tests")

    sys.stdout.write("> Creating main package... ")
    os.makedirs(main_package, exist_ok=True)
    _create_file("__init__.py", get_init(), main_package)
    print("done")

    sys.stdout.write("> Creating test package... ")
    os.makedirs(tests_package, exist_ok=True)
    _create_file("__init__.py", get_init(), tests_package)
    _create_file("context.py", get_context(), tests_package)
    _create_file("test_main.py", get_main_test_suite(name, runnable), tests_package)
    print("done")

    sys.stdout.write("> Creating README.rst... ")
    _create_file(
        "README.rst", get_readme(name, description, runnable, use_conf), output_dir
    )
    print("done")

    sys.stdout.write("> Creating setup.py... ")
    _create_file(
        "setup.py",
        get_setup(name, version, author, description, runnable, use_conf),
        output_dir,
    )
    print("done")

    sys.stdout.write("> Creating requirements.txt... ")
    _create_file("requirements.txt", get_dev_requirements(use_pylint), output_dir)
    print("done")

    sys.stdout.write("> Creating entrypoint... ")
    _create_file("__main__.py", get_main(name, use_conf), main_package)
    print("done")

    if use_conf:
        sys.stdout.write("> Creating default configuration... ")
        _create_file("config-default.yml", get_conf(), output_dir)
        print("done")

    if create_venv:
        sys.stdout.write("> Creating virtual environment... ")
        sys.stdout.flush()
        cmd.exec_python(
            "-m", "venv", os.path.join(output_dir, VENV_NAME), print_output=verbose
        )
        cmd.exec_python(
            "-m", "pip", "install", "--upgrade", "pip", print_output=verbose
        )
        print("done")

    sys.stdout.write("> Installing %s... " % name)
    sys.stdout.flush()
    cmd.exec_pip("install", "-e", ".", print_output=verbose)
    print("done")

    sys.stdout.write("> Installing dev dependencies... ")
    sys.stdout.flush()
    cmd.exec_pip("install", "-r", "requirements.txt", print_output=verbose)
    print("done")

    print("")
    print("Finished!")
    return 0  # TODO beter dit


def _create_file(fname, content, pname=None):
    output_path = os.path.abspath(os.path.join(pname, fname))
    with open(output_path, "w+") as f:
        f.write(content)
