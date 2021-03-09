FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apk add linux-headers g++ build-base libressl-dev libxslt-dev libgcrypt-dev musl-dev libffi-dev \
libxml2 libxslt libc-dev

RUN poetry install --no-dev --no-root

COPY . ./app

CMD ["celery", "worker", "-A", "core.celery_app", "-l", "info"]