# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['picard']

package_data = \
{'': ['*']}

install_requires = \
['typing_extensions>=3.6,<4.0']

extras_require = \
{'aws': ['boto3>=1.9,<2.0']}

setup_kwargs = {
    'name': 'picard.py',
    'version': '0.1.0',
    'description': 'Make it so.',
    'long_description': None,
    'author': 'John Freeman',
    'author_email': 'jfreeman08@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
