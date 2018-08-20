from simple_settings import settings


class AbstractUser(object):
    def __init__(self, uid, name, email, language_code, timezone):
        self.uid = uid
        self.name = name
        self.email = email
        self.language_code = language_code
        self.timezone = timezone

    def has_permission(self, endpoint):
        return False

    def is_authorised(self):
        return False


class UnauthorizedUser(AbstractUser):
    def __init__(self):
        super().__init__(
            '0', 'Unauthorized', 'unauthorized@example.com',
            settings.DEFAULT_LANGUAGE_CODE, settings.DEFAULT_TIMEZONE)


class AuthorizedUser(AbstractUser):
    def __init__(self, uid, name, email, language_code=None, timezone=None):
        if language_code is None:
            language_code = settings.DEFAULT_LANGUAGE_CODE

        if timezone is None:
            timezone = settings.DEFAULT_TIMEZONE

        super().__init__(
            uid, name, email, language_code, timezone)

    def has_permission(self, endpoint):
        # NOTE: entry point to limit endpoints per user, if it's that something
        # that you want to have on api

        return True

    def is_authorised(self):
        return True
