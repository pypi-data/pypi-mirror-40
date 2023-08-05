# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['acr_cloud']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'acr-cloud',
    'version': '0.1.0',
    'description': 'acrcloud music recognition wrapper',
    'long_description': None,
    'author': 'Andriy Orehov',
    'author_email': 'andriyorehov@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
