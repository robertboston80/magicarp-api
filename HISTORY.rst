1.6.0 (2018-08-XX)
~~~~~~~~~~~~~~~~~~

New Features:

 * New field `DocumentField`, behaves like a Mongo-like document, any key and
   any value will do, as long as they can be json serialised. (Note: there is
   already a mechanism to define how to serialise complex objects). Helps if
   response is document without fixed structure. Previously developer was
   forced to use raw response and had no support of framework with validation.

Breaking Compatibility:

 * default map endpoint started to use new schema Map (behaves the same)


1.5.0 (2018-07-18)
~~~~~~~~~~~~~~~~~~

New Features:

 * Renamed response to envelope to distinguish it from response as an
   interaction of webserver, in other words from now on each request,
   there will be a response in form of envelope that may or may not contain
   additional payload
 * Envelopes are classes, in order to make possible to override http_code they
   return.

Breaking Compatibility:

 * responses have been changed into envelopes


1.4.1 (2018-07-09)
~~~~~~~~~~~~~~~~~~

Bug Fixes:

 * Prevent critical error on initialisation of logging with default settings


1.4.0 (2018-07-08)
~~~~~~~~~~~~~~~~~~

New Features:

 * logging module follows implementation provided by flask, there are three
   variables on settings LOGGING, LOGGING_ADDITIONAL_HANDLERS and
   LOGGING_ADDITIONAL_LOGGERS, first one defines logging for the whole magicarp
   (there is `root` and `magicarp` as a base for logging), while
   LOGGING_ADDITIONAL_* allows to add loggers and/or handlers on top of that

Breaking Compatibility Changes:

 * logging was re-modeled and as such previous configuration won't work and
   will be ignored


1.3.0 (2018-06-20)
~~~~~~~~~~~~~~~~~~

New Features:

 * input/output fields on schema that allow blanks will return None if None was
   provided (with possibly default to be set for such cases in the future)
 * automated error codes for incoming data validation are possible to override,
   change ERROR_CODEBOOK_ATTRIBUTES and ERROR_CODEBOOK_SCHEMA in your local
   settings
 * add blinker as dependency to allow adding custom signals
 * create signals module that will allow emitting signals from magicarp
 * first magicarp signal is emitted, it's name is 'shutdown', is being
   send only in development mode when shutdown request was received
 * add implementation of persistent storage
 * add example implementation of /auth endpoint
 * add favicon to common endpoints
 * add a way to override authentication
 * add a way to override registering routes

Breaking Compatibility Changes:

 * hooks on magicarp server_factory has been changed from 'before_set_up' to
   'before_setup' and 'set_up' into 'setup'
 * renamed two functions on server factory to be slightly clearer, one went
   from 'before_setup' to 'first_setup' and the other changed from
   'after_setup' to 'final_setup'


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

 * Fix input throwing exception if collection was in use on incoming data.
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
* Rename common sub-packages/routes to be easily identifiable as non-core parts

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
