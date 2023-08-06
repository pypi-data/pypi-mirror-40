# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fastest',
 'fastest.bodies',
 'fastest.case_labyrinth',
 'fastest.case_labyrinth.type_check_detect',
 'fastest.code_assets',
 'fastest.compiler',
 'fastest.io',
 'fastest.type']

package_data = \
{'': ['*']}

install_requires = \
['watchdog>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'fastest',
    'version': '0.0.4',
    'description': 'Automate tests via docstrings and more',
    'long_description': None,
    'author': 'AmreshVenugopal',
    'author_email': 'amresh.venugopal@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
