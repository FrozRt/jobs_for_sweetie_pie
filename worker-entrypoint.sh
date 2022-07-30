#!/bin/sh
set -e

beat() {
  echo "Starting beat..."

  exec celery -A core.celery_app  beat \
      --loglevel=info \
      --pidfile=
  }

worker() {
  echo "Starting worker..."

  exec celery -A core.celery_app worker \
      --concurrency=4 \
      --loglevel=info
  }


case "$1" in
  worker)
    shift
    worker
    ;;
  beat)
    shift
    beat
    ;;
  *)
    exec "$@"
    ;;
esac