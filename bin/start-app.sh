#!/usr/bin/env bash

export FLASK_APP=magicarp.server

HOST=$(python -c 'from simple_settings import settings; print(settings.FLASK_SERVER_HOST)')
PORT=$(python -c 'from simple_settings import settings; print(settings.FLASK_SERVER_PORT)')

flask run --host=$HOST --port=$PORT
