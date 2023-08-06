import setuptools
from pathlib import Path

setuptools.setup(
    name="tempdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["test", "data"])
)
# Create the source & distribution package
# 1. python3 setup.py sdist bdist_wheel
