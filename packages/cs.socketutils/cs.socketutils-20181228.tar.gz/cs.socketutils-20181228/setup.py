#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.socketutils',
  description = 'some utilities for network sockets',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20181228',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Topic :: System :: Networking', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.logutils', 'cs.pfx'],
  keywords = ['python2', 'python3'],
  long_description = 'Utility functions and classes for sockets.\n\n## Function `bind_next_port(sock, host, base_port)`\n\nBind the socket `sock` to the first free `(host,port)`; return the port.\n\nParameters:\n* `sock`: open socket.\n* `host`: target host address.\n* `base_port`: the first port number to try.\n\n## Class `OpenSocket`\n\nA file-like object for stream sockets, which uses os.shutdown on close.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.socketutils'],
)
