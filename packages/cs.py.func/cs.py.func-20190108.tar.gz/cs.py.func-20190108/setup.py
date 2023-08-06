#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.py.func',
  description = 'Convenience facilities related to Python functions. * funccite: cite a function (name and code location) * @prop: replacement for @property which turns internal AttributeErrors into RuntimeErrors * some decorators to verify the return types of functions',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190108',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.py3'],
  keywords = ['python2', 'python3'],
  long_description = "Convenience facilities related to Python functions.\n* funccite: cite a function (name and code location)\n* @prop: replacement for @property which turns internal AttributeErrors into RuntimeErrors\n* some decorators to verify the return types of functions\n\n## Function `callmethod_if(o, method, default=None, a=None, kw=None)`\n\nCall the named `method` on the object `o` if it exists.\n\nIf it does not exist, return `default` (which defaults to None).\nOtherwise call getattr(o, method)(*a, **kw).\n`a` defaults to ().\n`kw` defaults to {}.\n\n## Function `derived_from(property_name)`\n\nA property which must be recomputed\nif the revision of another property exceeds the snapshot revision.\n\n## Function `derived_property(func, original_revision_name='_revision', lock_name='_lock', property_name=None, unset_object=None)`\n\nA property which must be recomputed\nif the reference revision (attached to self)\nexceeds the snapshot revision.\n\n## Function `funccite(func)`\n\nReturn a citation for a function (name and code location).\n\n## Function `funcname(func)`\n\nReturn a name for the supplied function `func`.\nSeveral objects do not have a __name__ attribute, such as partials.\n\n## Function `prop(func)`\n\nA substitute for the builtin @property.\n\nThe builtin @property decorator lets internal AttributeErrors escape.\nWhile that can support properties that appear to exist conditionally,\nin practice this is almost never what I want, and it masks deeper errors.\nHence this wrapper for @property that transmutes internal AttributeErrors\ninto RuntimeErrors.\n\n## Function `returns_bool(func)`\n\nDecorator for functions which should return Booleans.\n\n## Function `returns_str(func)`\n\nDecorator for functions which should return strings.\n\n## Function `returns_type(func, basetype)`\n\nDecrator which checks that a function returns values of type `basetype`.\n\n## Function `yields_str(func)`\n\nDecorator for generators which should yield strings.\n\n## Function `yields_type(func, basetype)`\n\nDecorator which checks that a generator yields values of type `basetype`.",
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.py.func'],
)
