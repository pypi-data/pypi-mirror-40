# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['file_replicator']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'inotify>=0.2.10,<0.3.0']

entry_points = \
{'console_scripts': ['file-replicator = file_replicator.cli:main']}

setup_kwargs = {
    'name': 'file-replicator',
    'version': '0.1.0',
    'description': 'Replicate files to another computer for remote development',
    'long_description': None,
    'author': 'Timothy Corbett-Clark',
    'author_email': 'timothy.corbettclark@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
