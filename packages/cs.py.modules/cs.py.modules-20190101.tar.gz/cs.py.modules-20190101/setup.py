#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.py.modules',
  description = 'module/import related stuff',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190101',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  long_description = 'Convenience functions related to modules and importing.\n\n## Function `import_module_name(module_name, name, path=None, lock=None)`\n\nImport `module_name` and return the value of `name` within it.\n\nParameters:\n* `module_name`: the module name to import.\n* `name`: the name within the module whose value is returned;\n  if `name` is None, return the module itself.\n* `path`: an array of paths to use as sys.path during the import.\n* `lock`: a lock to hold during the import (recommended).\n\n## Function `module_attributes(M)`\n\nGenerator yielding the names and values of attributes from a module\nwhich were defined in the module.\n\n## Function `module_files(M)`\n\nGenerator yielding .py pathnames involved in a module.\n\n## Function `module_names(M)`\n\nReturn a list of the names of attributes from a module which were\ndefined in the module.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.py.modules'],
)
