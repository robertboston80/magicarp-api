from api import exceptions
from api import tools


class NotSet(object):
    def __str__(self):
        return "NotSet"

    def __repr__(self):
        return self.__str__()


class BaseField(object):
    is_collection = False
    is_schema = False

    # is required is set by certain settings on schema, not on field itself
    # purpose is that given schema might have very different required fields
    # depends in which context is being used (for example creating product and
    # updating product, name is required only when creating and cannot be
    # nullified when updating)
    is_required = False

    def __init__(self, description='', validators=None):
        self.description = description
        self.validators = validators
        self.data = NotSet()

    def populate(self, value, parents=None):
        self.data = self.normalise(value)

    def jsonify(self):
        return self.data

    def validate(self):
        """Validate given field, but only if was populated before.
        """
        if not self.is_set():
            raise exceptions.ApiException("Object validated too early")

        if not self.validators:
            return

        for validator in self.validators:
            if isinstance(validator, type):
                raise exceptions.ApiException(
                    "Validator has to be an instance, not type")

            validator(self.data)

    def normalise(self, value):
        return value

    def is_set(self):
        return not isinstance(self.data, NotSet)

    def __str__(self):
        return self.data.__str__()

    def __repr__(self):
        return self.data.__str__()

    def get_default_arguments(self):
        return {
            'description': self.description,
            'validators': self.validators,
        }


class CollectionField(BaseField):
    is_collection = True

    def __init__(self, field_type, *args, **kwargs):
        self.field_type = field_type

        super().__init__(*args, **kwargs)

    def normalise(self, value):
        if not isinstance(value, (list, set, tuple)):
            raise exceptions.InvalidPayloadError(
                "Collection field can be populated only with iterable "
                "payload (ie. list), got: {}".format(value))

        return list(value)

    def populate(self, value, parents=None):
        data = []

        for val in self.normalise(value):
            instance = self.get_new_instance()
            instance.populate(val, parents)

            data.append(instance)

        self.data = data

    def jsonify(self):
        return [obj.jsonify() for obj in self.data]

    def get_new_instance(self):
        return self.field_type.__class__(
            **self.field_type.get_default_arguments())

    def get_default_arguments(self):
        data = super().get_default_arguments()

        data.update({
            'field_type': self.field_type,
        })

        return data


class SchemaField(BaseField):
    is_schema = True

    def __init__(self, schema, *args, **kwargs):
        self.schema = schema

        super().__init__(*args, **kwargs)

    def normalise(self, value):
        if not isinstance(value, (dict,)):
            raise exceptions.InvalidPayloadError(
                'Schema field can be populated only with dictinary like '
                'payload (ie. {{"my_value": true}}), got: {}'.format(value))

        return value

    def populate(self, value, parents=None):
        data = self.schema()

        data.populate(self.normalise(value), parents)

        self.data = data

    def validate(self):
        """Validate given schema-field, but only if was populated before.
        """
        if not self.is_set():
            raise exceptions.ApiException("Object validated too early")

        self.data.validate()

    def jsonify(self):
        return self.data.as_dictionary()

    def get_default_arguments(self):
        data = super().get_default_arguments()

        data.update({
            'schema': self.schema,
        })

        return data


class BasePrimitiveField(BaseField):
    pass


class StringField(BasePrimitiveField):
    def normalise(self, value):
        return str(value)


class BoolField(BasePrimitiveField):
    def normalise(self, value):
        try:
            value = str(value)

            if value in (0, 'false', 'no'):
                return False
            elif value in (1, 'true', 'yes'):
                return True

            raise ValueError
        except (TypeError, ValueError):
            raise exceptions.InvalidPayloadError(
                "Boolean field has to be truthy, one of: "
                "0, 1, true, false, yes, no. "
                "Case-insensitive where it applies, got: {}".format(value)
            )


class DateField(BasePrimitiveField):
    def normalise(self, value):
        return tools.parse_into_datetime(value)


class IntegerField(BasePrimitiveField):
    def normalise(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            raise exceptions.InvalidPayloadError(
                "Integer field has to be numeric, got: {}".format(value)
            )
