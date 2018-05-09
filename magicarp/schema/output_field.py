from magicarp import exceptions
from magicarp.schema import base


class BaseOutputField(object):
    def normalise(self, value):
        try:
            return super().normalise(value)
        except exceptions.InvalidPayloadError as err:
            raise exceptions.ResponseError(err)

    def confirm_argument_is_of_expected_shape(self, value):
        try:
            super().confirm_argument_is_of_expected_shape(value)
        except exceptions.InvalidPayloadError as err:
            raise exceptions.ResponseError(err)


class SchemaField(base.BaseSchemaField, BaseOutputField):
    def populate(self, value):
        self.confirm_argument_is_of_expected_shape(value)

        error_invalid_payload = []

        for field in self.fields:
            if field.name not in value:
                continue

            field.parent = self

            sub_payload = value[field.name]

            try:
                field.populate(sub_payload)
            except (
                    exceptions.InvalidPayloadError,
                    exceptions.ResponseError) as err:
                error_invalid_payload.append((field.name, str(err)))

        if error_invalid_payload:
            raise exceptions.ResponseError(
                error_invalid_payload=error_invalid_payload
            )

        self.data = self.fields


class IntegerField(base.BaseIntegerField, BaseOutputField):
    pass


class StringField(base.BaseStringField, BaseOutputField):
    pass


class DateField(base.BaseDateField, BaseOutputField):
    pass


class BoolField(base.BaseBoolField, BaseOutputField):
    pass


class CollectionField(base.BaseCollectionField, BaseOutputField):
    pass
