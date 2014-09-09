#!/usr/bin/env python

from __future__ import with_statement

import re
import sys

try:
    import setuptools as impl
except ImportError:
    import distutils.core as impl

with open('README.rst') as ld_file:
    long_description = ld_file.read()

with open('fuzzify.py') as fuzzify_source:
    source = fuzzify_source.read()
    pattern = re.compile(r'''__version__ = ['"](?P<version>[\d.]+)['"]''')
    version = pattern.search(source).group('version')

dependencies = ['path.py']

setup_params = dict(
    name="fuzzify",
    version=version,
    description="rSync fuzzy file pool creation",
    long_description=long_description,
    author="Shane R. Spencer",
    author_email="shane@bogomip.com",
    url="https://github.com/whardier/fuzzify",
    license="MIT",
    py_modules=['fuzzify'],
    #test_suite='tests',
    install_requires=dependencies,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: System',
        'Topic :: System :: Archiving',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: System :: Filesystems',
    ],
    entry_points={
        'console_scripts': [
            'fuzzify = fuzzify:main',
        ],
    }
)

if __name__ == '__main__':
    impl.setup(**setup_params)
