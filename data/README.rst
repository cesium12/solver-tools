.. _data:

The data directory
==================

If you keep data files in here, :ref:`solvertools.util` will be able to find them,
whether solvertools is an installed package or not.

The data directory is organized as follows:

`data/dict`
    Dictionary (wordlist) files that can be loaded with :ref:`solvertools.wordlist`.

`data/pickle`
    Pickled data structures. :ref:`solvertools.wordlist` and
    :ref:`solvertools.model.language_model` use these extensively so that they load
    quickly, without recomputing things from scratch.

`data/inputs`
    This directory should be empty in version control. The purpose of this
    directory is to contain very large files, such as Google N-gram files,
    that should not be checked in. Instead, :ref:`scripts` will read these files and
    produce smaller files that can be checked in.

`data/answers`
    A corpus of :ref:`past Mystery Hunt answers <answers>`, useful for testing.

Although the nature of what we do often requires large data files, please do
not check in extremely large files! Put them in the `data/inputs` directory and
find a way to turn them into a smaller representation. We should find a way to
share the `data/inputs` directory.

