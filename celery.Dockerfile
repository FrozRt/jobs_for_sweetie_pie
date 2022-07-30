FROM python:3.8-slim-buster

WORKDIR /app
COPY poetry.lock pyproject.toml /app/


RUN apt-get update && pip install --upgrade pip poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev \
    && rm -rf /root/.cache/pip

ENV PYTHONUNBUFFERED 1

RUN adduser --uid 1000 --home /app --disabled-password --gecos "" worker && \
    chown -hR worker: /app

COPY --chown=worker:worker . /app
WORKDIR /app

ENV PYTHONPATH=/app

RUN chmod +x ./worker-entrypoint.sh

USER worker
ENTRYPOINT ["./worker-entrypoint.sh"]