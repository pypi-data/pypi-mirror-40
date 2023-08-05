# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['annict']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.12.1,<0.13.0',
 'furl>=2.0,<3.0',
 'rauth>=0.7.3,<0.8.0',
 'requests-cache>=0.4.13,<0.5.0',
 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'annict',
    'version': '0.7.0',
    'description': 'Annict API for python',
    'long_description': '# python-annict\n\n[Annict API](https://docs.annict.com/ja/api/) wrapper for Python\n\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e7936cf6e72a4e14b3bfb07879de1c3d)](https://app.codacy.com/app/hiro.ashiya/python-annict?utm_source=github.com&utm_medium=referral&utm_content=kk6/python-annict&utm_campaign=Badge_Grade_Dashboard)\n[![CircleCI](https://img.shields.io/circleci/project/github/kk6/python-annict.svg?style=flat-square)](https://circleci.com/gh/kk6/python-annict)\n[![PyPI](https://img.shields.io/pypi/v/annict.svg?style=flat-square)](https://pypi.org/project/annict/)\n[![License](https://img.shields.io/pypi/l/annict.svg)](https://pypi.org/project/annict/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n**python-annict** officially supports Python 3.6 or higher.\n\n## Installation\n\n```bash\npip install annict\n```\n\n## Quickstart\n\n### Authentication\n\nAcquire the URL for authentication code.\n\n```python\n>>> from annict.auth import OAuthHandler\n>>> handler = OAuthHandler(client_id=\'Your client ID\', client_secret=\'Your client secret\')\n>>> url = handler.get_authorization_url(scope=\'read write\')\n>>> print(url)\n```\n\nOpen the browser and access the URL you obtained, the authentication code will be displayed.\nIt will be passed to the `handler.authenticate()` \'s argument to get the access token.\n\n```python\n>>> handler.authenticate(code=\'Authentication code\')\n>>> print(handler.get_access_token())\n```\n\nNote that this authentication flow is unnecessary when issuing a personal access token on Annict and using it.\n\nSee: [Annict API: 個人用アクセストークンが発行できるようになりました](http://blog.annict.com/post/157138114218/personal-access-token)\n\n### Hello world\n\n\n```python\n>>> from annict.api import API\n>>> annict = API(\'Your access token\')\n>>> results = annict.works(filter_title="Re:ゼロから始める異世界生活")\n>>> print(results[0].title)\nRe:ゼロから始める異世界生活\n```\n\n### Cache\n\nFor now, we do not have our own cache system. However, caching is also important to reduce the load on AnnictAPI.\n\nSo I introduce a cache plugin for *requests* library called [requests_cache](https://github.com/reclosedev/requests-cache).\n\nInstall with pip.\n\n```bash\npip insall requests_cache\n```\n\n*requests_cache* is very easy to use.\n\n```python\n>>> import requests_cache\n>>> requests_cache.install_cache(cache_name=\'annict\', backend=\'memory\', expire_after=300)\n>>> # At first, from Annict API.\n>>> api.me()\n>>> # You can get results from cache, if it is within the expiration time.\n>>> api.me()\n\n```\n\nFor more information: [Requests-cache documentation](https://requests-cache.readthedocs.io/en/latest/) \n\n## Documentation\n\n- [This library\'s documentation](https://pythonhosted.org/annict/)\n- [Annict Docs(Japanese)](https://docs.annict.com/ja/)\n',
    'author': 'kk6',
    'author_email': 'hiro.ashiya@gmail.com',
    'url': 'https://annict.jp/userland/projects/7',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
