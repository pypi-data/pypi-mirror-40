# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['whost', 'whost.ui']

package_data = \
{'': ['*']}

install_requires = \
['PyYaml>=3.13,<4.0',
 'colorama>=0.4.1,<0.5.0',
 'humanfriendly>=4.17,<5.0',
 'ipython>=7.2,<8.0',
 'netifaces>=0.10.7,<0.11.0',
 'requests>=2.21,<3.0',
 'tabulate>=0.8.2,<0.9.0',
 'unidecode>=1.0,<2.0']

setup_kwargs = {
    'name': 'whost',
    'version': '0.1.12',
    'description': 'Cardshop Writer Host Tools',
    'long_description': '# Cardshop Writer Host\n\nCardshop use writer hosts to download, write and ship SD-cards to recipient.\nA WriterHost is an always-running, always-connected computer connected to one or more USB SD-card readers.\n\nWriter Hosts authenticate with the cardshop fetch tasks. The WriterHost operator is contacted (email) when an SD-card must be inserted, retrieved and shipped.\n\n## Requirements\n\n* always-on-capable computer\n* 500GB storage or more.\n* high-speed, direct, permanent connection to internet via ethernet.\n* one or more good-quality USB SD-card readers (Kingston)\n* A `writer` account on the cardshop.\n* An assigned port on the demo server (see [maintenance](http://wiki.kiwix.org/wiki/Cardshop-maintenance)).\n\n## Setup\n\n1. Install Ubuntu 18.04.1 LTS server with default options (see below)\n* log-in and elevate as `root` (`sudo su -`)\n* set a password for `root` (`passwd`)\n* Make sure internet is working\n* download/copy your tunnel private key to `/root/.ssh/tunnel` (chmod `600`)\n* download setup script `curl -L -o /tmp/whost-setup https://raw.githubusercontent.com/kiwix/cardshop/master/whost/whost-setup`\n* run the setup script `chmod +x /tmp/whost-setup && REVERSE_SSH_PORT=XXX /tmp/whost-setup`\n\n### Ubuntu Install\n\nJust a regular, fresh Ubuntu-server install. Bellow are the defaults used for tests.\n\n1. Boot off the install media & select *Install Ubuntu Server* at grub prompt.\n* Select language (*English*)\n* Select Keyboard layout (*English (US)*, *English (US)*)\n* Select *Install Ubuntu* (not cloud instance)\n* Configure the network (*eth via dhcp*)\n* Proxy Address: none\n* Mirror Address: http://archive.ubuntu.com/ubuntu (pre-filled default)\n* *Use an entire Disk*\n* Choose disk to install to: *selected disk*\n* Summary: confirm and continue\n* Profile\n * name: `maint`\n * server name: whatever (`bkored`)\n * username: `maint`\n * password: `maint`\n * Import Identity: *from github* > `rgaudin`\n* *Reboot now*\n* Remove install media then `ENTER`\n \n \n',
    'author': 'renaud gaudin',
    'author_email': 'reg@kiwix.org',
    'url': 'https://www.kiwix.org/kiwix-hotspot/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
