.. _install:

Installing solvertools
======================

The short answer on how to install this:

* ``sudo python setup.py develop``
* Or, set your ``PYTHONPATH`` to this directory

Longer answer:

If Solvertools is whining at you with import errors, the appropriate
thing to do is run "sudo python setup.py develop". This adds
solvertools to the global Python namespace.

Doing this requires python-distribute, or at least python-setuptools.

If you don't believe in packaging, that's fine, just set your
PYTHONPATH to the directory setup.py is in instead.

I aim to keep packaging bullshit to a minimum, because it is the least
fun part of Python. To that end, we should not use pkg_resources or
anything like it. We will not set zip_safe=True. And we will never,
never, never attempt to use a namespace package for anything.

Rob Speer, 2010

