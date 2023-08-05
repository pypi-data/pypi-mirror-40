#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.vt',
  description = 'A content hash based data store with a filesystem layer, using variable sized blocks, arbitrarily sized data and utilising some domain knowledge to aid efficient block boundary selection.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20181231.1',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Development Status :: 2 - Pre-Alpha', 'Environment :: Console', 'Programming Language :: Python :: 3', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  entry_points = {'console_scripts': ['vt = cs.vt.__main__:main']},
  install_requires = ['cs.buffer', 'cs.app.flag', 'cs.binary', 'cs.binary_tests', 'cs.cache', 'cs.debug', 'cs.deco', 'cs.env', 'cs.excutils', 'cs.fileutils', 'cs.inttypes', 'cs.later', 'cs.lex', 'cs.logutils', 'cs.mappings', 'cs.packetstream', 'cs.pfx', 'cs.progress', 'cs.py.func', 'cs.py.stack', 'cs.queues', 'cs.range', 'cs.resources', 'cs.result', 'cs.seq', 'cs.serialise', 'cs.socketutils', 'cs.threads', 'cs.tty', 'cs.units', 'cs.x', 'lmdb'],
  keywords = ['python3'],
  long_description = 'A content hash based data store with a filesystem layer, using\nvariable sized blocks, arbitrarily sized data and utilising some\ndomain knowledge to aid efficient block boundary selection.\n\n*NOTE*: pre-Alpha; alpha release following soon once the packaging\nis complete.\n\nSee also the Plan 9 Venti system:\n(http://library.pantek.com/general/plan9.documents/venti/venti.html,\nhttp://en.wikipedia.org/wiki/Venti).\n\n## Class `DebuggingLock`\n\nA wrapper for a threading Lock or RLock\nto notice contention and report contending uses.\n\n## Function `fromtext(s)`\n\nReturn raw byte array from text/hexadecimal string.\n\n## Class `LockContext`\n\nMRO: `builtins.tuple`  \nLockContext(caller, thread)\n\n## Function `totext(data)`\n\nRepresent a byte sequence as a hex/text string.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  packages = ['cs.vt'],
)
