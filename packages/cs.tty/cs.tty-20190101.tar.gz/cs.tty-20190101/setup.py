#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.tty',
  description = 'Functions related to terminals.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190101',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Environment :: Console', 'Operating System :: POSIX', 'Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Topic :: Terminals', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  long_description = 'Functions related to terminals.\n\n## Function `setupterm(*args)`\n\nRun curses.setupterm, needed to be able to use the status line.\nUses a global flag to avoid doing this twice.\n\n## Function `statusline(text, fd=None, reverse=False, xpos=None, ypos=None)`\n\nUpdate the status line.\n\n## Function `statusline_bs(text, reverse=False, xpos=None, ypos=None)`\n\nReturn a byte string to update the status line.\n\n## Function `ttysize(fd)`\n\nReturn a (rows, columns) tuple for the specified file descriptor.\n\nIf the window size cannot be determined, None will be returned\nfor either or both of rows and columns.\n\nThis function relies on the UNIX `stty` command.\n\n## Class `WinSize`\n\nMRO: `builtins.tuple`  \nWinSize(rows, columns)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.tty'],
)
