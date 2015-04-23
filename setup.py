#!/usr/bin/env python

from setuptools import setup

setup(
    name='ErikTools<rename this to your own project name>',
    version='0.1.0',
    summary='My useful libraries and scripts for simulated '
            'astronomical data',
    py_modules=['simcluster'],
    entry_points={
        'console_scripts': ['simcluster=simcluster:main']
    }
)
