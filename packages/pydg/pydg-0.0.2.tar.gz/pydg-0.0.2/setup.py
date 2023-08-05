# coding: utf-8


import os
from setuptools import setup

import pydg


this_dir = os.path.dirname(os.path.abspath(__file__))

keywords = []

classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Development Status :: 4 - Beta",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: BSD License",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Information Technology",
]

# read the readme file
with open(os.path.join(this_dir, "README.md"), "r") as f:
    long_description = f.read()

# load installation requirements
with open(os.path.join(this_dir, "requirements.txt"), "r") as f:
    install_requires = [line.strip() for line in f.readlines() if line.strip()]

setup(
    name=pydg.__name__,
    version=pydg.__version__,
    author=pydg.__author__,
    author_email=pydg.__email__,
    description=pydg.__doc__.strip().split("\n")[0].strip(),
    license=pydg.__license__,
    url=pydg.__contact__,
    keywords=keywords,
    classifiers=classifiers,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    python_requires=">=2.7",
    zip_safe=False,
    py_modules=[pydg.__name__],
    data_files=[(".", ["LICENSE", "requirements.txt", "README.md"])],
)
