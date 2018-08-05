import copy
import collections

from magicarp import exceptions, tools


class NotSet(object):
    def __str__(self):
        return "NotSet"

    def __repr__(self):
        return self.__str__()


class BaseField(object):
    description = ''
    parent = None
    is_instance = False

    def __init__(
            self, name, description=None, validators=None, allow_blank=True,
            parent=None):
        """Short description of what all those arguments stand for:

            name :: the only mandatory field, it basically tells how the field
                in question should be called, also it tells a schema to look
                for this name in coming payload, used as well for generation
                of error codes

            description :: human readable description of the field, used for
                auto generated api doc

            validators :: list of validators that should be applied, currently
                only data provided by the user is being validated, data prior
                to being validated is normalised towards certain values (for
                example boolean fields are either True or False, so validation
                is spared of type checking - with possible exception of
                handling None)

            allow_blank :: if given field allows None as data, this could
                be handled via validator (and still can be on top of that)
                but for certain systems null values are impossible (think of
                integer field receiving string value) and for such cases it's
                not a validation error it is payload error

            parent :: if object is part of bigger tree we can set a parent to
            it (helps with traversing)
        """
        self.name = name
        self.validators = [] if validators is None else validators
        self.allow_blank = allow_blank

        if description is not None:
            self.description = description

        if parent is not None:
            self.parent = parent

        self.data = NotSet()
        self.is_instance = True

    def confirm_argument_is_of_expected_shape(self, value):
        """Function checks whether argument value is among expected outcomes.

        For example only fields with allow_blank can have None as a value and
        collection fields probably want iterable.
        """
        if value is None and self.allow_blank is False:
            raise exceptions.InvalidPayloadError(
                "None/null is not acceptable value for a field")

    def make_new(self, parent):
        return self.__class__(
            name=self.name, description=self.description,
            validators=self.validators, allow_blank=self.allow_blank,
            parent=parent)

    def populate(self, value):
        self.confirm_argument_is_of_expected_shape(value)

        self.data = None if value is None else self.normalise(value)

    def normalise(self, value):
        return value

    def is_set(self):
        return not isinstance(self.data, NotSet)

    def get_canonical_string(self):
        ancestors = []
        parent = self.parent

        while parent:
            ancestors.insert(0, parent.name)

            parent = parent.parent

        ancestors.append(self.name)

        return '.'.join(ancestors)

    def as_dictionary(self, user=None):
        if not self.is_set():
            return None

        return self.data


class BaseSchemaField(BaseField):
    fields = ()

    def __init__(self, name, fields=None, **kwargs):
        if fields is not None:
            self.fields = fields

        super().__init__(name, **kwargs)

    def make_new(self, parent):
        return self.__class__(
            name=self.name, description=self.description,
            validators=self.validators, allow_blank=self.allow_blank,
            parent=parent, fields=self.fields)

    def get_field_by_name(self, name):
        for field in self.fields:
            if field.name != name:
                continue

            return field

    def confirm_argument_is_of_expected_shape(self, value):
        super().confirm_argument_is_of_expected_shape(value)

        if value is not None and not isinstance(value, (dict,)):
            raise exceptions.InvalidPayloadError(
                'Schema field can be populated only with dictinary like '
                'payload (ie. {{"my_value": true}}), got: {}'.format(value))

        if not self.fields:
            raise exceptions.InvalidPayloadError(
                "Invalid Schema definition, "
                "attribute fields is empty. Did you ask for empty schema?")

    def as_dictionary(self, user=None):
        if not self.is_set():
            return None

        tmp = {}

        for name, field in self.data.items():
            if not field.is_set():
                continue

            tmp[name] = field.as_dictionary(user=user)

        return tmp


