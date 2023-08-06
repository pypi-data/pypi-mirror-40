#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from shutil import rmtree
from glob import glob
from codecs import open

from setuptools import setup, Command
from setuptools.command.test import test as test_command

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

here = os.path.abspath(os.path.dirname(__file__))

packages = ['visibudget']


class PyTest(test_command):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def __init__(self, dist):
        super().__init__(dist)
        self.test_args = []
        self.test_suite = True
        self.pytest_args = []

    def initialize_options(self):
        test_command.initialize_options(self)
        try:
            from multiprocessing import cpu_count
            self.pytest_args = ['-n', str(cpu_count()), '--boxed']
        except (ImportError, NotImplementedError):
            self.pytest_args = ['-n', '1', '--boxed']

    def finalize_options(self):
        test_command.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


class PublishCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


# Load the package's Pipfile to get dependency information
pipfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pipfile['packages'], r=False)
test_requirements = convert_deps_to_pip(pipfile['dev-packages'], r=False)

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, packages[0], '__version__.py')) as f:
    exec(f.read(), about)

# Read the package's readme and history as strings
with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

# Find all data files for the package
data_files = []
for root, dirs, files in os.walk('data'):
    data_files.append((os.path.relpath(root, 'data'),
                       [os.path.join(root, f) for f in files]))

# Find all script files for the package
scripts = []
for fname in glob('bin/*'):
    scripts.append(fname)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme + '\n\n' + history,
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],
    url=about['__url__'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Office/Business',
    ],

    packages=packages,
    scripts=scripts,
    data_files=data_files,
    package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={'visibudget': 'visibudget'},
    include_package_data=True,
    install_requires=requirements,
    tests_require=test_requirements,
    zip_safe=False,

    cmdclass={'test': PyTest, 'publish': PublishCommand},
)
