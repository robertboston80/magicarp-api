import json


class MagicarpApiException(Exception):
    pass


class RoutingConfigurationError(MagicarpApiException):
    """Exception happens when attemt to register endpoint fails. As such is
    never to be visible for a flask application.
    """
    pass


class EndpointNotImplementedError(MagicarpApiException):
    """When endpoint was defined but is missing action method (that actually
    does things)
    """
    pass


class NotFoundError(MagicarpApiException):
    """Used exclusively when requested asset is not found.
    """
    pass


class BaseDataError(MagicarpApiException):
    """Exception is able to aggregate any number of errors and then display
    them as a dictionary of problems.
    """
    def __init__(
            self, *args, error_required_field=None, error_invalid_payload=None,
            **kwargs):
        self.error_required_field = error_required_field
        self.error_invalid_payload = error_invalid_payload

        super().__init__(*args, **kwargs)

    def get_errors_as_dict(self):
        """Method returns errors in a format that could be easily consumed by
        other parts of the system.

        Ie.
        {
            "required_fields": "email, password, user.first_name",
            "payload_error": {
                "address": [
                    "Payload provided has to be iterable",
                ]
            }
        }
        """
        tmp = {}

        if self.error_required_field:
            tmp['required_fields'] = ", ".join(
                [tmp[0] for tmp in self.error_required_field])

        if self.error_invalid_payload:
            tmp['payload_error'] = {}

            for key, error in self.error_invalid_payload:
                if key not in tmp['payload_error']:
                    tmp['payload_error'][key] = []

                tmp['payload_error'][key].append(error)

        # NOTE: this is something that should be reviewed soon
        return tmp if tmp else str(super().__str__())

    def __str__(self):
        return json.dumps(self.get_errors_as_dict())


class BasePayloadError(BaseDataError):
    pass


class PayloadError(BasePayloadError):
    pass


class InvalidPayloadError(BasePayloadError):
    pass


class ResponseError(BaseDataError):
    pass


class BaseValidationError(MagicarpApiException):
    pass


class ValidationError(BaseValidationError):
    """Individual validation error, will be thrown typically from validator.
    """
    pass


class MultipleValidationError(BaseValidationError):
    """Aggregated errors from validatin, used to make a proper response in
    human readable form.
    """
    def __init__(self, schema, errors, *args, **kwargs):
        self.errors = errors
        self.schema = schema

        super().__init__(*args, **kwargs)

    def get_errors_as_dict(self):
        """Method returns errors in a format that could be easily consumed by
        other parts of the system.

        Ie.
        {
            'username': {
                'error_code': '40-20',
                'errors': [
                    'Username cannot be empty',
                ],
            },
            'address': {
                'error_code': '12-20',
                'errors': {
                    'city': {
                        'error_code': '25-13',
                        'errors': [
                            'City is not recognised',
                        ]
                    },
                    'post_code': {
                        'error_code': '25-16',
                        'errors': [
                            'Post code cannot be empty',
                        ],
                    },
                },
            },
        }
        """
        # this import is on purpose to avoid cyclic-imports
        from magicarp import tools

        tmp = {}

        for key, errors in self.errors.items():
            tmp[key] = {
                'error_code': tools.helpers.make_error_code(key, self.schema),
                'errors': errors,
            }

        return tmp

    def __str__(self):
        return json.dumps(self.get_errors_as_dict())
