#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='FControllerPY',
    version='0.0.1',
    description='Container and Front Controller for modules or controllers.',
    author='Unay Santisteban',
    author_email='usantisteban@othercode.es',
    maintainer='Unay Santisteban',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/othercodes/fcontroller-py',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
