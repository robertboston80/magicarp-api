import url2vapi

from flask import Request


class ApiRequest(Request):
    '''Extended flask request, notable change: it is version aware.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.api_request = url2vapi.split(
            self.url, pattern="<version:double>")

    @property
    def version(self):
        return self.api_request.version['value'] \
            if self.api_request.version else None

    @property
    def remainder(self):
        return self.api_request.remainder

    def __str__(self):
        return '<ApiRequest(version={}, url={})>'.format(
            self.api_request.version, self.api_request.remainder)

    def request_is_versioned(self, path):
        '''Determines whether the request URI is versioned'''
        return self.version is not None

    @property
    def person(self):
        return {
            'id': self.user.uid,
            'username': self.user.name,
            'email': self.user.email,
        }

    @property
    def rollbar_person(self):  # pragma: no cover
        """Rollbar integration.

        If rollbar is not in use, ignore.
        """
        # as per rollbar requirements:
        # id - required
        # username and email are optional but have to be strings
        #
        # NOTE: any other value would be ignored, hence this wrapper that make
        # sure that we can provide more data about person, yet rollbar will be
        # exposed to what it accepts
        return {
            'id': self.person['uid'],
            'username': self.person['username'],
            'email': self.person['email'],
        }
