import json


class MagicarpApiException(Exception):
    pass


class DuplicateRouteError(MagicarpApiException):
    pass


class ApiRuntimeError(MagicarpApiException):
    pass


class ApiValueError(MagicarpApiException):
    pass


class BasePayloadError(MagicarpApiException):
    pass


class NotFoundError(MagicarpApiException):
    """Used exclusively when requested asset is not found.
    """
    pass


class PayloadError(BasePayloadError):
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

            print(self.error_invalid_payload)

            for key, error in self.error_invalid_payload:
                if key not in tmp['payload_error']:
                    tmp['payload_error'][key] = []

                tmp['payload_error'][key].append(error)

        return tmp

    def __str__(self):
        return json.dumps(self.get_errors_as_dict())


class InvalidPayloadError(BasePayloadError):
    pass


class MissingPayloadError(BasePayloadError):
    pass


class BaseResponseError(MagicarpApiException):
    pass


class ResponseConversionError(BaseResponseError):
    pass


class ResponseCriticalError(BaseResponseError):
    pass


class BaseBusinessLogicException(MagicarpApiException):
    pass


class BusinessLogicException(MagicarpApiException):
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
        from api.tools import misc

        tmp = {}

        for key, errors in self.errors.items():
            tmp[key] = {
                'error_code': misc.make_error_code(key, self.schema),
                'errors': errors,
            }

        return tmp

    def __str__(self):
        return json.dumps(self.get_errors_as_dict())
