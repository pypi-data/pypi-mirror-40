#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.serialise',
  description = 'Some serialising functions, now mostly a thin wrapper for the cs.binary functions.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190103',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.binary'],
  keywords = ['python2', 'python3'],
  long_description = "Some serialising functions, now mostly a thin wrapper for the cs.binary functions.\n\n## Function `get_bs(data, offset=0)`\n\nRead an extensible byte serialised unsigned int from `data` at `offset`.\nReturn value and new offset.\n\nContinuation octets have their high bit set.\nThe value is big-endian.\n\nIf you just have a bytes instance, this is the go. If you're\nreading from a stream you're better off with `cs.binary.BSUint`.",
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.serialise'],
)
