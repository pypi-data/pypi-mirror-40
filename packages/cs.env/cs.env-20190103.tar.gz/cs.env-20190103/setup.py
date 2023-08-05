#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.env',
  description = 'Some environment related functions.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190103',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.lex'],
  keywords = ['python2', 'python3'],
  long_description = "Some environment related functions.\n\n* LOGDIR, VARRUN, FLAGDIR: lambdas defining standard places used in other modules\n\n* envsub: replace substrings of the form '$var' with the value of 'var' from `environ`.\n\n* getenv: fetch environment value, optionally performing substitution\n\n## Function `envsub(s, environ=None, default=None)`\n\nReplace substrings of the form '$var' with the value of 'var' from environ.\n\nParameters:\n* `environ`: environment mapping, default `os.environ`.\n* `default`: value to substitute for unknown vars;\n        if `default` is `None` a `ValueError` is raised.\n\n## Function `getenv(var, default=None, environ=None, dosub=False)`\n\nFetch environment value.\n\nParameters:\n* `var`: name of variable to fetch.\n* `default`: default value if not present. If not specified or None,\n    raise KeyError.\n* `environ`: environment mapping, default `os.environ`.\n* `dosub`: if true, use envsub() to perform environment variable\n    substitution on `default` if it used. Default value is `False`.",
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.env'],
)
