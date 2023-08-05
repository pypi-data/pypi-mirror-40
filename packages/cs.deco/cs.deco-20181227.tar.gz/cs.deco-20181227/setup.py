#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.deco',
  description = 'Assorted decorator functions.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20181227',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.pfx'],
  keywords = ['python2', 'python3'],
  long_description = "Assorted decorator functions.\n\n## Function `decorator(deco, *da, **dkw)`\n\nWrapper for decorator functions to support optional keyword arguments.\n\nExamples:\n\n    @decorator\n    def dec(func, **dkw):\n      ...\n    @dec\n    def func1(...):\n      ...\n    @dec(foo='bah')\n    def func2(...):\n      ...",
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.deco'],
)
