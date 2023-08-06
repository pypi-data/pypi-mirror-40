# Copyright (C) 2019 Max Steinberg

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paladin-utils",
    version="0.0.1",
    author="Max Steinberg",
    author_email="nooneishere@supachat.net",
    description="A utility collection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/MAX1234/paladin-utils/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)