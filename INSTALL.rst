.. _install:

Installing Solvertools
======================

Prerequisites
-------------
Some pre-requisites to using Solvertools are:

- Software on your computer: Python (with development headers), NumPy, GCC, and
SWIG
    - On Ubuntu, you can get all of these with: `sudo aptitude install build-essential python-dev python-numpy swig`
- Familiarity with using an interactive Python prompt (preferably IPython)
- Familiarity with the command line
- At least 2 GB or so of RAM

Installing the usual way
------------------------

If you don't already have the code, you should:
- Download the code (no, I'm not going to link to it here; if you're on the
  team you've got the link)
- Download the data (unless your computer is fast enough to recompute it all!)
- Extract it
- Run ``sudo python setup.py develop`` (or your system's equivalent).

Installing from Git
-------------------
If you use Git to get the code, you will be able to receive and commit updates
to it.

- Get access to git.manicsages.org from Jason Alonso (jalonso), if necessary
- `git clone git@git.manicsages.org:solver-tools.git`
- ``sudo python setup.py develop`` as normal
The short answer on how to install this:

If that doesn't work
--------------------
If you can't run `setup.py` because you don't have a working C compiler, you
can try `setup-no-c.py`. Certain features will be missing.

If the setup doesn't work for some other reason, you can try just
setting your PYTHONPATH to the `solver-tools` directory.

