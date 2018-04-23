# encoding: utf8

import logging

import flask

from simple_settings import settings

# from flask import request, jsonify, got_request_exception

from magicarp import tools, exceptions


def create_app(before_set_up=None, before_routes=None, after_routes=None):
    app = flask.Flask(settings.APP_NAME)

    app.config.update(
        DEBUG=settings.DEBUG,
        TESTING=settings.TESTING,
    )

    if before_set_up:
        run_hook(app, before_set_up)

    set_up(app)

    # custom encoder is set, update it's implementation if needed
    app.json_encoder = tools.misc.JsonEncoder

    # custom request class in case you need more functionality than what Flask
    # offers out of box
    app.request_class = tools.api_request.ApiRequest

    if before_routes:
        run_hook(app, before_routes)

    register_routes(app)

    if after_routes:
        run_hook(app, after_routes)

    return app


def run_hook(app, callables):
    for func in callables:
        func(app)


def set_up(app):
    """Hooks for actions performed before each request.
    """
    @app.before_first_request
    def init_rollbar():  # pylint: disable=unused-variable
        if settings.ENABLE_ROLLBAR:
            tools.logging.init_rollbar(app)

    @app.before_request
    def before_request():  # pylint: disable=unused-variable
        """If there is anything that api should do before standard request
        processing add it in here. Caveat if this function returns anything
        standard view processing will be prevented.
        """
        user = tools.auth.retrieve_user_from_headers(flask.request.headers)

        # NOTE: add inactive version handling?
        # except exc.InactiveAPIVersion as err:
        #     return tools.responses.error_response(
        #       'Inactive API version', 404), ''
        # NOTE2: or perhaps method not implemented?
        # except exc.MethodNotImplemented as err:  # pragma: no cover
        #     # Note: 501 = Not Implemented
        #     response = tools.responses.error_response(err, 501)
        # except exc.MethodNotAllowed as err:
        #     return tools.responses.error_response(
        #         'Method {} not allowed for this request'.format(), 405),

        flask.request.user = user

    @app.after_request
    def after_request(response):  # pylint: disable=unused-variable
        """If there is anything that api should do before ending request, add
        it in here for example you might have transactional backend that
        require commit or rollback at the end of each request.

        NOTE: if unhandled exception happens, this function is not going to be
        executed.
        """
        return response

    @app.errorhandler(exceptions.BasePayloadError)
    def handle_malformed_input(err):  # pylint: disable=unused-variable
        """When incomming data is one way or another malformed, ie. missing
        key on input or is of wrong type.
        """
        app.logger.error(err, exc_info=True)

        return tools.response.error_response(err, 400)

    @app.errorhandler(exceptions.NotFoundError)
    def handle_missing_asset(err):  # pylint: disable=unused-variable
        """When incomming data is one way or another malformed, ie. missing
        key on input or is of wrong type.
        """
        return tools.response.error_response(err, 404)

    @app.errorhandler(exceptions.BaseValidationError)
    def handle_invalid_input(err):  # pylint: disable=unused-variable
        """When incomming data is not passing specification as described by
        spec, ie. email provided is not a valid email.
        """
        app.logger.error(err, exc_info=True)

        return tools.response.error_response(err, 500)

    @app.errorhandler(Exception)
    def handle_remaining_errors(err):  # pylint: disable=unused-variable
        """Handler for everything else that is not defined above
        """
        app.logger.error(err, exc_info=True)

        return tools.response.error_response(err, 500)

    app.debug = settings.DEBUG

    # add any other logger that may or may not exist in here
    loggers = [
        app.logger,
    ]

    # if logging enabled and env is test (nosetest/travis) or dev, use old
    # school logging (for production and similar use raven/rollbar)
    if settings.LOG_ENABLED and settings.ENV in (
            settings.ENV_DEV, settings.ENV_TEST):

        for some_logger in loggers:
            log_formatter = logging.Formatter(
                settings.LOGGING_FORMAT, settings.LOGGING_DATE_FORMAT)
            log_handler = logging.handlers.TimedRotatingFileHandler(
                filename=settings.LOG_PATH, when="midnight")
            log_handler.setFormatter(log_formatter)
            log_handler.setLevel(settings.LOG_LEVEL)

            some_logger.addHandler(log_handler)


def register_routes(app):
    from magicarp.routes import routing

    # from now on every attempt to register or de-register version will cause
    # exception
    routing.lock()

    for (blueprint, url_prefix) in routing.get_normalised_blueprints():
        app.register_blueprint(blueprint, url_prefix=url_prefix)
