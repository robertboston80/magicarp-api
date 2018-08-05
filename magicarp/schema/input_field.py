import collections
import copy

from simple_settings import settings

from magicarp import exceptions, tools
from magicarp.schema import base


class BaseInputField(object):
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


class SchemaField(base.BaseSchemaField, BaseInputField):
    required = None
    not_required = None

    # if you need to have some sort of validator on schema, let say given date
    # is correct when given float on another field is less than 100$ define it
    # as follows:
    # schema_validators = [(
    #     ('price', 'end_date'),
    #     lambda x, y: x > 100 and end_date < '2018-01-01'
    # ),]
    #
    # NOTE: lambda can be replaced with any sort of function or callable,
    # expected return is true/false
    schema_validators = tuple()

    def _get_not_required(self):
        if self.not_required is None:
            return []

        if not isinstance(self.not_required, collections.Iterable):
            raise ValueError("Optional fields need to be iterable")

        return self.not_required

    def _get_required(self):
        if self.required is None:
            return []

        if not isinstance(self.required, collections.Iterable):
            raise ValueError("Required fields are not iterable")

        return self.required

    def _prefix_with(self, prefix, values):
        return ["{}.{}".format(prefix, value) for value in values]

    def collect_required_fields(self):
        if self.fields is None:
            return []

        required = self._get_required()

        for field in self.fields:
            if isinstance(field, base.BaseSchemaField):
                required += self._prefix_with(
                    field.name, field.collect_required_fields())

            elif isinstance(field, base.BaseCollectionField) and \
                    isinstance(field.collection_type, base.BaseSchemaField):

                if field.collection_type.is_instance:
                    instance = field.collection_type.make_new(self)
                else:
                    instance = field.collection_type(
                        '{} - {}'.format(
                            field.name, field.collection_type), parent=self)

                required += self._prefix_with(
                    field.name, instance.collect_required_fields())

            else:
                continue

        for opt_value in self._get_not_required():
            if opt_value not in required:
                raise ValueError(
                    "Optional value {} not present in required fields: {}, "
                    "overriding has no effect. Stale schema?".format(
                        opt_value, ", ".join(required)))

            required.remove(opt_value)

        # TODO: we need to verify if collect_required_fields() mentions fields
        # that do exist, we can specify that given field is required using dot
        # notation, where each dot is a parent object ie:
        #
        # user.address.post_code.number
        #
        # if post_code changes a structure (by not having number anymore) we
        # should get validation error in here

        required = list(set(required))

        required.sort()

        required = tools.helpers.build_tree(required)

        return required

    def populate(self, value):
        self.confirm_argument_is_of_expected_shape(value)

        error_required_field = []
        error_invalid_payload = []

        required = self.collect_required_fields()

        # TODO: if error happens FW needs to return more detailed exceptions,
        # for example we can say not only that given field is missing but that
        # it's the schema with 3 required sub-field, same with collections, not
        # only that collection has to be list but also that the list has to be
        # of integers

        local_fields = {}

        payload = copy.deepcopy(value)

        for field in self.fields:
            if field.name not in payload and field.name in required:
                error_required_field.append((
                    field.get_canonical_string(), "Missing required field"))

            local_field = field.make_new(self)

            if field.name in payload:
                subpayload = payload.pop(field.name)

                try:
                    local_field.populate(subpayload)
                except exceptions.InvalidPayloadError as err:
                    error_invalid_payload.append((field.name, str(err)))

            local_fields[local_field.name] = local_field

        if payload and settings.EXCEPTION_ON_UNRECOGNISED_INPUT:
            error_invalid_payload.append((
                "payload",
                "Payload specifies fields that do not exist: {}".format(
                    ", ".join(payload.keys()))))

        if error_required_field or error_invalid_payload:
            raise exceptions.PayloadError(
                error_required_field=error_required_field,
                error_invalid_payload=error_invalid_payload
            )

        self.data = local_fields

    def validate(self):
        errors = {}

        for name, field in self.data.items():
            if not field.is_set():
                continue

            try:
                field.validate()
            except exceptions.BaseValidationError as err:
                if field.name not in errors:
                    errors[name] = []

                errors[name].append(str(err))

        for field_names, validator, message in self.schema_validators:
            fields = [
                self.data[name] for name in field_names
            ]

            is_valid = validator(*fields)

            if not is_valid:
                key = ','.join(field_names)

                if key not in errors:
                    errors[key] = []

                errors[key].append(
                    "Invalid value" if message is None else message)

        if errors:
            raise exceptions.MultipleValidationError(self.name, errors)


class IntegerField(base.BaseIntegerField, BaseInputField):
    pass


class StringField(base.BaseStringField, BaseInputField):
    pass


class DateTimeField(base.BaseDateTimeField, BaseInputField):
    pass


class DateField(base.BaseDateField, BaseInputField):
    pass


class TimeField(base.BaseTimeField, BaseInputField):
    pass


class BoolField(base.BaseBoolField, BaseInputField):
    pass


class CollectionField(base.BaseCollectionField, BaseInputField):
    pass


class DocumentField(BaseInputField):
    pass
