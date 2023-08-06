#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name="AutomatedDrinkDispensingSystem",
    version="0.0a2",
    author="Chris Blanks",
    author_email="christopherablanks@gmail.com",
    url="https://github.com/ChrisBlanks/AutomatedDrinkDispensingSystem",
    packages=setuptools.find_packages(),
    license="LICENSE.txt",
    long_description=open("README.txt").read(),
    install_requires=[
        "setuptools >= 18.5", "cryptography >= 1.7.1",

    ],
)
