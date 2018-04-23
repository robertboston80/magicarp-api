from flask import request

from magicarp import tools, router
from magicarp.misc import logic


class Ping(tools.endpoint.BaseEndpoint):
    """Ping to get response: "pong".

    Used for health check.
    """
    url = '/ping'
    name = 'ping'

    def action(self):  # pylint: disable=arguments-differ
        response = logic.get_pong(request.version)

        return response


class UrlMap(tools.endpoint.BaseEndpoint):
    """All urls available on api.
    """
    url = '/'
    name = 'url_map'

    def action(self):  # pylint: disable=arguments-differ
        func_list = logic.get_url_map(request.version)

        return func_list


blueprint = router.Blueprint(
    __name__, namespace="/", routes=[
        Ping(),
        UrlMap(),
    ])
