jk_rawhtml
==========

Introduction
------------

This python module provides support for programmatically generating HTML5 code.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-rawhtml)
* [pypi.python.org](https://pypi.python.org/pypi/jk_rawhtml)

Motivation
----------

In most use cases it is very convenient to use one of the many template languages to create HTML output.
But using a template engine will require ...

* including another module in the source
* packing a variety of additional files into your software

While including another Python module is probably the least of your concern unfortunately there are some
use cases where a more simplistic approach would be much more convenient: Whenever you do *not* want to
include more files into the software you provide or whenever you do very simple things and don't want to
overcomplicate your software.

This work has been inspired by some old work of Tavis Rudd
(https://bitbucket.org/tavisrudd/throw-out-your-templates) which - at the
time of this writing - seems to have been abandoned as his code is neither a real python module nor does
it support Python 3.

The goal of this new module `jk_rawhtml` is to provide an easy way of generating state-of-the-art HTML5
code programmatically and being well suited to use in recent Python prorgams. A completely new implementation
approach has been taken in order to implement this module `jk_rawhtml` in Python 3 as a state-of-the-art module.
The idea of `jk_rawhtml` is to provide a simple, well structured, maintainable approach for HTML generation
with support for CSS and SVG (in the long run) by intentionally leaving out older HTML standards
as these are obsolete now obsolete.

As this module is quite new and not every detail has yet been implemented, it already is ready to be used
and should not have any serious bugs. If you find any issues, please feel free to report them.

How to use this module
----------------------

...TODO...

Contact Information
-------------------

This is Open Source code. That not only gives you the possibility of freely using this code it also
allows you to contribute. Feel free to contact the author(s) of this software listed below, either
for comments, collaboration requests, suggestions for improvement or reporting bugs:

* Jürgen Knauth: jknauth@uni-goettingen.de, pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



