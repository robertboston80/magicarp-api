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
