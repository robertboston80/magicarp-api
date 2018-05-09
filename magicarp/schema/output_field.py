from magicarp import exceptions
from magicarp.schema import base


class BaseOutputField(object):
    pass


class SchemaField(base.BaseSchemaField, BaseOutputField):
    def populate(self, value):
        payload = self.normalise(value)

        error_invalid_payload = []

        for field in self.fields:
            if field.name not in payload:
                continue

            field.parent = self

            sub_payload = payload[field.name]

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

    def get_normal(self, value):
        try:
            return super().get_normal(value)
        except exceptions.InvalidPayloadError as err:
            raise exceptions.ResponseError(err)


class IntegerField(base.BaseIntegerField, BaseOutputField):
    def get_normal(self, value):
        try:
            return super().get_normal(value)
        except exceptions.InvalidPayloadError as err:
            raise exceptions.ResponseError(err)


class StringField(base.BaseStringField, BaseOutputField):
    pass


class DateField(base.BaseDateField, BaseOutputField):
    pass


class BoolField(base.BaseBoolField, BaseOutputField):
    def get_normal(self, value):
        try:
            return super().get_normal(value)
        except exceptions.InvalidPayloadError as err:
            raise exceptions.ResponseError(err)


class CollectionField(base.BaseCollectionField, BaseOutputField):
    def get_normal(self, value):
        try:
            return super().get_normal(value)
        except exceptions.InvalidPayloadError as err:
            raise exceptions.ResponseError(err)
