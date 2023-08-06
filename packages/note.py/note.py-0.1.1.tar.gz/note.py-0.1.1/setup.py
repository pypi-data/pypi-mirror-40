# coding=utf-8

from setuptools import setup, find_packages

NAME = "note.py"
VERSION = "0.1.1"
URL = "https://github.com/flyingpot/note.py"
AUTHOR = "flyingpot"
AUTHOR_EMAIL = "fanjingbo1@gmail.com"
LICENSE = "MIT"
MODULES = ["note"]
REQUIRES = ["Click", "pyobjc-framework-Cocoa", "Pyyaml"]
DESC = "TAKE NOTES IN COMMAND LINE"

setup(
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    name=NAME,
    version=VERSION,
    license=LICENSE,
    install_requires=REQUIRES,
    packages=find_packages(),
    py_modules = MODULES,
    description=DESC,
    entry_points={"console_scripts": ["note=note:cli"]},
)
