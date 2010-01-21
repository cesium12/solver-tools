Installing solvertools
======================

If Solvertools is whining at you with import errors, the appropriate
thing to do is run "sudo python setup.py develop". This adds
solvertools to the global Python namespace.

This requires python-distribute, or at least python-setuptools.

If you don't believe in packaging, that's fine, just set your
PYTHONPATH to the directory setup.py is in instead.

I aim to keep packaging bullshit to a minimum, because it is the least
fun part of Python. To that end, we should not use pkg_resources or
anything like it. We will not set zip_safe=True. And we will never,
never, never attempt to use a namespace package for anything.

Rob Speer, 2010

Automated sphinx-based documentation system
===========================================

The documentation system for solver-tools is called Sphinx.
Documentation on it is available at
http://sphinx.pocoo.org/contents.html.  Particular attention should be
given to the instructions for automatically generating code from
docstrings: http://sphinx.pocoo.org/ext/autodoc.html.

The top-level index document is :file:`index.rst` in the top of the
repository, and the documentation can be built by use of the
:file:`Makefile` also in the top-level directory.

The documentation is automatically rebuilt hourly and served from
https://svn.manicsages.org/docs/solver-tools/.

Jason Alonso, 2008

.. vim: tw=70
