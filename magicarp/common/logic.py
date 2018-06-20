import collections

from flask import current_app
from simple_settings import settings

from magicarp import storage
from magicarp.tools import auth_model


def get_pong(version=None):
    return 'pong - {}'.format(version) if version else 'pong'


def get_url_map(version=None):
    func_list = collections.OrderedDict()

    prefix = '/{}'.format(version) if version else ''

    for rule in current_app.url_map.iter_rules():
        if rule.endpoint == 'static':
            continue

        if not rule.rule.startswith(prefix):
            continue

        endpoint = current_app.view_functions[rule.endpoint]

        methods = endpoint.methods \
            if endpoint.methods else ["GET", "HEAD", "OPTIONS"]

        key = "({}) {}".format(",".join(methods), rule.rule)

        func_list[key] = endpoint.doc_short

    return func_list


def authorise_user(client_id, client_secret):
    # data = {
    #     'client_id': client_id,
    #     'client_secret': client_secret,
    # }
    #
    # url = 'https://some.service.com'
    #
    # response = requests.post(url, data=data)
    #
    # body = json.loads(response.text)

    body = {
        'access_token': 'yolo',
        'token_type': 'yolo',
        'expires_in': 3600,
    }

    payload = (
        client_id,
        body['token_type'],
    )

    storage.set_key(
        body['access_token'], payload, ttl=body['expires_in'])

    return {
        "message": "Granted!",
        "access_token": body['access_token'],
        "token_type": body['token_type'],
        "expires_in": body['expires_in'],
    }


def get_session_info(token_type, token):
    '''Validates a token for protected views'''
    if not all([token, token_type]):
        raise ValueError("Either token or token_type is empty")

    payload = storage.get_key(token)

    if not payload:
        raise ValueError("Unrecognised or expired user session")

    if payload[1] != token_type:
        raise ValueError("Unrecognised user session")

    return payload


def retrieve_user_from_request(request):
    """Converts header (if present) into authorised user. If no header present
    or backend is down, we should return unauthorised user.

    NOTE: throwing exception should be sorted out by view, decotare view with
    requirement to have certain view limited to authorised people with or
    without certain role.
    """
    auth_token = request.headers.get('Authorization')

    # if is set, we won't check authentication, this enables
    # us to test auth only on relevant endpoints and skip it on all others
    #
    # NOTE: there are two different parts to test in your api, one is with
    # static test User (header enables this), another is more granular approach
    # that allows you to retrieve 'real' test user from endpoint (and
    # test for example permissions and/or interactions between users)
    if auth_token == settings.TEST_USER and settings.TESTING is True:
        return auth_model.AuthorizedTestUser()
    elif not auth_token:
        return auth_model.UnauthorizedUser()

    try:
        token_type, token = auth_token.split(' ')

        client_id = get_session_info(token_type, token)
    except (AttributeError, ValueError):
        return auth_model.UnauthorizedUser()

    user = auth_model.AuthorizedUser(
        client_id, 'Client with token {}'.format(token),
        '{}@kyber.api.com'.format(client_id))

    return user
