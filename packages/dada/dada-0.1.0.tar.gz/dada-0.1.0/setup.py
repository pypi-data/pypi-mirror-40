# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dada', 'dada.scripts']

package_data = \
{'': ['*'], 'dada': ['config/*']}

install_requires = \
['click>=7.0,<8.0', 'pick>=0.6.4,<0.7.0', 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['dada = dada.scripts.dada:cli']}

setup_kwargs = {
    'name': 'dada',
    'version': '0.1.0',
    'description': 'Dada – a CLI project manager',
    'long_description': "# Dada\n\nDada is a project manager for web projects and documents.\n\nDada is pre-alpha! Probably won't work yet.",
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
