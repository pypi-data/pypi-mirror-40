# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pypath_setup']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pypath-setup = pypath_setup:main']}

setup_kwargs = {
    'name': 'pypath-setup',
    'version': '0.1.4',
    'description': 'Start processes by setting PYTHONPATH to point to some virtualenv',
    'long_description': None,
    'author': 'Paul Maréchal',
    'author_email': 'marechap.info@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
