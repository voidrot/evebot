#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

function start_dev_server() {
  echo "Running collectstatic..."
  python manage.py collectstatic --noinput --no-color
  echo "Running makemigrations..."
  python manage.py makemigrations
  echo "Running migrate..."
  python manage.py migrate
  echo "Starting development server..."
  exec uvicorn evebot.asgi:application --host 0.0.0.0 --reload --reload-include '*.html'
}

function start_prod_server() {
  python manage.py collectstatic --noinput --no-color
  echo "Starting production server..."
  python -m gunicorn evebot.asgi:application -k uvicorn_worker.UvicornWorker
}

if [ $# -eq 0 ]; then
    echo "Usage: start.sh [PROCESS_TYPE](server/beat/worker/flower)"
    exit 1
fi

PROCESS_TYPE=$1

if [ "$PROCESS_TYPE" == "server" ]; then
  if [ -n "$DEBUG" ]; then
    start_dev_server
  else
    start_prod_server
  fi
elif [ "$PROCESS_TYPE" == "beat" ]; then
  if [[ -z "DEBUG" && -s DEBUG ]]; then
    rm -f './celerybeat.pid'
    exec watchfiles --filter python celery.__main__.main --args '-A evebot.celery_app beat -l INFO'
  else
    exec celery -A evebot.celery_app beat -l INFO
  fi
elif [ "$PROCESS_TYPE" == "worker" ]; then
  if [[ -z "DEBUG" && -s DEBUG ]]; then
    exec watchfiles --filter python celery.__main__.main --args '-A evebot.celery_app worker -l INFO'
  else
    exec celery -A evebot.celery_app worker -l INFO
  fi
elif [ "$PROCESS_TYPE" == "flower" ]; then
  if [[ -z "DEBUG" && -s DEBUG ]]; then
    until timeout 10 celery -A evebot.celery_app inspect ping; do
      >&2 echo "Celery workers not available"
    done

    echo 'Starting flower'

    exec watchfiles --filter python celery.__main__.main \
      --args \
      "-A evebot.celery_app -b \"${VALKEY_URL}\" flower --basic_auth=\"${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}\""
  else
    until timeout 10 celery -A evebot.celery_app inspect ping; do
      >&2 echo "Celery workers not available"
    done

    echo 'Starting flower'

    exec celery \
        -A evebot.celery_app \
        -b "${VALKEY_URL}" \
        flower \
        --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"
  fi
else
  echo "Invalid process type. Please choose from: server, beat, worker, or flower."
  exit 1
fi
