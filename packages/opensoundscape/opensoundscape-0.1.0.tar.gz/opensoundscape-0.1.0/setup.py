# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['opensoundscape']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0']

entry_points = \
{'console_scripts': ['opensoundscape = opensoundscape.console:run']}

setup_kwargs = {
    'name': 'opensoundscape',
    'version': '0.1.0',
    'description': 'Open source, scalable acoustic classification for ecology and conservation',
    'long_description': None,
    'author': 'Barry Moore',
    'author_email': 'moore0557@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
