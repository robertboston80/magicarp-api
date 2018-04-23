import os
import logging

APP_NAME = 'scaffold'

DEBUG = False
TESTING = False

ENV_TEST = 'TEST'
ENV_PROD = 'PROD'
ENV_DEV = 'DEV'

ENV = None

# if you have one backend for multiple api's, change namespace to avoid user
# session collision
SESSION_NAMESPACE = 'api'

DEFAULT_LANGUAGE_CODE = 'en_GB'
DATE_TIMEZONE = 'UTC'

# leave None if you don't want to use rollbar
ROLLBAR_API_KEY = None

ROLLBAR_ENABLED = False

ENABLE_ROLLBAR = False

BASE_LOCATION = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..'))

LOG_ENABLED = True

LOGGING_FORMAT = "[%(asctime)s] %(message)s"
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_PATH = os.path.join(BASE_LOCATION, 'logs', 'api.log')
LOG_LEVEL = logging.WARNING
