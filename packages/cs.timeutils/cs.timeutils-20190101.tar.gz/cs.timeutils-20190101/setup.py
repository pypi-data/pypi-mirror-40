#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.timeutils',
  description = 'convenience routines for times and timing',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190101',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  long_description = "Convenience routines for timing.\n\n## Function `ISOtime(gmtime)`\n\nProduce an ISO8601 timestamp string from a UNIX time.\n\n## Function `sleep(delay)`\n\ntime.sleep() sometimes sleeps significantly less that requested.\nThis function calls time.sleep() until at least `delay` seconds have\nelapsed, trying to be precise.\n\n## Function `time_from_ISO(isodate, islocaltime=False)`\n\nParse an ISO8601 date string and return seconds since the epoch.\nIf islocaltime is true convert using localtime(tm) otherwise use\ngmtime(tm).\n\n## Function `time_func(func, *args, **kw)`\n\nRun the supplied function and arguments.\nReturn a the elapsed time in seconds and the function's own return value.\n\n## Function `tm_from_ISO(isodate)`\n\nParse an ISO8601 date string and return a struct_time.",
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.timeutils'],
)
