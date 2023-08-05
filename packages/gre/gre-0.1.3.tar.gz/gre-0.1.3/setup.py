#!/usr/bin/env python3

import pathlib
from setuptools import setup, find_packages

BASE = pathlib.Path(__file__).parent
README = (BASE / "README.md").read_text()

setup(
    name='gre',
    version='0.1.3',
    description='A handy helper to manage GRE Vocab preparation',
    author='Sayan Goswami',
    author_email='<goswami.sayan47@gmail.com>',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/Sayan98/gre',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'tinydb',
        'wiktionaryparser'
    ],
    entry_points='''
        [console_scripts]
        gre=gre.main:cli
    ''',
)
