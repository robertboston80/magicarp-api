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

        local_fields = {}

        for field in self.fields:
            local_field = field.make_new(self)

            if field.name in value:
                try:
                    local_field.populate(value[field.name])
                except (
                        exceptions.InvalidPayloadError,
                        exceptions.ResponseError) as err:
                    error_invalid_payload.append((field.name, str(err)))

            local_fields[field.name] = local_field

        if error_invalid_payload:
            raise exceptions.ResponseError(
                error_invalid_payload=error_invalid_payload
            )

        self.data = local_fields


class IntegerField(base.BaseIntegerField, BaseOutputField):
    pass


class StringField(base.BaseStringField, BaseOutputField):
    pass


class DateTimeField(base.BaseDateTimeField, BaseOutputField):
    pass


class DateField(base.BaseDateField, BaseOutputField):
    pass


class TimeField(base.BaseTimeField, BaseOutputField):
    pass


class BoolField(base.BaseBoolField, BaseOutputField):
    pass


class CollectionField(base.BaseCollectionField, BaseOutputField):
    pass


class DocumentField(base.BaseDocumentField, BaseOutputField):
    pass
