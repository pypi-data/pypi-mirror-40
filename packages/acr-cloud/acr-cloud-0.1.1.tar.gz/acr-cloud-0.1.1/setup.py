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
    'version': '0.1.1',
    'description': 'acrcloud music recognition wrapper',
    'long_description': "# ACRCloud-py\n\nAn ACRCloud API Python client library\n\n## Installation\n```\n$ pip nstall git+https://github.com/andriyor/acrcloud-py.git#egg=acrcloud-py\n```\n\n### Requirements\n* Python 3.6 and up\n\n### Installation from source\n```\n$ git clone https://github.com/andriyor/acrcloud-py.git\n$ cd acrcloud-py\n$ python setup.py install\n```\n\n## Usage\n\nBefore you can begin identifying audio with ACRCloud's API, you need to sign up for a free trial over at \nhttps://www.acrcloud.com and create an Audio & Video recognition project. \nThis will generate a `host`, `access_key`, and `access_secret` for you to use.\n\n```\nfrom acrcloud import ACRCloud\nimport os\n\nacr = ACRCloud('eu-west-1.api.acrcloud.com', 'access_key', 'access_secret')\nmetadata = acr.identify('path-to-file.ogg')\nprint(metadata)\n```\n\n## Development\nInstall [Pipenv](https://docs.pipenv.org/)   \n```\n$ pipenv install --dev -e .\n```",
    'author': 'Andriy Orehov',
    'author_email': 'andriyorehov@gmail.com',
    'url': 'https://github.com/andriyor/acrcloud-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
