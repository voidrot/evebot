#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

function start_dev_server() {
  echo "Running makemigrations..."
  python manage.py makemigrations
  echo "Running migrate..."
  python manage.py migrate
  echo "Starting development server..."
  exec uvicorn config.asgi:application --host 0.0.0.0 --reload --reload-include '*.html'
}

function start_prod_server() {
  python manage.py collectstatic --noinput --no-color
  echo "Starting production server..."
  python -m gunicorn config.asgi:application -k uvicorn_worker.UvicornWorker
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
  if [[ -z "DEBUG" ] && [ -s DEBUG ]]; then
    rm -f './celerybeat.pid'
    exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app beat -l INFO'
  else
    exec celery -A config.celery_app beat -l INFO
  fi
elif [ "$PROCESS_TYPE" == "worker" ]; then
  if [[ -z "DEBUG" ] && [ -s DEBUG ]]; then
    exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app worker -l INFO'
  else
    exec celery -A config.celery_app worker -l INFO
  fi
elif [ "$PROCESS_TYPE" == "flower" ]; then
  if [[ -z "DEBUG" ] && [ -s DEBUG ]]; then
    until timeout 10 celery -A config.celery_app inspect ping; do
      >&2 echo "Celery workers not available"
    done

    echo 'Starting flower'

    exec watchfiles --filter python celery.__main__.main \
      --args \
      "-A config.celery_app -b \"${VALKEY_URL}\" flower --basic_auth=\"${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}\""
  else
    until timeout 10 celery -A config.celery_app inspect ping; do
      >&2 echo "Celery workers not available"
    done

    echo 'Starting flower'

    exec celery \
        -A config.celery_app \
        -b "${VALKEY_URL}" \
        flower \
        --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"
  fi
else
  echo "Invalid process type. Please choose from: server, beat, worker, or flower."
  exit 1
fi
