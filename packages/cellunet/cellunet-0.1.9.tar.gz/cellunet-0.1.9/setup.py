# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cellunet', 'cellunet.utils']

package_data = \
{'': ['*'],
 'cellunet': ['data/composite_nuc.tif',
              'data/composite_nuc.tif',
              'data/composite_nuc.tif',
              'data/composite_nuc.tif',
              'data/composite_nuc.tif',
              'data/labels0.tif',
              'data/labels0.tif',
              'data/labels0.tif',
              'data/labels0.tif',
              'data/labels0.tif',
              'data/labels1.tif',
              'data/labels1.tif',
              'data/labels1.tif',
              'data/labels1.tif',
              'data/labels1.tif',
              'data/nuc0.png',
              'data/nuc0.png',
              'data/nuc0.png',
              'data/nuc0.png',
              'data/nuc0.png',
              'data/nuc1.png',
              'data/nuc1.png',
              'data/nuc1.png',
              'data/nuc1.png',
              'data/nuc1.png',
              'etc/*']}

install_requires = \
['keras==2.0.0',
 'numpy==1.14.6',
 'pandas==0.23.0',
 'scikit-image==0.14.1',
 'scipy==1.1.0',
 'tensorflow==1.8.0',
 'tifffile>=2019.1,<2020.0']

setup_kwargs = {
    'name': 'cellunet',
    'version': '0.1.9',
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
