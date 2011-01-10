.. _install:

Installing solvertools
======================

If you don't already have the code, you should:

- Install Git, if necessary
- Install Python (with development headers), NumPy, GCC, and SWIG
  (on Ubuntu: `aptitude install build-essential python-dev python-numpy swig`)
- Get access to git.manicsages.org from Jason Alonso (jalonso), if necessary
- `git clone git@git.manicsages.org:solver-tools.git`

The short answer on how to install this:

- ``sudo python setup.py develop``
- Or, set your ``PYTHONPATH`` to this directory

Longer answer:

If Solvertools is whining at you with import errors, the appropriate
thing to do is run "sudo python setup.py develop". This adds
solvertools to the global Python namespace.

Doing this requires python-distribute, or at least python-setuptools. It also
needs to be able to compile some C code using SWIG.

If you don't believe in packaging, that's fine, just set your
PYTHONPATH to the directory setup.py is in instead. You might have to compile
C extensions, like Regulus, yourself in this case.

I aim to keep packaging bullshit to a minimum, because it is the least fun part
of Python. To that end, we should not use pkg_resources or anything like it. We
will not let setuptools zip everything into an "egg".  And we will never,
never, never attempt to use a namespace package for anything.

Rob Speer, 2010

