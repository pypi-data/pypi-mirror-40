#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name='securenotes-client',
    version='0.2.1',
    author="Andreas Hasenkopf",
    author_email="andreas@hasenkopf.xyz",
    description="Command line client for SecureNotes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crazyscientist/secure-notes-client",
    packages=find_packages(),
    python_requires=">=3.5",
    scripts=["securenotes_client/securenotes.py",],
    install_requires=['requests', 'pycryptodomex', 'mdv'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/crazyscientist/secure-notes-client/issues",
        "Documentation": "https://readthedocs.org/projects/secure-notes-client/",
        "Source Code": "https://github.com/crazyscientist/secure-notes-client"
    }
)
