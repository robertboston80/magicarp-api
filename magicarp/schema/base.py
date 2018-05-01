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

    def __init__(
            self, name, description=None, validators=None, allow_blank=True):
        """Short description of what all those arguments stand for:

            name :: the only mandatory field, it basically tells how the field
                in question should be called, also it tells a schema to look
                for this name in comming payload, used as well for generation
                of error codes

            description :: human readable description of the field, used for
                auto generated api doc

            validataors :: list of validators that should be applied, currently
                only data provided by the user is being validated, data prior
                to being validated is normalised towards certain values (for
                example boolean fields are either True or False, so validation
                is spared of type checking - with possible exception of
                handling None)

            allow_blank :: if given field allows None as input data, this can
                be handled via validator but for certain systems null values
                are impossible and in such cases it's not a validation error


        """
        self.name = name
        self.validators = [] if validators is None else validators
        self.allow_blank = allow_blank

        if description is not None:
            self.description = description

        self.data = NotSet()

    def get_normal(self, value):
        return value

    def normalise(self, value):
        if value is None:
            if self.allow_blank is True:
                return None
            else:
                raise exceptions.InvalidPayloadError(
                    "None/null is not possible for the field")

        return self.get_normal(value)

    def populate(self, value):
        self.data = self.normalise(value)

    def is_set(self):
        return not isinstance(self.data, NotSet)

    def as_kwarg(self):
        return self.data

    def get_canonical_string(self):
        ancestors = []
        parent = self.parent

        while parent:
            ancestors.insert(0, parent.name)

            parent = parent.parent

        ancestors.append(self.name)

        return '.'.join(ancestors)

    def as_json(self, user):
        if not self.is_set():
            return None

        return self.data


class BaseSchemaField(BaseField):
    fields = ()

    def __init__(self, name, fields=None, **kwargs):
        if fields is not None:
            self.fields = fields

        super().__init__(name, **kwargs)

    def get_field_by_name(self, name):
        for field in self.fields:
            if field.name != name:
                continue

            return field

    def as_kwargs(self):
        res = {}
        for field in self.fields:
            if not field.is_set():
                continue

            res[field.name] = field.as_kwarg()

        return res

    def get_normal(self, value):
        if not isinstance(value, (dict,)):
            raise exceptions.InvalidPayloadError(
                'Schema field can be populated only with dictinary like '
                'payload (ie. {{"my_value": true}}), got: {}'.format(value))

        return value

    def populate(self, value):
        self.data = self.fields

    def as_json(self, user):
        if not self.is_set():
            return None

        tmp = {}

        for field in self.data:
            if not field.is_set():
                continue

            tmp[field.name] = field.as_json(user)

        return tmp


class BaseCollectionField(BaseField):
    subfield = None

    def __init__(self, name, subfield=None, **kwargs):
        if subfield is not None:
            self.subfield = subfield

        super().__init__(name, **kwargs)

    def populate(self, value):
        data = []

        for idx, val in enumerate(self.normalise(value)):
            instance = self.subfield(
                '{} - instance - {}'.format(self.name, idx))
            instance.parent = self
            instance.populate(val)

            data.append(instance)

        self.data = data

    def as_kwargs(self):
        res = []

        if self.is_set():
            for obj in self.data:
                res.append(obj.as_kwarg())

        return res

    def get_normal(self, value):
        if not isinstance(value, collections.Iterable):
            raise exceptions.InvalidPayloadError(
                "Collection field can be populated only with iterable "
                "payload (ie. list), got: {}".format(value))

        return list(value)

    def as_json(self, user):
        if not self.is_set():
            return None

        tmp = []

        for obj in self.data:
            if not obj.is_set():
                continue

            tmp.append(obj.as_json(user))

        return tmp


class BaseBoolField(BaseField):
    def get_normal(self, value):
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


class BaseDateField(BaseField):
    def get_normal(self, value):
        return tools.datetime_helpers.parse_into_datetime(value)


class BaseStringField(BaseField):
    def get_normal(self, value):
        return str(value)


class BaseIntegerField(BaseField):
    def get_normal(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            raise exceptions.InvalidPayloadError(
                "Unable convert value to integer, got: {}".format(value))
