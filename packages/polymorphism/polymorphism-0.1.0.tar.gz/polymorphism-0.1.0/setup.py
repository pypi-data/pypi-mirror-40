# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['polymorphism']

package_data = \
{'': ['*']}

install_requires = \
['pytest-cov>=2.6,<3.0']

setup_kwargs = {
    'name': 'polymorphism',
    'version': '0.1.0',
    'description': 'Ad hoc polymorphism for Python classes!',
    'long_description': None,
    'author': 'asduj',
    'author_email': 'asduj@ya.ru',
    'url': 'https://github.com/asduj/polymorphism',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4',
}


setup(**setup_kwargs)
