#!/usr/bin/env python

from setuptools import setup, find_packages
from distutils.util import convert_path
import codecs

# Load version information
main_ns = {}
ver_path = convert_path('xmlrunner/version.py')
with codecs.open(ver_path, 'rb', 'utf8') as ver_file:
    exec(ver_file.read(), main_ns)

install_requires = ['six>=1.4.0']

# this is for sdist to work.
import sys
if sys.version_info < (2, 7):
    # python 2.6 no longer supported, use last 1.x release instead.
    raise RuntimeError('This version requires Python 2.7+')  # pragma: no cover

setup(
    name = 'unittest-xml-reporting-iron',
    version = main_ns['__version__'],
    author = 'Jani Mikkonen',
    author_email = 'jani.mikkonen@gmail.com',
    description = 'unittest-based test runner with Ant/JUnit like XML reporting.',
    license = 'BSD',
    platforms = ['Any'],
    keywords = [
        'pyunit', 'unittest', 'junit xml', 'report', 'testrunner', 'xmlrunner'
    ],
    url = 'https://github.com/rasjani/unittest-xml-reporting/tree/fix-182',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing'
    ],
    packages = ['xmlrunner', 'xmlrunner.extra'],
    zip_safe = False,
    include_package_data = True,
    install_requires = install_requires,
    test_suite = 'tests'
)
