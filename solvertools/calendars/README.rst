.. _calendar:

`solvertools.calendars` -- universal calendar converter
=======================================================
This directory contains `pycalcal.py`, by Enrico Spinielli, which is in turn a
port of the Common Lisp module Calendrica by Robert F.  Anderson.

Its entire namespace is imported as `solvertools.calendars`.

pycalcal is distributed as literate code; I built it, left out most of the
machinery, and only included the resulting .py file and the .pdf of
documentation here. You can find the rest at
http://code.google.com/p/pycalcal/.

Here is its `extremely complete documentation`_. It is a freaking book.

.. _`extremely complete documentation`: http://manicsages.org/doc/_static/pycalcal.pdf

The usual way to use it is to convert everything to and from an internal calendar called
"fixed". Here are two relevant examples::

    >>> from solvertools import calendars
    >>> calendars.mayan_long_count_from_fixed(calendars.fixed_from_gregorian([2012, 1, 13]))
    [12, 19, 19, 0, 17]

    >>> calendars.gregorian_from_fixed(calendars.fixed_from_mayan_long_count([13, 0, 0, 0, 0]))
    [2012, 12, 21]

If you're curious about this thing -- and I hope you are -- "fixed" is defined
as the number of days since December 31, 1 BC (0000-12-31) in the proleptic
Gregorian calendar.

You could also call it the Julian Day number minus 1721425.
