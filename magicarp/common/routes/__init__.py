import os

from flask import request, current_app, make_response
from simple_settings import settings

from magicarp import router, endpoint, signals

from magicarp.common import logic


class Ping(endpoint.BaseEndpoint):
    """Ping to get response: "pong".

    Used for health check.
    """
    url = '/ping'
    name = 'ping'

    def action(self):  # pylint: disable=arguments-differ
        resp = logic.get_pong(request.version)

        return resp


class UrlMap(endpoint.BaseEndpoint):
    """All urls available on api.
    """
    url = '/'
    name = 'url_map'

    def action(self):  # pylint: disable=arguments-differ
        func_list = logic.get_url_map(request.version)

        return func_list


class ShutDown(endpoint.BaseEndpoint):
    """ShutDown rouote, that terminates the server, expose it only for
    development and testing environment, unless you like server restarts.
    """
    url = '/shutdown'
    name = 'shutdown'

    methods = ['POST']

    def action(self):  # pylint: disable=arguments-differ
        func = request.environ.get('werkzeug.server.shutdown')

        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')

        # pylint: disable=protected-access
        signals.app_shutdown.send(current_app._get_current_object())
        # pylint: enable=protected-access

        func()

        return


class FavIcon(endpoint.BaseEndpoint):
    """Favicon, to prevent 500 when accessing api from a browser.
    """
    url = '/favicon.ico'
    name = 'favicon'

    response = None

    def action(self):  # pylint: disable=arguments-differ
        import base64
        resp = make_response(base64.b64decode(settings.FAVICON_CONTENT))

        resp.headers['content-type'] = 'image/vnd.microsoft.icon'

        return resp, 200


routes = [
    Ping(),
    UrlMap(),
    FavIcon(),
]


if os.environ.get("FLASK_ENV") == 'development':
    routes.append(ShutDown())

blueprint = router.Blueprint(
    __name__, namespace="/", routes=routes)
