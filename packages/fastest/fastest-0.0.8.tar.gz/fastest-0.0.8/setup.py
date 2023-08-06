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
    'version': '0.0.8',
    'description': 'Automate tests via docstrings and more',
    'long_description': '## Fastest\nCreates unit tests from examples in the docstring and more\n\n\n### Install\n\n```\n$ pip install fastest\n```\n\n### Usage\n```\n$ python main.py --path=$(pwd) --source=<source>\n```\nwhere `path` is the the project root, and [`source`](https://coverage.readthedocs.io/en/coverage-4.3.4/source.html#source) \nis same as the value passed to the command `coverage run -m unittest --source=$source test`\n\n\n### Introduction\nThings that happen when you run `python main.py --path=$(pwd) --source=<source>` in your\npython project:\n\n1. Checks for a `test` file at the project root, it creates if it doesn\'t find one.\n2. Watches `.py` files for changes.\n3. Creates unittests if a function has examples in its docstrings like so:\n\n```python\n# .\n# ├──module_a\n# ├──module_b\n#    └── utils.py\n#\ndef add(x, y):\n    """\n    example: add(3, 4) -> 7 #\n    """\n    return x + y\n```\n\nThis will create a unittest in the `test` directory, `assertEqual(add(3, 4), 7)`\nwithin `Class test_<file>_<function>(self)` \n(for the given directory, tree: `Class test_utils_add(self)`)\n\n4. Runs all tests that are created.\n5. Creates a coverage report (in html format).\n6. Print the link to the coverage reports\' index.html.\n\n\n\n',
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
