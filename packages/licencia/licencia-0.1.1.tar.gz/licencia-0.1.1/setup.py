# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['licencia']

package_data = \
{'': ['*']}

install_requires = \
['beautifultable>=0.6.0,<0.7.0',
 'cleo>=0.7.2,<0.8.0',
 'importlib-metadata>=0.8.0,<0.9.0',
 'tomlkit>=0.5.3,<0.6.0']

entry_points = \
{'console_scripts': ['licencia = licencia.app:application.run']}

setup_kwargs = {
    'name': 'licencia',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'kk6',
    'author_email': 'hiro.ashiya@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
