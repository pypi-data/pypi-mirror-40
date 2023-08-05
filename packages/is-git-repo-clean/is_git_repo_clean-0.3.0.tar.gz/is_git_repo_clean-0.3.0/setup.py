# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['is_git_repo_clean']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'is-git-repo-clean',
    'version': '0.3.0',
    'description': 'A simple function to test whether your git repo is clean',
    'long_description': None,
    'author': 'Philip Olson',
    'author_email': 'philip.olson@pm.me',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
