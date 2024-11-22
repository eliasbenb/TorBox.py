__author__ = "Elias Benbourenane <eliasbenbourenane@gmail.com>"
__liicense__ = "MIT"
from torbox import __version__  # noqa: I001

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="torbox",
    version=__version__,
    author="Elias Benbourenane",
    author_email="eliasbenbourenane@gmail.com",
    description="Python wrapper for the TorBox API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eliasbenb/TorBox.py",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
)
