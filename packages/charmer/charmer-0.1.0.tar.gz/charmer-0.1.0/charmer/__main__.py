import argparse
import sys
from collections import OrderedDict
from charmer import initializer, runner


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action", help="Initialize a new project", nargs="*", default="init"
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Say 'yes' to all prompts during initialization",
    )
    parser.add_argument(
        "-vb",
        "--verbose",
        action="store_true",
        help="Show output of sub processes during initialization",
    )
    args = parser.parse_known_args()[0]
    actions = OrderedDict(
        [
            ("test", runner.run_tests),
            ("lint", runner.run_lint),
            ("start", runner.start_project),
            ("wheel", runner.build_wheel),
        ]
    )
    exit_code = 0

    args.action = sys.argv or "init"

    if "init" in args.action:
        initializer.start(args)
    for action_name in actions:
        if action_name in args.action:
            extra_args = sys.argv[sys.argv.index(action_name) + 1 :]
            if "_" in extra_args:
                extra_args = extra_args[: extra_args.index("_")]
            exit_code |= actions[action_name](extra_args)
    exit(exit_code)


if __name__ == "__main__":
    main()

# TODO add command: install --dev
# TODO add command: clean
# TODO add command: upload
