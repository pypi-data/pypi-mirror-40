# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cellunet', 'cellunet.utils']

package_data = \
{'': ['*'], 'cellunet': ['data/*', 'etc/*']}

install_requires = \
['keras==2.0.0',
 'numpy==1.14.6',
 'pandas==0.23.0',
 'scipy==1.1.0',
 'tensorflow==1.8.0',
 'tifffile>=2019.1,<2020.0']

setup_kwargs = {
    'name': 'cellunet',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'Takamasa Kudo',
    'author_email': 'kudo@stanford.edu',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
