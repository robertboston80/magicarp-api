import os
import logging

APP_NAME = 'magicarp'

# allows to override flask's settings
FLASK_CONFIG = None

DEBUG = False
TESTING = False

FLASK_ENV = 'development'

SECRET_KEY = None

TEST_USER_ENABLED = False

# if you have one backend for multiple api's, change namespace to avoid user
# session collision
SESSION_NAMESPACE = 'magicarp'

DEFAULT_LANGUAGE_CODE = 'en_GB'
DATE_TIMEZONE = 'UTC'

# leave None if you don't want to use rollbar
ROLLBAR_API_KEY = None
ROLLBAR_ENABLED = False
ROLLBAR_ENV = 'dev'

BASE_LOCATION = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..'))

CACHE_ENGINE = 'dummy'

LOCAL_LOGS_ENABLED = True
LOG_ENABLED = True

LOGGING_FORMAT = "[%(asctime)s] %(message)s"
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_PATH = os.path.join(BASE_LOCATION, 'logs', 'api.log')
LOG_LEVEL = logging.WARNING
