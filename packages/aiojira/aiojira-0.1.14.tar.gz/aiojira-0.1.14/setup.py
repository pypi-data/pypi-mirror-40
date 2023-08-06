# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiojira']

package_data = \
{'': ['*']}

install_requires = \
['aioify>=0.3.1,<0.4.0', 'jira>=2.0,<3.0', 'poetry-version>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'aiojira',
    'version': '0.1.14',
    'description': 'Asynchronous Jira library',
    'long_description': "# aiojira - asynchronous Jira Python library\n[![License](https://img.shields.io/pypi/l/aiojira.svg)](https://www.apache.org/licenses/LICENSE-2.0)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiojira.svg)\n[![PyPI](https://img.shields.io/pypi/v/aiojira.svg)](https://pypi.org/project/aiojira/)\n\nAsynchronous Jira Python library - asynchronous wrapper for https://github.com/pycontribs/jira\n\n## Installation\nTo install from [PyPI](https://pypi.org/project/aiojira/) run:\n```shell\n$ pip install https://github.com/yifeikong/aioify/archive/master.zip\n$ pip install aiojira\n```\n\n## Usage\nFor documentation refer to https://jira.readthedocs.io, because `aiojira` uses the same API as `jira` with 2 exceptions:\n1. All functions are converted to coroutines, that means you have to add `await` keyword before all function calls.\n2. To asynchronously create classes from `aiojira` use static method `create`.\n\nExample:\n```python\nimport asyncio\nimport aiojira\n\n\nserver = 'https://jira.example.com/'\nauth = ('user', 'password')\n\nJIRA = asyncio.run(aiojira.JIRA.create(server=server, basic_auth=auth))\nprojects = asyncio.run(JIRA.projects())\nprint(projects)\n```\n",
    'author': 'Roman Inflianskas',
    'author_email': 'r.inflyanskas@zmeke.com',
    'url': 'https://github.com/rominf/aiojira',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
