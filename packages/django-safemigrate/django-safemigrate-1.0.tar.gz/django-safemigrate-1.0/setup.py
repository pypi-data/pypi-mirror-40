# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['django_safemigrate',
 'django_safemigrate.management',
 'django_safemigrate.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.1,<3.0']

setup_kwargs = {
    'name': 'django-safemigrate',
    'version': '1.0',
    'description': 'Safely run migrations before deployment',
    'long_description': None,
    'author': 'Ryan Hiebert',
    'author_email': 'ryan@aspiredu.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
