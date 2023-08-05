#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.py.stack',
  description = 'Convenience functions for the python execution stack.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190101',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  long_description = "I find the supplied python traceback facilities quite awkward.\nThese functions provide convenient facilities.\n\n## Function `caller(frame_index=-3)`\n\nReturn the `Frame` of the caller's caller.\n\nUseful `frame_index` values:\n* `-1`: caller, this function\n* `-2`: invoker, who wants to know the caller\n* `-3`: the calling function of the invoker\n\n## Class `Frame`\n\nMRO: `Frame`, `builtins.tuple`  \nNamedtuple for stack frame contents.\n\n## Function `frames()`\n\nReturn the current stack as a list of Frame objects.\n\n## Function `stack_dump(fp=None, indent=0, Fs=None)`\n\nRecite current or supplied stack to `fp`, default sys.stderr.",
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.py.stack'],
)
