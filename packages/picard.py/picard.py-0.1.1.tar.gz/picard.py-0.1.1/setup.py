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
    'version': '0.1.1',
    'description': 'Make it so.',
    'long_description': '======\npicard\n======\n-----------\nMake it so.\n-----------\n\n.. start-include\n\n.. image:: https://travis-ci.org/thejohnfreeman/picard.svg?branch=master\n   :target: https://travis-ci.org/thejohnfreeman/picard\n   :alt: Build Status\n.. image:: https://readthedocs.org/projects/picard/badge/?version=latest\n   :target: https://picard.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\nThe idea of Ansible_ with the execution of Make_.\n\n.. _Ansible: https://www.ansible.com/overview/how-ansible-works\n.. _Make: https://www.gnu.org/software/make/manual/make.html\n\nWith Picard, you define a set of targets, each with a recipe that leaves it in\na desired state, e.g. a compiled executable or a running service. Targets may\ndepend on each other, e.g. "this executable depends on that source file" or\n"this service depends on that host", in a directed acyclic graph. Like Make,\nPicard executes the recipes for targets in dependency order.\n\nLike Ansible, Picard comes with many sophisticated recipes out-of-the-box\nthat behave like rsync_: they find the differences between a target\'s present\nstate and its goal state, and execute just the changes necessary to transition\nfrom the first to the second.\n\n.. _rsync: https://linux.die.net/man/1/rsync\n\nMake is limited to considering targets on the local filesystem, while Ansible\ncan consider more general targets and states, e.g. the existence and\nconfiguration of remote machines. Ansible\'s input is a rigid declarative\ntemplate (based on Jinja_), while Make\'s input is an executable script that\nbuilds the abstract definitions of the targets and gets to leverage functions\nand variables. Picard tries to combine the best of both worlds in pure Python.\n\n.. _Jinja: http://jinja.pocoo.org/\n\n.. end-include\n\nHelp\n====\n\nPlease see the documentation on `Read the Docs`_.\n\n.. _`Read the Docs`: https://picard.readthedocs.io\n\nIf you have any questions, please ask me_ in the issues_, by email_, over\nTwitter_, or however you want to reach me. I\'ll be happy to help you, because\nit will help me make this documentation better for the next reader.\n\n.. _me: https://github.com/thejohnfreeman\n.. _issues: https://github.com/thejohnfreeman/picard/issues\n.. _email: mailto:jfreeman08@gmail.com\n.. _Twitter: https://twitter.com/thejohnfreeman\n',
    'author': 'John Freeman',
    'author_email': 'jfreeman08@gmail.com',
    'url': 'https://github.com/thejohnfreeman/picard',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
