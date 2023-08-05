#MIT License
#
#Copyright (c) 2018 Dafiti OpenSource
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

# We used setup.py from the requests library as reference:
# https://github.com/requests/requests/blob/master/setup.py


from __future__ import absolute_import

import os
import re
import sys

from codecs import open

from setuptools import setup
from setuptools.command.test import test as TestCommand


here = os.path.abspath(os.path.dirname(__file__))

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

install_requires = [
    'numpy',
    'scipy',
    'statsmodels>=0.9.0',
    'matplotlib>=2.2.3',
    'jinja2>=2.10'
]

tests_require = [
    'pytest',
    'pytest-cov',
    'mock',
    'tox'
]

setup_requires = [
    'flake8',
    'isort',
    'pytest-runner'
]

extras_require = {
    'docs': [
        'ipython',
        'jupyter'
    ]
}

packages = ['causalimpact']

_version = {}
_version_path = os.path.join(here, 'causalimpact', '__version__.py')
with open(_version_path, 'r', 'utf-8') as f:
    exec(f.read(), _version)

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()


class PyTest(TestCommand):

    user_options = [
        ('coverage=', None, 'Runs coverage report.'),
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []
        self.coverage = False

    def finalize_options(self):
        TestCommand.finalize_options(self)

        if self.coverage:
            self.pytest_args.extend(['--cov-config', '.coveragerc'])
            self.pytest_args.extend([
                '--cov', 'causalimpact', '--cov-report', 'term-missing'])

        self.pytest_args.extend(['-p', 'no:warnings'])

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='pycausalimpact',
    version=_version['__version__'],
    author='Willian Fuks',
    author_email='willian.fuks@gmail.com',
    url='https://github.com/dafiti/causalimpact',
    description= "Python version of Google's Causal Impact model",
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=packages,
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires,
    extras_require=extras_require,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering',
    ],
    cmdclass={'test': PyTest},
    test_suite='tests'
)
