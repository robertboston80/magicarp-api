from flask import request

from . import exceptions, envelope, tools


class BaseEndpoint(object):
    short_description = None
    long_description = None

    # if set to None, will default to GET, HEAD and OPTIONS
    methods = None

    # if set, given object will be constructed on entry
    input_schema = None

    # if set, given object will be returned
    output_schema = None

    # each response is an envelope that may or may not contain extra data, it's
    # sort of saying that magicarp kept composure in case of error or error is
    # totally uncontrolled so that even envelope could not be created, if we
    # set it to None we will disable it (however flask error will follow,
    # unless we keep in mind that not only response but http_response_code is
    # expected by flask), if we set it to envelope.Raw() we will return data
    # as-is
    envelope = envelope.Read()

    # if set given permission will be checked before attempting to call
    # endpoint
    permissions = ()

    argument_name = 'input_schema'

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

    def action(self, *args, **kwargs):
        raise exceptions.EndpointNotImplementedError(
            "Endpoint do not implement action")

    @property
    def request(self):
        return request

    def parse_input(self, payload):
        # pylint: disable=not-callable
        accepted_instance = self.input_schema(
            self.input_schema.__name__.lower())
        # pylint: enable=not-callable

        accepted_instance.populate(payload)

        # if invalidated throw exception that will be automatically handled
        # by framework
        accepted_instance.validate()

        return {
            self.argument_name: accepted_instance,
        }

    def parse_output(self, result):
        # pylint: disable=not-callable
        expected_output = self.output_schema(
            self.output_schema.__name__.lower())
        # pylint: enable=not-callable

        expected_output.populate(result)

        return expected_output

    def get_payload(self, request_):
        if request_.headers.get('Content-Type') == 'application/json':
            return request.get_json()

        return tools.helpers.to_json(request_.values)

    def __call__(self, *args, **kwargs):
        payload = self.get_payload(request)

        if self.input_schema:
            kwargs.update(self.parse_input(payload))

        result = self.action(*args, **kwargs)

        # if request.headers.get('X-Docs'):
        #     result = view.__doc__, 200
        # else:
        #     result = self.action(*args, **kwargs)

        if self.output_schema:
            result = self.parse_output(result)

        # this will trick to run callable as function and not method
        if self.envelope:
            return self.envelope(result)

        return result
