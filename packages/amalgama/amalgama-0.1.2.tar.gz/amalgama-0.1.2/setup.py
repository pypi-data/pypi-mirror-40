# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['amalgama']

package_data = \
{'': ['*']}

install_requires = \
['pyquery>=1.4,<2.0']

setup_kwargs = {
    'name': 'amalgama',
    'version': '0.1.2',
    'description': 'amalgama scraper',
    'long_description': "# Amalgama-pq \n[![image](https://img.shields.io/pypi/v/amalgama.svg)](https://pypi.org/project/amalgama/)\n[![image](https://img.shields.io/pypi/l/amalgama.svg)](https://pypi.org/project/amalgama/)\n[![image](https://img.shields.io/pypi/pyversions/amalgama.svg)](https://pypi.org/project/amalgama/)\n[![Build Status](https://travis-ci.org/andriyor/amalgama-pq.svg?branch=master)](https://travis-ci.org/andriyor/amalgama-pq)\n[![codecov](https://codecov.io/gh/andriyor/amalgama-pq/branch/master/graph/badge.svg)](https://codecov.io/gh/andriyor/amalgama-pq)\n\nAmalgama lyrics scraping\n\n## Installation\n```\n$ pip install git+https://github.com/andriyor/amalgama-pq.git#egg=amalgama-pq\n```\n\n### Requirements\n* Python 3.6 and up\n\n### Installation from source\n```\n$ git clone https://github.com/andriyor/amalgama-pq.git\n$ cd amalgama\n$ python setup.py install\n```\n\n## Usage\n\n```\nimport requests\n\nimport amalgama\n\nartist, song = 'Pink Floyd', 'Time'\nurl = amalgama.get_url(artist, song)\ntry:\n    response = requests.get(url)\n    response.raise_for_status()\n    text = amalgama.get_first_translate_text(response.text)\n    print(f'{text}{url}')\nexcept requests.exceptions.HTTPError:\n    print(f'{artist}-{song} not found in amalgama {url}')\n```\n\n## Development\nInstall [Pipenv](https://docs.pipenv.org/)   \n```\n$ pipenv install --dev -e .\n```",
    'author': 'Andriy Orehov',
    'author_email': 'andriyorehov@gmail.com',
    'url': 'https://github.com/andriyor/amalgama-pq',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
