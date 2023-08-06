# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['flomutils']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.1.3,<0.2.0',
 'flom>=0.3.1,<0.4.0',
 'matplotlib>=3.0,<4.0',
 'numpy>=1.16,<2.0']

entry_points = \
{'console_scripts': ['flomutils = flomutils.__main__:main']}

setup_kwargs = {
    'name': 'flomutils',
    'version': '0.1.0',
    'description': 'plot, analyze, and modify your flom motion',
    'long_description': None,
    'author': 'coord.e',
    'author_email': 'me@coord-e.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
