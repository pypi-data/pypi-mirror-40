#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

import pywekaclassifiers

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

def get_reqs(*fns):
    lst = []
    for fn in fns:
        for package in open(os.path.join(CURRENT_DIR, fn)).readlines():
            package = package.strip()
            if not package:
                continue
            lst.append(package.strip())
    return lst

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pywekaclassifiers',
    version=pywekaclassifiers.__version__,
    description='A Python wrapper for the Weka data mining library.',
    author='Picatureanu Nicusor',
    author_email='nicolaepicatureanu@gmail.com',
    url='https://github.com/Nicusor97/PyWekaClassifiers.git',
    license='MIT License',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        'pywekaclassifiers': [
            'fixtures/*'
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
    ],
    platforms=['OS Independent'],
    install_requires=get_reqs('pip-requirements.txt'),
)
