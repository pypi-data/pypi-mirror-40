#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

__requirements__ = ['asynctest', 'coverage']
__test_requirements__ = ['asynctest', 'coverage']
__version__ = "0.1.1"

# Decent reference:
# https://gemfury.com/stevenferreira/python:sample/-/content/setup.py?gclid=Cj0KCQiApILhBRD1ARIsAOXWTztNWw_wmu2xA4Ka0yn-EjwbS99NZBI19Pjozfw7qAjVGSXDTY6grkkaAm1WEALw_wcB
setup(
    name="recoil",
    version=__version__,
    description="Simple Spring-inspired IoC framework for Python.",
    long_description="Component autowiring and other IoC goodies",
    author="flitt3r",
    license="MIT",
    url="https://gitlab.com/flitt3r/recoil",

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Development Status :: 1 - Planning
        # Development Status :: 2 - Pre-Alpha
        # Development Status :: 3 - Alpha
        # Development Status :: 4 - Beta
        # Development Status :: 5 - Production/Stable
        # Development Status :: 6 - Mature
        # Development Status :: 7 - Inactive
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='python ioc spring inversion of control',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=__requirements__,
    extras_require={'test': ['coverage', 'asynctest']}
)
