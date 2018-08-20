#!/usr/bin/env bash

set -e

# following line will fail with full stack trace if there is mistake in settings
APP_NAME=$(python3 -c 'from magicarp.settings.base import APP_NAME; print(APP_NAME)')

HOST=$(python3 -c 'from simple_settings import settings; print(settings.FLASK_SERVER_HOST)')
PORT=$(python3 -c 'from simple_settings import settings; print(settings.FLASK_SERVER_PORT)')

export FLASK_APP=magicarp.server_factory:create_app
export DEBUG=$(python -c 'from simple_settings import settings; print(settings.DEBUG)')
export FLASK_ENV=$(python -c 'from simple_settings import settings; print(settings.FLASK_ENV)')

flask run --host=$HOST --port=$PORT --no-reload
