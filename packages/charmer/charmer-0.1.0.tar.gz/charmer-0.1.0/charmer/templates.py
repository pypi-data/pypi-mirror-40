import os

from charmer.constants import VENV_PATH_SUFFIX_PYTHON

BR = "\n"


def get_init():
    return ""


def get_main(name, use_conf):
    result = ""
    result += '"""This module serves as the entry point of ' + name + '."""'
    result += BR
    if use_conf:
        result += "import logging"
        result += BR
        result += "import conf"
        result += BR
    result += BR
    result += BR
    result += "def main():"
    result += BR
    result += '    """The actual entry point."""'
    result += BR
    if use_conf:
        result += "    logger = logging.getLogger('name')"
        result += BR
        result += "    log_level = logging.getLevelName(conf.get('log_level', 'DEBUG').upper())"
        result += BR
        result += "    logger.setLevel(log_level)"
        result += BR
    result += "    raise NotImplementedError()"
    result += BR
    result += BR
    result += BR
    result += "if __name__ == '__main__':"
    result += BR
    result += "    main()"
    result += BR
    return result


def get_readme(name, description, runnable, use_conf):
    result = name + BR + len(name) * "=" + BR + BR + description + BR
    if runnable:
        if use_conf:
            result += BR
            result += "Usage"
            result += BR
            result += "'''''"
            result += BR
            result += BR
            result += "::"
            result += BR
            result += BR
            result += "    python -m "
            result += name
            result += " --config config-default.yml"
            result += BR
        else:
            result += BR
            result += "Usage"
            result += BR
            result += "'''''"
            result += BR
            result += BR
            result += "::"
            result += BR
            result += BR
            result += "    python -m "
            result += name
            result += BR
    result += BR
    result += "Testing"
    result += BR
    result += "'''''''"
    result += BR
    result += BR
    result += "::"
    result += BR
    result += BR
    result += "    python -m unittest discover tests"
    result += BR
    return result


def get_setup(name, version, author, description, runnable, use_conf):
    result = '"""This is the installation toolset for this project."""'
    result += BR
    result += "from setuptools import setup, find_packages"
    result += BR
    result += BR
    result += "with open('README.rst', 'r') as fh:"
    result += BR
    result += "    long_description = fh.read()"
    result += BR
    result += BR
    result += "setup(name='"
    result += name
    result += "',"
    result += BR
    result += "      version='"
    result += version
    result += "',"
    result += BR
    result += "      author='"
    result += author
    result += "',"
    result += BR
    result += "      description='"
    result += description
    result += "',"
    result += BR
    result += "      long_description=long_description,"
    result += BR
    result += "      packages=find_packages(exclude=('tests',))"
    if use_conf:
        result += "," + BR
        result += "      install_requires=['conf~=0.2.0']"
    if runnable:
        result += ","
        result += BR
        result += "      entry_points={"
        result += BR
        result += "          'console_scripts': ["
        result += BR
        result += "              '"
        result += name
        result += " = "
        result += name
        result += ".__main__:main'"
        result += BR
        result += "          ]"
        result += BR
        result += "      }"
    result += ")" + BR
    return result


def get_context():
    result = '"""Import this module first before importing your project stuff in the tests"""'
    result += BR
    result += "import sys"
    result += BR
    result += "import os"
    result += BR
    result += BR
    result += "dname = os.path.dirname(__file__)"
    result += BR
    result += "relpath = os.path.join(dname, '..')"
    result += BR
    result += "abspath = os.path.abspath(relpath)"
    result += BR
    result += "sys.path.insert(0, abspath)"
    result += BR
    return result


def get_main_test_suite(name, runnable):
    result = '"""Contains a test suite for basic tests."""'
    result += BR
    result += "import context"
    result += BR
    result += "import unittest"
    result += BR
    if runnable:
        result += "from " + name + ".__main__ import main" + BR
    result += BR
    result += BR
    result += "class MainTestSuite(unittest.TestCase):"
    result += BR
    result += '    """Basic test cases."""'
    result += BR
    if runnable:
        result += BR
        result += "    def test_main(self):"
        result += BR
        result += "        with self.assertRaises(NotImplementedError):"
        result += BR
        result += "            main()"
        result += BR
    result += BR
    result += BR
    result += "if __name__ == '__main__':"
    result += BR
    result += "    unittest.main()"
    result += BR
    return result


def get_conf():
    result = "log_level: INFO"
    return result


def get_dev_requirements(use_pylint):
    result = ""
    result += "wheel" + BR
    result += "setuptools" + BR
    if use_pylint:
        result += "pylint" + BR
    return result
