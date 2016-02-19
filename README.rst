rfcs
====

The complete command-line tool for searching and viewing RFCs. It provides a
convenient interface for the API provided by `IETF <https://datatracker.ietf.org>`__

rfcs provides four major subcommands:
-  `rfcs search QUERY` - Search for RFCs matching a particular query. The
   default maximum number of results returned is 5.
-  `rfcs info RFC` - Get information on a particular RFC.
-  `rfcs text RFC` - View the RFC's text.
-  `rfcs url RFC --format FMT` - Get a url to view the RFC, in a format of
  `{text, html, pdf, bibtex}`.


Installation
------------

.. code:: bash

    pip install rfcs

