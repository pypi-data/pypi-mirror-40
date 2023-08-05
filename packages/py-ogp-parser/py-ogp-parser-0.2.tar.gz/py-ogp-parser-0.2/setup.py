from setuptools import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
import sys

requires = [
    "requests>=2.14.2",
    "beautifulsoup4>=4.6.0"
]


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name='py-ogp-parser',
    version='0.2',
    description='Opengraph Protocol Parser',
    url='https://github.com/ukyoda/py-ogp-parser',
    author='ukyoda',
    author_email='black12172001@hotmail.co.jp',
    license='MIT',
    keywords='opengraph beautifulsoup4 requests scraping',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)
