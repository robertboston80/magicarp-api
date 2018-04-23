# -*- coding: utf8 -*-
"""
Logging
=======

Module is responsible for various operations related to logging, some functions
operate with rollbar (and because rollbar itself is an option, they might be
dormant), others are working with standard logging that is available in python
(and a way flask/simple settings interact with it).
"""

import os
import sys

import flask

from simple_settings import settings

if settings.ENABLE_ROLLBAR:
    import rollbar
    import rollbar.contrib.flask

    def init_rollbar(app):  # pragma: no cover
        # NOTE: this will catch only unhandled exceptions, handled
        # exceptions are going through proper exception handling as defined
        # in server_tools

        flask.got_request_exception.connect(
            rollbar.contrib.flask.report_exception, app)

        if settings.ROLLBAR_API_KEY is None:
            raise ValueError("ROLLBAR_API_KEY not set")

        # send exception from `app` to rollbar, using flask's signal
        # system.

        rollbar.init(
            # access token for the demo app: https://rollbar.com/demo
            settings.ROLLBAR_API_KEY,
            # environment name
            settings.ENV,
            # server root directory, makes tracebacks prettier
            root=os.path.dirname(os.path.realpath(__file__)),
            # flask already sets up logging
            allow_logging_basic_config=False
        )

    def rollbar_send_message(message, log_level='warning'):  # pragma: no cover
        rollbar.report_message(message, log_level)

    def rollbar_sys_info(**kwargs):  # pragma: no cover
        rollbar.report_exc_info(sys.exc_info(), **kwargs)

else:
    def init_rollbar(app):  # pragma: no cover
        pass

    def rollbar_send_message(message, log_level='warning'):  # pragma: no cover
        pass

    def rollbar_sys_info(**kwargs):  # pragma: no cover
        pass
