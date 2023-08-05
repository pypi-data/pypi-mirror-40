# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['pydantic_openapi']

package_data = \
{'': ['*']}

install_requires = \
['inflection', 'pydantic>=0.16,<0.17']

setup_kwargs = {
    'name': 'pydantic-openapi',
    'version': '0.1.2',
    'description': 'Generate OpenAPI schema from pydantic models',
    'long_description': None,
    'author': 'Yury Blagoveshchenskiy',
    'author_email': 'yurathestorm@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
