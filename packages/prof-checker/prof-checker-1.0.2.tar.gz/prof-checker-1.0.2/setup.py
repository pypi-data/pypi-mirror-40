import ast
import re
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


with open("prof_checker.py", "r") as fh:
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    match = _version_re.search(fh.read())
    version = match.group("version") if match is not None else '"unknown"'
    version = str(ast.literal_eval(version))


setup(
    name="prof-checker",
    version=version,
    author="Tornike Gogniashvili",
    author_email="t.gogniashvili@gmail.com",
    description="Wrapper for profanity checker that can work on python services/scripts, similar to linters (e.g. pylint)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ozychhi/prof-checker",
    packages=find_packages(),
    install_requires=["profanity-check", "click>=6.5"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "dev": ["pytest", "tox", "black"],
    },
    py_modules=["prof_checker"],
    entry_points={"console_scripts": ["prof_checker=prof_checker:main"]},
)
