#!/usr/bin/env bash

HOST=$(python -c 'from simple_settings import settings; print(settings.FLASK_SERVER_HOST)')
PORT=$(python -c 'from simple_settings import settings; print(settings.FLASK_SERVER_PORT)')

export FLASK_APP=magicarp.server_factory:create_app
export DEBUG=$(python -c 'from simple_settings import settings; print(settings.DEBUG)')
export FLASK_ENV=$(python -c 'from simple_settings import settings; print(settings.FLASK_ENV)')

flask run --host=$HOST --port=$PORT
