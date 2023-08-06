#!/usr/bin/env python
# (C) Copyright NuoDB, Inc. 2018  All Rights Reserved.

"""
Setup script for pynuoadmin package. This can be installed using pip as
follows:

    pip install "$NUODB_HOME/drivers/pynuoadmin"

To install with autocomplete dependency:

    pip install "$NUODB_HOME/drivers/pynuoadmin[completion]"

"""

from setuptools import setup

metadata = dict(
    name='pynuoadmin',
    version='1.0.0',
    url='https://nuodb.com',
    author='NuoDB',
    author_email='info@nuodb.com',
    license='BSD License',
    description='Python management interface for NuoDB',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
    ],
    py_modules=['nuodb_cli', 'nuodb_mgmt'],
    install_requires=['requests>=2.8.1,<3.0.0', 'pynuodb>=2.3.3'],
    extras_require=dict(completion='argcomplete>=1.9.0,<2.0.0'),
)

if __name__ == '__main__':
    setup(**metadata)
