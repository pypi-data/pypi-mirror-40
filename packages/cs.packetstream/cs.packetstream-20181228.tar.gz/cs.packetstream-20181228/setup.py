#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.packetstream',
  description = 'general purpose bidirectional packet stream connection',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20181228',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Topic :: System :: Networking', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.logutils', 'cs.pfx'],
  keywords = ['python2', 'python3'],
  long_description = 'A general purpose bidirectional packet stream connection.\n\n## Class `Packet`\n\nMRO: `cs.binary.PacketField`, `abc.ABC`  \nA protocol packet.\n\n## Class `PacketConnection`\n\nA bidirectional binary connection for exchanging requests and responses.\n\n## Class `Request_State`\n\nMRO: `builtins.tuple`  \nRequestState(decode_response, result)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.packetstream'],
)
