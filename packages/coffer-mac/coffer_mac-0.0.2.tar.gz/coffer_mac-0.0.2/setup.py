#!/usr/bin/env python

import coffer_mac
from setuptools import setup


setup(
    name='coffer_mac',
    packages=['coffer_mac'],
    version=coffer_mac.__version__,
    description='Tiny Python API for performing MAC address lookups using Coffer.',
    license='MIT',
    url='https://github.com/vesche/coffer_mac',
    author=coffer_mac.__author__,
    author_email=coffer_mac.__email__,
    install_requires=['beautifulsoup4', 'requests'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Security"
    ]
)