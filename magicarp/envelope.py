import flask


class Undefined(object):
    """Tribute to javascript
    """
    pass


def _base(envelope_type, data, success=True):
    dct = {
        'success': success,
        'envelope_type': envelope_type,
    }

    if data is not Undefined:
        dct['content'] = data

    return dct


class BaseEnvelope(object):
    def __init__(self, code=200):
        self.code = code

    def wrap(self, payload, code):
        return flask.jsonify(payload), code


class Read(BaseEnvelope):
    '''Default read (GET, OPTION) envelope'''

    def __call__(self, data=Undefined):
        return self.wrap(_base('read', data), self.code)


class Update(BaseEnvelope):
    '''Default update (PUT, PATCH) envelope'''

    def __init__(self, code=202):
        super().__init__(code)

    def __call__(self, data=Undefined):
        return self.wrap(_base('update', data), self.code)


class Create(BaseEnvelope):
    '''Default create (POST) envelope'''

    def __init__(self, code=201):
        super().__init__(code)

    def __call__(self, data=Undefined):
        return self.wrap(_base('create', data), self.code)


class Delete(BaseEnvelope):
    '''Default delete (DELETE) envelope'''

    def __init__(self, code=202):
        super().__init__(code)

    def __call__(self, data=Undefined):
        return self.wrap(_base('delete', data), self.code)


class RawJson(BaseEnvelope):
    '''Used to return jsonified data as-is with given http code
    '''

    def __call__(self, data=Undefined):
        return self.wrap(data, self.code)


class Raw(BaseEnvelope):
    '''Used to return data as-is (literally) with given http code
    '''

    def __call__(self, data=Undefined):
        return (
            None if data is Undefined else data,
            self.code
        )


class Error(BaseEnvelope):
    '''Default error envelope

    This envelope not only will create itself, but it's content will be
    populated with human readable exception message if exception supports it.
    '''

    def __init__(self, code=500):
        super().__init__(code)

    def __call__(self, err):
        payload = _base('error', Undefined, False)

        if hasattr(err, 'get_errors'):
            payload['content'] = err.get_errors()
        else:
            payload['content'] = str(err)

        return self.wrap(payload, self.code)
