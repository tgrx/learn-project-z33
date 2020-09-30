#!/usr/bin/env bash

DIR_SCRIPTS="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

gunicorn --config="${DIR_SCRIPTS}/gunicorn.conf.py" project.asgi:application
