.. _google:

The `solvertools.google` package
================================

Interfaces to Google APIs go here. So far, this includes just the Google
Language API.

The Google Language API
-----------------------
This is the Sages' interface to the Google Language API. The API itself is
documented at: http://code.google.com/apis/ajaxlanguage/documentation/.

*Do not call these functions in a loop*. You might get us banned from using the
API. Google's rule is that every request has to be initiated by a user.

.. automodule:: solvertools.google.language
    :members:

