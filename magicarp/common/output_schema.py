from magicarp.schema import output_field as field

"""Module holds some (possibly) common responses, to be used as point of
reference.
"""


class ResourceCreated(field.SchemaField):
    fields = (
        field.StringField(
            "message",
            description="Human readable message from server what was created"),
        field.StringField(
            "uid", description="Unique asset identifier"),
        field.StringField(
            "url", description="Url to read-access for this object"),
    )

    @property
    def description(self):
        return (
            "Generic reply from api-server, "
            "whenever resource was created successfully.")


class ResourceUpdated(field.SchemaField):
    fields = (
        field.StringField(
            "message",
            description="Human readable message from server what was created"),
        field.StringField(
            "url",
            description="Optional url to read-access for this object"),
    )

    @property
    def description(self):
        return (
            "Generic reply from api-server, "
            "whenever resource was updated successfully.")


class ListResponse(field.CollectionField):
    collection_type = field.StringField

    @property
    def description(self):
        return (
            "Reply from server that replies with any kind of collection.")


class Credentials(field.SchemaField):
    fields = (
        field.StringField(
            "message", description="Descriptive message of what has happened"),
        field.StringField(
            "access_token", description="Generated access token"),
        field.StringField(
            "token_type", description="What type of token is it"),
        field.IntegerField(
            "expires_in",
            description="How much time till it has to be renewed"),
    )


class Map(field.DocumentField):
    fields = (
        field.StringField(
            "key", description="KEY"
        ),
        field.StringField(
            "value", description="VALUE"
        ),
    )
