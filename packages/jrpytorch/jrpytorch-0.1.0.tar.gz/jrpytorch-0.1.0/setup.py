# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jrpytorch']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0,<4.0',
 'numpy>=1.15,<2.0',
 'sklearn>=0.0.0,<0.0.1',
 'torch>=1.0,<2.0',
 'torchvision>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'jrpytorch',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jamie',
    'author_email': 'jamie@jumpingrivers.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
