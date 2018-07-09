import os
import logging

from . import favicon

FAVICON_CONTENT = favicon.__doc__

APP_NAME = 'magicarp'

# allows to override flask's settings
FLASK_CONFIG = None

DEBUG = False
TESTING = False

FLASK_ENV = 'development'

SECRET_KEY = None

ROUTING_ADD_COMMON = True
ROUTING_ADD_AUTH = True

TEST_USER_ENABLED = False
TEST_USER = None

# if you have one backend for multiple api's, change namespace to avoid user
# session collision
SESSION_NAMESPACE = 'magicarp'

DEFAULT_LANGUAGE_CODE = 'en_GB'
DATE_TIMEZONE = 'UTC'

CACHE_ENGINE = 'dummy'


def get_redis_engine():
    from magicarp.storage import redis_engine

    return redis_engine


def get_dummy_engine():
    from magicarp.storage import dummy_engine

    return dummy_engine


STORAGE_SETTINGS = {}
STORAGE_ENGINE = 'dummy'
STORAGE_ENGINES = {
    'redis': get_redis_engine,
    'dummy': get_dummy_engine,
}

# if you want to integrate leave None if you don't want to use rollbar
ROLLBAR_API_KEY = None
ROLLBAR_ENV = 'dev'

# logging is handled by standard `python` logging module, hence this
# dictionary, it is used by logging.config.dictConfig on app start-up,
# after that there is possibility to register new handlers with any number of
# existing loggers, for more complex solution, providing function
# `register_loggers` to `create_app` in module `server_factory` is recommended
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'magicarp': {
            'handlers': ['console'],
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
}


# if you want to register additional handlers for loging as defined in LOGGING
# dict, override LOGGING_ADDITIONAL_HANDLERS with list of callables that
# take no arguments and return instance of handler, ie.
# LOGGING_ADDITIONAL_HANDLERS = [lambda: SMTPHandler()]
LOGGING_ADDITIONAL_HANDLERS = ()

# if you want to attach extra handlers defined in LOGGING_ADDITIONAL_HANDLERS, 
# override LOGGING_ADDITIONAL_LOGGERS with list of strings, where each of them
# defines logger that should have handler added, ie. sqlalchemy, note:
# 'app.logger' is standard flask logger that will defined after
# logging.config.dictConfig
LOGGING_ADDITIONAL_LOGGERS = (
    'app.logger',
)

FLASK_SERVER_HOST = '0.0.0.0'
FLASK_SERVER_PORT = 5000

# if you want to have capability of assigning custom error codes that are
# stable, populate this dictionary with keys that are strings and values that
# are unique numeric values
# ie.
# ERROR_CODEBOOK_ATTRIBUTES = {
#   'user': 1,
#   'address': 2,
#   and etc...
# }
ERROR_CODEBOOK_ATTRIBUTES = {}
ERROR_CODEBOOK_SCHEMA = {}
