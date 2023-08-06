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

entry_points = \
{'console_scripts': ['fastest = fastest.__main__:main']}

setup_kwargs = {
    'name': 'fastest',
    'version': '0.0.6',
    'description': 'Automate tests via docstrings and more',
    'long_description': '## Fastest\nCreates unit tests from examples in the docstring and more\n\n\n### Install\n\n```\n$ pip install fastest\n```\n\n### Usage\n```\n$ python main.py --path=$(pwd)\n```\n',
    'author': 'AmreshVenugopal',
    'author_email': 'amresh.venugopal@gmail.com',
    'url': 'https://github.com/AmreshVenugopal/fastest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
