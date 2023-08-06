# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['twodo_domain']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses>=0.6,<0.7']

setup_kwargs = {
    'name': 'twodo-domain',
    'version': '0.0.1',
    'description': 'The domain (entities) of the 2do app.',
    'long_description': '# 2do-domain\nEntity domain of the application 2DO\n\n## Warning\n\nThis is just an experiment...there is (I mean, I did not create) any real 2DO app.\n',
    'author': 'Alexandre Souza',
    'author_email': '0x41e@protonmail.ch',
    'url': 'https://github.com/alexandre/twodo_domain',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
