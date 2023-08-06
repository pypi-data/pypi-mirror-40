from charmer import cmd, setup_handler


def run_tests(extra_args):
    out, err, exit_code = cmd.exec_python(
        "-m", "unittest", "discover", "tests", *extra_args
    )
    return exit_code


def run_lint(extra_args):
    proj_name = setup_handler.read().name
    out, _, exit_code = cmd.exec_python("-m", "pylint", proj_name, *extra_args)
    return exit_code


def build_wheel(extra_args):
    # cmd.exec_python("setup.py", "sdist")
    out, _, exit_code = cmd.exec_python("setup.py", "bdist_wheel", *extra_args)
    return exit_code


def start_project(extra_args):
    proj_name = setup_handler.read().name
    out, _, exit_code = cmd.exec_python("-m", proj_name, *extra_args)
    return exit_code
