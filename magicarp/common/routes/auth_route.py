from magicarp import router, endpoint

from magicarp.common import logic, accept, output_schema


class AuthenticateUser(endpoint.BaseEndpoint):
    """Authorise user
    """
    url = '/'
    name = 'authenticate_user'

    methods = ["POST"]

    input_schema = accept.LoginPassword
    output_schema = output_schema.Credentials

    argument_name = 'payload'

    def action(self, payload):  # pylint: disable=arguments-differ
        client_id = payload.data['client_id'].data
        client_secret = payload.data['client_secret'].data

        body = logic.authorise_user(client_id, client_secret)

        return {
            "message": "Granted!",
            "access_token": body['access_token'],
            "token_type": body['token_type'],
            "expires_in": body['expires_in'],
        }


routes = [
    AuthenticateUser(),
]


blueprint = router.Blueprint(
    __name__, namespace="/auth", routes=routes)
