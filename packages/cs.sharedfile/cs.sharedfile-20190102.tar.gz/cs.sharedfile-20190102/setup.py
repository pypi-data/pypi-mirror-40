#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.sharedfile',
  description = 'facilities for shared access to files',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190102',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.filestate', 'cs.lex', 'cs.logutils', 'cs.pfx', 'cs.range', 'cs.timeutils'],
  keywords = ['python2', 'python3'],
  long_description = 'Facilities for shared access to files.\n\n## Function `lockfile(path, ext=None, poll_interval=None, timeout=None)`\n\nA context manager which takes and holds a lock file.\n\nParameters:\n* `path`: the base associated with the lock file.\n* `ext`:\n  the extension to the base used to construct the lock file name.\n  Default: `".lock"`\n* `timeout`: maximum time to wait before failing,\n  default None (wait forever).\n* `poll_interval`: polling frequency when timeout is not 0.\n\n## Class `SharedAppendFile`\n\nA base class to share a modifiable file between multiple users.\n\nThe use case was driven from the shared CSV files used by\n`cs.nodedb.csvdb.Backend_CSVFile`, where multiple users can\nread from a common CSV file, and coordinate updates with a\nlock file.\n\nThis presents the following interfaces:\n* `__iter__`: yields data chunks from the underlying file up\n  to EOF; it blocks no more than reading from the file does.\n  Note that multiple iterators share the same read pointer.\n\n* `open`: a context manager returning a writable file for writing\n  updates to the file; it blocks reads from this instance\n  (though not, of course, by other users of the file) and\n  arranges that users of `__iter__` do not receive their own\n  written data, thus arranging that `__iter__` returns only\n  foreign file updates.\n\nSubclasses would normally override `__iter__` to parse the\nreceived data into their natural records.\n\n## Class `SharedAppendLines`\n\nMRO: `SharedAppendFile`  \nA line oriented subclass of `SharedAppendFile`.\n\n## Class `SharedCSVFile`\n\nMRO: `SharedAppendLines`, `SharedAppendFile`  \nShared access to a CSV file in UTF-8 encoding.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.sharedfile'],
)
