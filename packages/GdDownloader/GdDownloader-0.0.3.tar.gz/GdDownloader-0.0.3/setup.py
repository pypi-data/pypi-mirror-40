import os
import sys
import setuptools
from setuptools.command.install import install

CURRENT_DIR = os.getcwd()
REQUIREMENTS = 'requirements.txt'
requires = [line.strip('\n') for line in open(REQUIREMENTS).readlines()]
with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = "0.0.3"

setuptools.setup(
    name="GdDownloader",
    version=VERSION,
    author='Domnan Diretnan, Mmadu Manasseh',
    author_email="diretnandomnan@gmail.com",
    description="easy wrapper for downloading google drive files using only shareable link",
    url="https://github.com/deven96/drive_downloader",
    packages=setuptools.find_packages(),
    install_requires=requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords='downloader googledrive gdrive drive',
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    package_data={
        '': ['*.*'],
    },
    include_package_data=True,
)