class BaseCollectionField(BaseField):
    collection_type = None

    def __init__(self, name, collection_type=None, **kwargs):
        if collection_type is not None:
            self.collection_type = collection_type

        super().__init__(name, **kwargs)

    def make_new(self, parent):
        return self.__class__(
            name=self.name, description=self.description,
            validators=self.validators, allow_blank=self.allow_blank,
            parent=parent, collection_type=self.collection_type)

    def confirm_argument_is_of_expected_shape(self, value):
        super().confirm_argument_is_of_expected_shape(value)

        if value is not None and not isinstance(value, collections.Iterable):
            raise exceptions.InvalidPayloadError(
                "Collection field can be populated only with iterable "
                "payload (ie. list), got: {}".format(value))

        if self.collection_type is None:
            raise exceptions.InvalidPayloadError(
                "Invalid Collection definition, "
                "attribute collection_type not set. I have no idea how "
                "to populate your collection")

    def populate(self, value):
        self.confirm_argument_is_of_expected_shape(value)

        data = []

        for idx, val in enumerate(value):
            if self.collection_type.is_instance:
                instance = self.collection_type.make_new(self)
            else:
                instance = self.collection_type(
                    '{} - instance - {}'.format(self.name, idx), parent=self,
                    description='{} - instance - {}'.format(
                        self.description, idx))

            instance.populate(val)

            data.append(instance)

        self.data = data

    def as_dictionary(self, user=None):
        if not self.is_set():
            return None

        res = []

        for obj in self.data:
            if not obj.is_set():
                continue

            res.append(obj.as_dictionary(user=user))

        return res


class BaseBoolField(BaseField):
    def normalise(self, value):
        try:
            value = str(value).lower()

            if value in ('0', 'false', 'no', 'n'):
                return False
            elif value in ('1', 'true', 'yes', 'y'):
                return True

            raise ValueError
        except (TypeError, ValueError):
            raise exceptions.InvalidPayloadError(
                "Boolean field has to be truthy, one of: "
                "0, 1, true, false, yes, no, y, n. "
                "Case-insensitive where it applies, got: {}".format(value)
            )


class BaseDateTimeField(BaseField):
    def normalise(self, value):
        return tools.datetime_helpers.parse_into_datetime(value)


class BaseDateField(BaseField):
    def normalise(self, value):
        return tools.datetime_helpers.parse_into_date(value)


class BaseTimeField(BaseField):
    def normalise(self, value):
        return tools.datetime_helpers.parse_into_time(value)


class BaseStringField(BaseField):
    def normalise(self, value):
        return str(value)


class BaseIntegerField(BaseField):
    def normalise(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            raise exceptions.InvalidPayloadError(
                "Unable convert value to integer, got: {}".format(value))


class BaseDocumentField(BaseSchemaField):
    fields = (
        BaseStringField(
            "key", description="Any string like object"
        ),
        BaseStringField(
            "value", description="Any string like object"
        ),
    )

    def confirm_argument_is_of_expected_shape(self, value):
        super().confirm_argument_is_of_expected_shape(value)

        if not self.fields or len(self.fields) > 2:
            raise exceptions.InvalidPayloadError(
                "Invalid DocumentField definition, attribute fields is "
                "either empty or has more elements than two. "
                "Not sure how I should proceed.")

        if value is None:
            return

        if not isinstance(value, (dict, tuple, list)):
            raise exceptions.InvalidPayloadError(
                "DocuemntField can be populated only with dictinaries or "
                "lists/tuples each containing two elements "
                "got: {}".format(value))

    def as_dictionary(self, user=None):
        if not self.is_set():
            return None

        tmp = {}

        for field_key, field_value in self.data.items():
            tmp[field_key.as_dictionary(user=user)] = \
                field_value.as_dictionary(user=user)

        return tmp

    def normalise(self, value):
        # TODO: support dict-like structures
        if isinstance(value, dict):
            return value.items()

        return [(elm[0], elm[1]) for elm in value]

    def populate(self, value):
        self.confirm_argument_is_of_expected_shape(value)

        error_invalid_payload = []

        local_data = {}

        payload = self.normalise(copy.deepcopy(value))

        schema_key = self.fields[0]
        schema_value = self.fields[1]

        for value_key, value_value in payload:
            local_schema_key = schema_key.make_new(self)
            local_schema_value = schema_value.make_new(self)

            try:
                local_schema_value.populate(value_value)
            except exceptions.InvalidPayloadError as err:
                error_invalid_payload.append(
                    (local_schema_value.name, str(err)))

            try:
                local_schema_key.populate(value_key)
            except exceptions.InvalidPayloadError as err:
                error_invalid_payload.append(
                    (local_schema_value.name, str(err)))

            local_data[local_schema_key] = local_schema_value

        if error_invalid_payload:
            raise exceptions.PayloadError(
                error_invalid_payload=error_invalid_payload
            )

        self.data = local_data
