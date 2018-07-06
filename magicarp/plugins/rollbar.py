import os
import sys

import flask

try:
    import rollbar
    import rollbar.contrib.flask
except ImportError:
    pass

from simple_settings import settings


def init(app):  # pragma: no cover
    if not settings.ROLLBAR_API_KEY:
        raise ValueError("ROLLBAR_API_KEY not set")

    # NOTE: this will catch only unhandled exceptions, handled
    # exceptions are going through proper exception handling as defined
    # in server_tools
    flask.got_request_exception.connect(
        rollbar.contrib.flask.report_exception, app)

    # send exception from `app` to rollbar, using flask's signal
    # system.

    rollbar.init(
        # access token for the demo app -> https://rollbar.com/demo
        settings.ROLLBAR_API_KEY,
        # environment name
        settings.ROLLBAR_ENV,
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False
    )


def send_message(message, log_level='warning'):  # pragma: no cover
    rollbar.report_message(message, log_level)


def sys_info(**kwargs):  # pragma: no cover
    rollbar.report_exc_info(sys.exc_info(), **kwargs)
