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
    'version': '0.1.1',
    'description': "Python client for Farsight Security's DNSDB API",
    'long_description': '# fsi-dnsdb\n\nPython client for Farsight Security\'s [DNSDB API](https://api.dnsdb.info/).\n\n## Features\n\n * supports all capabilities of [DNSDB API](https://api.dnsdb.info/)\n * sorting of results by last_seen\n * convert epoch to ISO 8601\n * normalize results with regard sensor or zone observation\n * DNSDB API Error codes returned in JSON data structure\n \n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install fsi-dnsdb.\n\n```bash\npip install fsi-dnsdb\n```\n\n## Usage\n\n```python\nfrom dnsdb import Dnsdb\n\napi_key="12345"\ndnsdb = Dnsdb(api_key)\n\nresults = dnsdb.search(name="fsi.io")\nresults = dnsdb.search(name="mail.fsi.io", inverse=True)\nresults = dnsdb.search(ip="104.244.14.108")\nresults = dnsdb.search(ip="104.244.14.0/24")\nresults = dnsdb.search(ip="2620:11c:f008::108")\nresults = dnsdb.search(hexadecimal="36757a35")\nquota = dnsdb.quota()\n```\n\n## Advanced Usage\n\n```python\nfrom dnsdb import Dnsdb\n\napi_key="12345"\ndnsdb = Dnsdb(api_key)\n\nresults = dnsdb.search(name="fsi.io", type="A")\nresults = dnsdb.search(name="farsightsecurity.com", bailiwick="com.")\nresults = dnsdb.search(name="fsi.io", wildcard_left=True)\nresults = dnsdb.search(name="fsi", wildcard_right=True)\nresults = dnsdb.search(name="fsi.io", sort=False)\nresults = dnsdb.search(name="fsi.io", remote_limit=150000, return_limit=1000)\nresults = dnsdb.search(name="fsi.io", time_last_after=1514764800)\n```\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Gabriel Iovino',
    'author_email': 'giovino@gmail.com',
    'url': 'https://github.com/giovino/fsi-dnsdb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
