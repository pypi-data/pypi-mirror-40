# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['xlsxreporter']

package_data = \
{'': ['*']}

install_requires = \
['xlsxwriter>=1.1,<2.0']

setup_kwargs = {
    'name': 'xlsxreporter',
    'version': '0.1.0',
    'description': 'A thin wrapper around xlsxwriter, to aid in generating row-by-row XLSX reports.',
    'long_description': None,
    'author': 'Jonas Myrlund',
    'author_email': 'myrlund@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
