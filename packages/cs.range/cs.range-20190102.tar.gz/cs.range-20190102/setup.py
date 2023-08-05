#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.range',
  description = 'a Range class implementing compact integer ranges with a set-like API, and associated functions',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190102',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.logutils', 'cs.seq'],
  keywords = ['python2', 'python3'],
  long_description = 'A Range is an object resembling a set but optimised for contiguous\nranges of int members.\n\n## Function `overlap(span1, span2)`\n\nReturn a list `[start,end]` denoting the overlap of two spans.\n\nExample:\n\n    >>> overlap([1,9], [5,13])\n    [5, 9]\n\n## Class `Range`\n\nA collection of ints that collates adjacent ints.\n\nThe interface is as for a `set` with additional methods:\n* `spans()`: return an iterable of `Spans`, with `.start`\n  included in each `Span` and `.end` just beyond\n\nAdditionally, the update/remove/etc methods have a secondary\ncalling signature: `(start,end)`, which is the same as passing\nin `Range(start,end)` but much more efficient.\n\n## Class `Span`\n\nMRO: `Span`, `builtins.tuple`  \nA namedtuple with `.start` and `.end` attributes.\n\n## Function `spans(items)`\n\nReturn an iterable of `Spans` for all contiguous sequences in\n`items`.\n\nExample:\n\n    >>> list(spans([1,2,3,7,8,11,5]))\n    [1:4, 7:9, 11:12, 5:6]',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.range'],
)
