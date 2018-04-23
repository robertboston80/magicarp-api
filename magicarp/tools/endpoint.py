from flask import request

from magicarp import exceptions, tools


class BaseEndpoint(object):
    short_description = None
    long_description = None

    # if set to None, will default to GET, HEAD and OPTIONS
    methods = None

    # if set, given object will be constructed on entry
    input_schema = None

    # if set, given object will be returned
    output_schema = None

    # which response to use, defaults to (success, 200)
    response = tools.response.read_response

    # if set given permission will be checked before attempting to call
    # endpoint
    permissions = ()

    argument_name = 'payload'

    # TODO: make sure that url is prefixed with forward slash
    # url = '/'

    @classmethod
    def name(cls):
        return cls.__name__

    @property
    def doc_short(self):
        if self.short_description:
            return self.short_description

        elif self.__doc__:
            return self.__doc__.split('\n')[0].strip()

        return "[Docstring not set nor attribute short_description]"

    @property
    def doc_long(self):
        if self.long_description:
            return self.long_description

        elif self.__doc__:
            return self.__doc__

        return "[Docstring not set nor attribute long_description]"

    def parse_output(self, response):
        return response

    def action(self, *args, **kwargs):
        raise exceptions.ApiRuntimeError("Endpoint do not implement action")

    @property
    def request(self):
        return request

    def __call__(self, *args, **kwargs):
        if request.headers.get('Content-Type') == 'application/json':
            payload = request.get_json()
        else:
            payload = tools.misc.to_json(request.values)

        if self.input_schema:
            # pylint: disable=not-callable
            accepted_instance = self.input_schema(
                self.input_schema.__name__.lower())
            # pylint: enable=not-callable

            accepted_instance.populate(payload)

            # if invalidated throw exception that will be automatically handled
            # by framework
            accepted_instance.validate()

            kwargs[self.argument_name] = accepted_instance

        result = self.action(*args, **kwargs)

        # if request.headers.get('X-Docs'):
        #     response = view.__doc__, 200
        # else:
        #     response = view(**data)

        if self.output_schema:
            # pylint: disable=not-callable
            expected_response = self.output_schema(
                self.output_schema.__name__.lower())
            # pylint: enable=not-callable

            try:
                expected_response.populate(result)
            except exceptions.ApiException as err:
                raise exceptions.ResponseCriticalError(
                    "Result from endpoint do not fulfil contract. "
                    "Original error: " + str(err))

            result = expected_response

        # this will trick to run callable as function and not method
        return self.response.__func__(result)
