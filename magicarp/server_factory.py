import logging

import flask

from simple_settings import settings

from . import exceptions, tools, response


# pylint: disable=too-many-branches
def create_app(
        first_setup=None, setup=None, register_error_handlers=None,
        register_loggers=None, before_routes=None, final_setup=None,
        register_extra_error_handlers=None, register_auth=None,
        register_routes=None, get_user_from_request=None):
    app = flask.Flask(settings.APP_NAME)

    app.config.from_object('magicarp.settings.flask_defaults')

    if first_setup:
        first_setup(app)

    if setup:
        setup(app)
    else:
        _setup(app)

    if register_auth:
        register_auth(app, flask.request)
    else:
        _register_auth(app, get_user_from_request)

    if register_error_handlers:
        register_error_handlers(app)
    else:
        _register_error_handlers(app)

    if register_extra_error_handlers:
        register_extra_error_handlers(app)

    if register_loggers:
        register_loggers(app)
    else:
        _register_loggers(app)

    if before_routes:
        before_routes(app)

    if register_routes:
        register_routes(app)
    else:
        _register_routes(app)

    if final_setup:
        final_setup(app)

    return app
# pylint: enable=too-many-branches


def _register_error_handlers(app):
    @app.errorhandler(exceptions.NotFoundError)
    def handle_missing_asset(err):  # pylint: disable=unused-variable
        """When we request asset but it's not found, ie. /user/uid/1/ should
        return user but there is no user for uid 1.
        """
        return response.error_response(err, 404)

    @app.errorhandler(exceptions.EndpointNotImplementedError)
    def handle_missing_implementation(err):  # pylint: disable=unused-variable
        """When endpoint was defined but it's content is empty.
        """
        app.logger.error(err, exc_info=True)

        return response.error_response(err, 500)

    @app.errorhandler(exceptions.BasePayloadError)
    def handle_malformed_input(err):  # pylint: disable=unused-variable
        """When incomming data is one way or another malformed, ie. missing
        key, wrong type or field that is not expected for given endpoint.
        """
        app.logger.error(err, exc_info=True)

        return response.error_response(err, 400)

    @app.errorhandler(exceptions.BaseValidationError)
    def handle_invalid_input(err):  # pylint: disable=unused-variable
        """When incomming data is valid in structure and thus has passed
        handle_malformed_input check, but is not avalid, ie. client_id
        has to be positive integer or email needs to have '@'
        """
        app.logger.error(err, exc_info=True)

        return response.error_response(err, 500)

    @app.errorhandler(exceptions.ResponseError)
    def handle_invalid_response(err):  # pylint: disable=unused-variable
        """When application handled incomming data, but according to definition
        of endpoint response data makes little to no sense. Usually happens
        when schema is stale or business logic has changed recently.
        """
        app.logger.error(err, exc_info=True)

        return response.error_response(err, 500)

    @app.errorhandler(Exception)
    def handle_other_magicarp_errors(err):  # pylint: disable=unused-variable
        """Handler for everything else that comes from magicarp and has no more
        specific error handling.
        """
        app.logger.error(err, exc_info=True)

        return response.error_response(err, 500)

    @app.errorhandler(Exception)
    def handle_remaining_errors(err):  # pylint: disable=unused-variable
        """Handler for everything else that is not defined above
        """
        app.logger.error(err, exc_info=True)

        return response.error_response(err, 500)

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


def _register_loggers(app):
    # add any other logger that may or may not exist in here
    loggers = [
        app.logger,
    ]

    # if logging enabled and env is test (nosetest/travis) or dev, use old
    # school logging (for production and similar use raven/rollbar)
    if settings.LOG_ENABLED and settings.LOCAL_LOGS_ENABLED:
        for some_logger in loggers:
            log_formatter = logging.Formatter(
                settings.LOGGING_FORMAT, settings.LOGGING_DATE_FORMAT)
            log_handler = logging.handlers.TimedRotatingFileHandler(
                filename=settings.LOG_PATH, when="midnight")
            log_handler.setFormatter(log_formatter)
            log_handler.setLevel(settings.LOG_LEVEL)

            some_logger.addHandler(log_handler)


def _register_auth(app, get_user_from_request):
    """Example how auth of user works, this one works with built-in auth
    namespace, override it to whatever auth endpoint is being used
    """
    if get_user_from_request is None:
        from magicarp.common import logic

        get_user_from_request = logic.retrieve_user_from_request

    @app.before_request
    def user_auth():  # pylint: disable=unused-variable
        flask.request.user = get_user_from_request(flask.request)


def _setup(app):
    """Hooks for actions performed before each request.
    """
    @app.before_first_request
    def init_rollbar():  # pylint: disable=unused-variable
        """This is only an example, rollbar is not hardcoded at all"""
        tools.logging.init_logging(app)

    # @app.before_request
    # def example_preprocessor():  # pylint: disable=unused-variable
    #     pass

    @app.after_request
    def after_request(resp):  # pylint: disable=unused-variable
        """If there is anything that api should do before ending request, add
        it in here for example you might have transactional backend that
        require commit or rollback at the end of each request.

        NOTE: if unhandled exception happens, this function is not going to be
        executed.
        """
        return resp

    app.debug = settings.DEBUG

    # custom encoder is set, update it's implementation if needed
    app.json_encoder = tools.helpers.JsonEncoder

    # custom request class in case you need more functionality than what Flask
    # offers
    app.request_class = tools.api_request.ApiRequest


def _register_routes(app):
    from magicarp import routing

    common_blueprints = []

    if settings.ROUTING_ADD_AUTH:
        from magicarp.common.routes import auth_route

        common_blueprints.append(auth_route.blueprint)

    if settings.ROUTING_ADD_COMMON:
        from magicarp.common import routes

        common_blueprints.append(routes.blueprint)

    routing.register_version(None, common_blueprints)

    # from now on every attempt to register or de-register version will cause
    # exception
    routing.lock()

    for (blueprint, url_prefix) in routing.get_normalised_blueprints():
        app.register_blueprint(blueprint, url_prefix=url_prefix)
