# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dnsdb']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'dnsdb',
    'version': '0.1.0',
    'description': "A Python Client to interact with Farsight Security's DNSDB API",
    'long_description': None,
    'author': 'Gabriel Iovino',
    'author_email': 'giovino@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
