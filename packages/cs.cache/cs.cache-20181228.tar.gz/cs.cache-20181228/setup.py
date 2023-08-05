#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.cache',
  description = 'caching data structures and other lossy things with capped sizes',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20181228',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  long_description = 'A few caching facilities.\n\n## Class `LRU_Cache`\n\nA simple least recently used cache.\n\nUnlike `functools.lru_cache`\nthis provides `on_add` and `on_remove` callbacks.\n\n## Function `lru_cache(maxsize=None, cache=None, on_add=None, on_remove=None)`\n\nEnhanced workalike of @functools.lru_cache.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.cache'],
)
