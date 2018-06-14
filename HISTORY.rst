1.3.0 (2018-06-XX)
~~~~~~~~~~~~~~~~~~

New Features:

 * input/output fields on schema that allow blanks will return None if None was
   provided (with possibly default to be set for such cases in the future)
 * automated error codes for incomming data validation are possible to override,
   change ERROR_CODEBOOK_ATTRIBUTES and ERROR_CODEBOOK_SCHEMA in your local
   settings
 * add blinker as dependency this will allow to add custom signals at will

1.2.0 (2018-06-07)
~~~~~~~~~~~~~~~~~~

New Features:

 * TimeField accepts many different formats: ie. 12m 15h or 12:00:30
 * Add common endpoint '/shutdown' it terminates server, is only available for
   development and it's primary use is in test cases
 * Add a way to override flask settings (not all of them yet, but it's trivial
   to add missing ones)
 * Bump version of flask to 1.0+
 * New flask allows starting app by pointing to app factory, this allows to
   drop unneeded file server.py
 * Add a way to override port and host when starting dev server

Bug Fixes:

 * DateField is correctly validated


1.1.0 (2018-05-30)
~~~~~~~~~~~~~~~~~~

New Features:

 * Add DateField and TimeField to existing fields on schema input/output
 * Make date parsing more robust by assuming duck-typing

1.0.11 (2018-05-11)
~~~~~~~~~~~~~~~~~~

Bug Fixes:

 * Fix input throwing exception if collection was in use on incomming data.
   (Regression from change for version 1.0.10)

1.0.10 (2018-05-09)
~~~~~~~~~~~~~~~~~~

Bug Fixes:

 * Fix fields on SchemaField (and in some cases on CollectionField) being shared
   via reference.

1.0.9 (2018-05-04)
~~~~~~~~~~~~~~~~~~

New Features:

 * reduce number of exception
 * add missing exception to be handled on default by fw
 * add a way to register additional exceptions in a fw

1.0.8 (2018-05-02)
~~~~~~~~~~~~~~~~~~

New Features:

 * increment versions of pytz and simple-settings

1.0.7 (2018-05-01)
~~~~~~~~~~~~~~~~~~

Version bump to force cache flush

1.0.6 (2018-05-01)
~~~~~~~~~~~~~~~~~~

Version bump to force cache flush

1.0.5 (2018-05-01)
~~~~~~~~~~~~~~~~~~

New Features:

* Common routes can be easily turned off
* Rename common subpackages/routes to be easily identifiable as non-core parts

1.0.4 (2018-05-01)
~~~~~~~~~~~~~~~~~~

Bug Fixes:

* Fix premature initialisation of flask app

1.0.3 (2018-05-01)
~~~~~~~~~~~~~~~~~~

Bug Fixes:

* Fix simple setting triggering too early to mess up import order (and cause
  in some cases cyclic-import)

1.0.2 (2018-05-01)
~~~~~~~~~~~~~~~~~~

Bug Fixes:

* Fix possible issue with cyclic import with tools<->exceptions

1.0.1 (2018-05-01)
~~~~~~~~~~~~~~~~~~

Bug Fixes:

* Fix possible issue with cyclic import on tools.

1.0.0 (2018-05-01)
~~~~~~~~~~~~~~~~~~

* First release on PyPI.
