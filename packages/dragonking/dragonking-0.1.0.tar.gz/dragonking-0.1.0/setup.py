#from setuptools import setup

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dragonking",
    version="0.1.0",
    author="Daniel Qin, Raoul R. Wadhwa, Peter Erdi",
    author_email="k17dq01@kzoo.edu",
    description="Statistical tests for identification of dragon kings",
    url="https://github.com/dcqin17/dragonking",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
