# -*- coding=utf-8 -*-

from setuptools import setup, find_packages
from os import path
from io import open
import re

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'iterage/__init__.py'), encoding='utf-8') as f:
    version = re.search(r'__version__\s*=\s*"([^"]+)"\n', f.read()).group(1)

setup(
    name='iterage',
    version=version,
    description='Yet another iterator utils lib',
    long_description=long_description,
    long_description_content_type='text/markdown; charset=UTF-8',
    url='https://github.com/R1tschY/iterage',
    author='Richard Liebscher',
    author_email='r1tschy@posteo.de',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    py_modules=['iterage'],

    setup_requires=["pytest-runner"],
    tests_require=["pytest"],

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    #extras_require={  # Optional
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    #},

    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    project_urls={
        'Bug Reports': 'https://github.com/R1tschY/iterage/issues',
        'Source': 'https://github.com/R1tschY/iterage',
    },
)

