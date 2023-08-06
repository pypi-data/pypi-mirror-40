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
    'version': '0.1.4',
    'description': 'Google Cloud Platform Condor Pool Manager',
    'long_description': '# Google Cloud Platform Condor Pool Manager (GCPM)\n\n[![Build Status](https://travis-ci.org/mickaneda/gcpm.svg?branch=master)](https://travis-ci.org/mickaneda/gcpm) ([Coverage report](https://mickaneda.github.io/gcpm/))\n\nHTCondor pool manager for Google Cloud Platform.\n\n## Installation\n\n### Package installation\n\nGCPM can be installed by `pip`:\n\n    $ pip install gcpm\n\n### Service file installation\n\nTo install as service, do:\n\n    $ gcpm install\n\n:warning: Service installation is valid only for the system managed by **Systemd**.\n\nIf **logrotate** is installed, logrotation definition for **/var/log/gcpm.log** is also installed.\n\n## Configuration file\n\n### Configuration file path\n\nThe default configuration file is **~/.config/gcpm/gcpm.yml**.\n\nFor service, the configuration file is **/etc/gcpm.yml**.\n\nTo change the configuration file, use `--config` option:\n\n    $ gcpm run --config /path/to/my/gcpm.yml\n\n### Configuration file content\n\nA configuration file is YAML format.\n\nName|Description|Default Value|Mandatory|\n:---|:----------|:------------|:--------|\nconfig_dir   | Directory for some gcpm related files.|**~/.config/gcpm/** (user)<br>**/var/cache/gcpm** (service)|No\noatuh_file   | Path to OAuth information file for GCE/GCS usage.|**<config_dir>/oauth**|No\nservice_account_file | Service account JSON file for GCE/GCS usage.<br>If not specified, OAuth connection is tried.|-|No\nproject      | Google Cloud Platform Project Name.|-|Yes\nzone         | Zone for Google Compute Engine.|-|Yes\nmachines     | Array of machine settings.<br>Each setting is array of [core, mem, disk, idle, image] (see below).|[]|Yes\nmachines:core | Number of core of the machine type.|-|Yes\nmachines:mem | Memory (MB) of the machine type.|-|Yes\nmachines:disk | Disk size (GB) of the machine type.|-|Yes\nmachines:max | Limit of the number of instances for the machine type.|-|Yes\nmachines:idle | Number of idle machines for the machine type.|-|Yes\nmachines:image | Image of the machine type.|-|Yes\nmax_cores    | Limit of the total number of cores of all instances.<br>If it is set 0, no limit is applied.|0|No\nstatic       | Array of instance names which should run always.|[]|No\nprefix       | Prefix of machine names.|**gcp-wn**|No\npreemptible  | 1 for preemptible machines, 0 for not.|0|No\noff_timer    | Second to send condor_off after starting.|0|No\nnetwork_tag  | Array of GCP network tag.|[]|No\nreuse        | 1 to reused terminated instance. Otherwise delete and re-created instances.|0|No\ninterval     | Second of interval for each loop.|10|No\nhead_info    | If **head** is empty, head node information is automatically taken for each option:<br>hostname: Hostname<br>ip: IP address<br>gcp: Hostname|**gcp**|No\nhead         | Head node Hostname/IP address.|""|No\nport         | HTCondor port.|9618|No\ndomain       | Domain of the head node.<br>Set empty to take it from hostnaem.|""|No\nadmin        | HTCondor admin email address.|""|Yes\nowner        | HTCondor owner name.|""|Yes\nwait_cmd     | 1 to wait GCE commands result (create/start/stop/delete...).|0|No\nbucket       | Bucket name for pool_password file.|""|Yes\nstorageClass | Storage class name of the bucket.|"REGIONAL"|No\nlocation     | Storage location for the bucket.<br>If empty, it is decided from the **zone**.|""|No\nlog_file     | Log file path. Empty to put it in stdout.|""|No\nlog_level    | Log level. (**debug**, **info**, **warning**, **error**, **critical**)|**info**|No\n',
    'author': 'Michiru Kaneda',
    'author_email': 'Michiru.Kaneda@gmail.com',
    'url': 'https://github.com/mickaneda/gcpm',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
