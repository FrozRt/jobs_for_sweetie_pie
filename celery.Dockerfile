FROM python:3.8-alpine3.14

ENV PYTHONUNBUFFERED 1

RUN apk add linux-headers g++ build-base libressl-dev libxslt-dev libgcrypt-dev musl-dev libffi-dev \
libxml2 libxslt libc-dev

RUN pip install "poetry==1.1.13"
RUN poetry install --no-dev --no-root

COPY . ./app

