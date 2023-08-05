#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.configutils',
  description = 'utility functions for .ini style configuration files',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190101',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.py3', 'cs.fileutils', 'cs.threads'],
  keywords = ['python2', 'python3'],
  long_description = 'Utility functions and classes for configuration files.\n\n## Class `ConfigSectionWatcher`\n\nMRO: `collections.abc.Mapping`, `collections.abc.Collection`, `collections.abc.Sized`, `collections.abc.Iterable`, `collections.abc.Container`  \nA class for monitoring a particular clause in a config file.\n\n## Class `ConfigWatcher`\n\nMRO: `collections.abc.Mapping`, `collections.abc.Collection`, `collections.abc.Sized`, `collections.abc.Iterable`, `collections.abc.Container`  \nA monitor for a windows style .ini file.\nThe current SafeConfigParser object is presented as the .config property.\n\n## Function `load_config(config_path, parser=None)`\n\nLoad a configuration from the named `config_path`.\n\nIf `parser` is missing or None, use SafeConfigParser (just\nConfigParser in Python 3).\nReturn the parser.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.configutils'],
)
