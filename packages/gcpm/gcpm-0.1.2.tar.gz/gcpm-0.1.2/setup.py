# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['gcpm']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.1.3,<0.2.0',
 'google-api-python-client>=1.7,<2.0',
 'google-auth-httplib2>=0.0.3,<0.0.4',
 'google-auth>=1.6,<2.0',
 'oauth2client>=4.1,<5.0',
 'ruamel.yaml>=0.15.83,<0.16.0']

entry_points = \
{'console_scripts': ['gcpm = gcpm:main']}

setup_kwargs = {
    'name': 'gcpm',
    'version': '0.1.2',
    'description': 'HTCondor pool manager for Google Cloud Platform.',
    'long_description': '# gcp_condor_pool_manager (gcpm)\n\n[![Build Status](https://travis-ci.org/mickaneda/gcpm.svg?branch=master)](https://travis-ci.org/mickaneda/gcpm) ([Coverage report](https://mickaneda.github.io/gcpm/))\n\nHTCondor pool manager for Google Cloud Platform.\n\n',
    'author': 'Michiru Kaneda',
    'author_email': 'Michiru.Kaneda@gmail.com',
    'url': 'https://github.com/mickaneda/gcp_condor_pool_manager',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
