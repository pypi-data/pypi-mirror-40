# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="python3-SmartSchema",
    version="0.1.1",
    # version_command='git describe',
    description="Progressive update for schema",
    license="MIT",
    author="Jaiswal-ruhil",
    author_email="cschultz@example.com",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ]
)
