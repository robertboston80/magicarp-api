"""
Auth
====

Authentication related set of functions.
"""
import json

from simple_settings import settings

from . import cache, misc, auth_model


def validate_token(user_uid, token):
    '''Validates a token for protected views'''
    if not all([token, user_uid]):
        raise ValueError("Either token or uid is empty")

    key = misc.generate_session_key(user_uid)
    response = cache.get_key(key)

    if not response:
        raise ValueError("User session does not exist")

    data = json.loads(response)

    if not data['token'] == token:
        raise ValueError("Invalid token")


def get_user_via_auth_token(auth_token):
    if not auth_token:
        return auth_model.UnauthorizedUser()

    try:
        user_uid, token = auth_token.split(':')

        validate_token(user_uid, token)
    except (AttributeError, ValueError):
        return auth_model.UnauthorizedUser()

    auth_engine = misc.get_auth_engine()

    user = auth_engine.get_user_by_uid(uid=user_uid)

    return user


def retrieve_user_from_headers(headers):
    """Converts header (if present) into authorised user. If no header present
    or backend is down, we should return unauthorised user.

    NOTE: throwing exception should be sorted out by view, decotare view with
    requirement to have certain view limited to authorised people with or
    without certain role.
    """
    auth_token = headers.get('X-Auth-Token', '')

    # if Api-Auto-Auth is set, we won't check authentication, this enables
    # us to test auth only on relevant endpoints and skip it on all others
    #
    # NOTE: there are two different layers of testing your api, one is with
    # static test User (header enables this) that is always returning same
    # person with certain default settings, another is more granular approach
    # that allows you to retrieve test user from endpoint of your choice (and
    # test for example permissions and/or interactions between users)
    if settings.ENV == settings.ENV_TEST and \
            'Enable-Static-Test-User' in headers:
        return auth_model.AuthorizedTestUser()
    elif not auth_token:
        return auth_model.UnauthorizedUser()

    return get_user_via_auth_token(auth_token)
