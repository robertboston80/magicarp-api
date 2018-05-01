import flask


class Undefined(object):
    """Tribute to javascript
    """
    pass


def _base_response(response_type, data):
    response = {
        'success': True,
        'type': response_type
    }

    if data is not Undefined:
        response['data'] = data

    return response


def _wrap(response, code):
    return flask.jsonify(response), code


def read_response(data=Undefined, code=200):
    '''Default get response'''
    return _wrap(_base_response('read', data), code)


def update_response(data=Undefined, code=202):
    '''Default update successful response'''
    return _wrap(_base_response('update', data), code)


def create_response(data=Undefined, code=201):
    '''Default creation successful response'''
    return _wrap(_base_response('create', data), code)


def delete_response(data=Undefined, code=202):
    '''Default deleteion successful response'''
    return _wrap(_base_response('delete', data), code)


def raw_response(data=None, code=200):
    """Used for edge cases, when we cannot for some reason send standardised
    output
    """
    return _wrap(data, code)


def error_response(err, code=500):
    '''Default error response

    Note: error response returns message (sometimes stack trace) under a
    keyword 'response', this is to maintain same, simple dictionary that is
    being returned from views.
    '''
    response = _base_response('error', Undefined)

    response['success'] = False

    if hasattr(err, 'get_errors_as_dict'):
        response['data'] = err.get_errors_as_dict()
    else:
        response['data'] = str(err)

    return _wrap(response, code)
