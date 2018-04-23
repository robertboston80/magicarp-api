"""
Tools
=====

This sub-package is a typical location for all helper functions that we keep in
framework. Package holds modules and assorted functions that are too small to
be separated to own namespace.
"""

import datetime

import pytz

from simple_settings import settings
from dateutil import parser as date_parser

from . import (  # NOQA
    logging, misc, api_request, auth_model, auth, validators, response,
    endpoint)


def dt_utcnow():
    '''Returns now() UTC with tzinfo'''
    now = datetime.datetime.utcnow()
    now = now.replace(tzinfo=pytz.utc)
    return now


def _fix_timezone(date_obj, timezone=None):
    if not timezone:
        timezone = settings.DATE_TIMEZONE

    zone = pytz.timezone(timezone)

    date_obj = date_obj.astimezone(zone) if date_obj.tzinfo \
        else zone.localize(date_obj)

    return date_obj


def parse_into_datetime(value, timezone=None):
    '''Parse a string into a datetime

    Expects: string value representing a datetime
    '''
    if not value:
        raise ValueError(
            "Object needs to be non-empty in order to parse it as a date")

    date_obj = date_parser.parse(value)

    return _fix_timezone(date_obj, timezone)


def get_current_datetime(timezone=None):
    date_obj = datetime.datetime.now().replace(microsecond=0)

    return _fix_timezone(date_obj)
