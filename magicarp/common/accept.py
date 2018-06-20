from magicarp.schema import input_field as field
from magicarp.tools import validators


class LoginPassword(field.SchemaField):
    fields = (
        field.StringField(
            "client_id", description="Id of the client",
            validators=[validators.IsNonEmpty()], allow_blank=False),
        field.StringField(
            "client_secret", description="Secret of the client",
            validators=[validators.IsNonEmpty()], allow_blank=False),
    )

    required = (
        "client_id", "client_secret"
    )
