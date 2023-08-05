# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['confedit']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'pick>=0.6.4,<0.7.0']

entry_points = \
{'console_scripts': ['conf = conf:conf']}

setup_kwargs = {
    'name': 'confedit',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Dominic Looser',
    'author_email': 'dominic.looser@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
