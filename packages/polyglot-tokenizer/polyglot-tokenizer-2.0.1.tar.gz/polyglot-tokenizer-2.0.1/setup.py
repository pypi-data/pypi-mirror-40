# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['polyglot_tokenizer', 'polyglot_tokenizer.tests']

package_data = \
{'': ['*'], 'polyglot_tokenizer': ['data/*']}

install_requires = \
['pbr>=5.1,<6.0', 'six>=1.12,<2.0']

setup_kwargs = {
    'name': 'polyglot-tokenizer',
    'version': '2.0.1',
    'description': "Tokenizer for world's most spoken languages and social media texts like Facebook, Twitter etc.",
    'long_description': None,
    'author': 'irshadbhat',
    'author_email': 'bhatirshad127@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
