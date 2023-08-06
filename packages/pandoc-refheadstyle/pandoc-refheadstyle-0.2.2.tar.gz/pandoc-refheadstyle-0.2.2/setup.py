#!/usr/bin/python
# Copyright 2016, 2019 Odin Kroeger
#
# This programme is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This programme is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Setup for the *pandoc-refheadstyle* package."""

from os import path
from setuptools import setup



# Functions
# =========

def readme(readme_fname="README.rst"):
    """Returns the contents of README.rst.

    :param str readme_fname: Path to README.rst.
    :returns: Contents of *readme_fname*.
    :rtype: str
    """
    readme_path = path.join(path.dirname(__file__), readme_fname)
    with open(readme_path) as readme_handle:
        return readme_handle.read()


# Metadata
# ========

# Name of this package.
NAME = 'pandoc-refheadstyle'

# Version of this package.
VERSION = '0.2.2'

# All other metadata.
# pylint: disable=C0330
METADATA = {
    'name':             NAME,
    'version':          VERSION,
    'description':      ('Pandoc filter that sets a a custom style '
                         'for the reference section header.'),
    'long_description': readme(),
    'keywords':         'pandoc reference section header',
    'classifiers':      ['Development Status :: 4 - Beta',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 2.7',
                 'Environment :: Console',
                 'Operating System :: OS Independent',
                 'Topic :: Text Processing :: Filters'
    ],
    'url':             'https://github.com/odkr/pandoc-refheadstyle/',
    'project_urls':     {
                'Source': 'https://github.com/odkr/pandoc-refheadstyle/',
                'Tracker': 'https://github.com/odkr/pandoc-refheadstyle/issues'
    },
    'author':           'Odin Kroeger',
    'author_email':     'tqxwcv@maskr.me',
    'license':          'MIT',
    'python_requires':  '>=2.7',
    'packages':         ['pandoc_refheadstyle'],
    'install_requires': ['panflute'],
    'zip_safe':         True
}


# Boilerplate
# ===========

if __name__ == '__main__':
    setup(**METADATA)
