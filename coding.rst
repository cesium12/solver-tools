.. _coding:

Coding style of solvertools
===========================

Python conventions
------------------
**No tabs.** You cannot use tab characters in Python code that you expect other
people to be able to edit. Have your text editor convert tabs to four spaces.

Write code that will work on Python 2.5 through 2.x, using `__future__` if
necessary for things like the `with` statement.

Use new-style classes so we know what type they are. That is, instead of
``class Foo:``, you should say ``class Foo(object):``.

Import statements should be absolute whenever possible, as in::

  from solvertools.something import stuff

Logging
-------
It's tempting to use print statements to debug your code, but that can get
confusing and annoying for people who use your code. Instead, what you want is
`logging`.

We've done the confusing part already: anything imported from within
`solvertools` will have a logging handler set up. Then all you need to is put
this at the top of your file::
    
    logger = logging.getLogger(__name__)

And then you can print status messages with lines such as:

    logger.info(message)
    logger.warn(message)

As a bonus, the logger will handle Unicode gracefully no matter what OS you're
on and what kind of string you throw at it, which is considerably better than
the `print` statement.

String handling
---------------
We're going to be working with text a *lot*, and in Python 2, this has one
major pitfall: the discrepancies between `str` strings and `unicode` strings.

Here's the rule of thumb: **all text is Unicode unless you're sure it's ASCII**.

Unicode string literals look like `u"text"`. You can define a Unicode
representation of a custom class with the `__unicode__` magic method (instead
of `__str__`). To read a text file, use this instead of `open`::

    codecs.open(filename, encoding='utf-8')

If you have some text, and you actually want to make sure it is plain ASCII,
run your Unicode through `solvertools.util.asciify`. This does what is likely
to be the right thing for Mystery Hunt: it replaces accented characters with
un-accented English letters, and removes anything else it can't handle. Most of
our wordlists (see :ref:`wordlists`) use this for storing and looking up words,
which means that you can feed them Unicode and they know what to do with it.

If you end up in a situation that neither `codecs` nor `asciify` can handle,
you can convert between Unicode strings and strings of raw bytes like this::

    someBytes = someString.encode('utf-8')
    someString = someBytes.decode('utf-8')

Numbers for characters
----------------------
You may end up writing code that represents text characters as numbers.

If the text is ASCII text, the valid numbers are between 32 and 127 (with
possibly the occasional 9 and 10 for tabs and linebreaks). If the text is
Unicode, a character number could be any 32-bit integer, although my system
only has one printable character numbered higher than a million and I'm not
sure why it's there.

No text is numbered from 0 to 255 unless it's in a hideously obsolete encoding.
There is no such thing as 8-bit ASCII. You may have thought there was, when you
grew up using DOS and Windows, but then you thought there was an Easter Bunny
too.

Directory structure
-------------------

The root of the package contains `setup.py`, enabling solvertools to be
installed using Setuptools or Distribute. See :ref:`install`.

The `.rst` files all over the place form our documentation, in ReStructuredText
format. These files should share a directory with whatever they're documenting. See :ref:`docs`.

`solvertools` contains all the Python code. Self-contained components can go in
their own subdirectories (make sure they have an `__init__.py` file, even if
it's empty).

`data` contains non-Python data files, as explained in :ref:`data`. There are
functions in `util.py` for working with these data files no matter where they
are in the repository.

We don't have any C extensions yet, but if we do, someone should figure out
where to put them and how to make them build.
