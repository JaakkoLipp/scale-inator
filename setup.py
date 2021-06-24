#!/usr/bin/env python3

from setuptools import setup

setup(
    name="scale_inator",
    packages=['scale_inator'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'scale_inator=scale_inator.main:main',
        ],
    },
)
