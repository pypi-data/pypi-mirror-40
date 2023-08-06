#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="scutter",
    version='0.0.0',
    url="https://github.com/awesometoolbox/scutter",

    package_dir={
        '': 'src'
    },

    packages=[
        "scutter",
    ],

    include_package_data=True,

    install_requires=[
        "requests-html",
        "w3lib",
        "dragnet",
        "related",
    ],

    setup_requires=[
        'pytest-runner',
    ],

    tests_require=[],
    license="MIT",
    keywords='scutter',
    description="scutter",
)
