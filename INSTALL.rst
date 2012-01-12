.. _install:

Installing Solvertools
======================

Prerequisites
-------------
Some pre-requisites to using Solvertools are:

- Software on your computer: Python (with development headers), NumPy, GCC, and SWIG
    - On Ubuntu, you can get all of these with: `sudo aptitude install build-essential python-dev python-numpy swig`
- Familiarity with using an interactive Python prompt (preferably IPython)
- Familiarity with the command line
- At least 4 GB or so of RAM

Installing the usual way
------------------------

If you don't already have the code, you should:

- Download the code (no, I'm not going to link to it here; if you're on the
  team you've got the link)
- Extract the code (Linux/Mac/UNIX command: `tar xvf solvertools-*.tar.bz2`)
- Make sure you have the dependencies
- `cd solver-tools`
- Run ``sudo python setup.py develop`` (or your system's equivalent).

Installing from Git
-------------------
If you use Git to get the code, you will be able to receive and commit updates
to it.

- Get access to git.manicsages.org from Jason Alonso (jalonso), if necessary
- `git clone git@git.manicsages.org:solver-tools.git`
- ``sudo python setup.py develop`` as normal

If that doesn't work
--------------------
If you can't run `setup.py` because you don't have a working C compiler, you
can try `setup-no-c.py`. You won't be able to grep entire wordlists within
Solvertools in this version.

If the setup doesn't work for some other reason, you can try just
setting your PYTHONPATH to the `solver-tools` directory.

