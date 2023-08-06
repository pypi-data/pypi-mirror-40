# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['simple_project']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'simple-project',
    'version': '1.2.3',
    'description': 'Some description.',
    'long_description': 'My Package\n==========\n',
    'author': 'Sébastien Eustace',
    'author_email': 'sebastien@eustace.io',
    'url': 'https://poetry.eustace.io',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
