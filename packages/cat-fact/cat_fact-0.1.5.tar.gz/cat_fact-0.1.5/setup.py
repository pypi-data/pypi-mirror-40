"""
# cat_fact
`catFact` Get random cat facts from the internet :smile:

## Installation Instructions

Create and activate virtual environment.

```bash
$ virtualenv venv
$ source ./venv/bin/activate
```
Now run `python setup.py install`, this will install `catFact` command into the virtual environment

If running `catFact` says command not found, deactivate and activate the virtual environment. That should fix it.

## Example

```bash
$ catFact
Julius Ceasar, Henri II, Charles XI, and Napoleon were all afraid of cats.
```

"""

import sys
import re
import os.path

from setuptools import setup, find_packages


def get_version():
    """Returns the package version taken from version.py
    """
    root = os.path.dirname(__file__)
    version_path = os.path.join(root, "cat_fact/__init__.py")
    text = open(version_path).read()
    rx = re.compile("^__version__ = '(.*)'", re.M)
    m = rx.search(text)
    version = m.group(1)
    return version


install_requires = [
    "click>=6.7",
    "requests>=2.21"
]


setup(
    name="cat_fact",
    version=get_version(),
    author="Shaik Sohail Yunus",
    author_email="sohail.yunusha1@gmail.com",
    maintainer="Shaik Sohail Yunus",
    maintainer_email="sohail.yunusha1@gmail.com",
    description="Get random cat facts fromt the internet " + u"\U0001F638",
    long_description=__doc__,
    install_requires=install_requires,
    packages=find_packages(),
    url="https://github.com/sohail535/cat_fact",
    entry_points="""
        [console_scripts]
        catFact = cat_fact.cli:cli
    """
)

