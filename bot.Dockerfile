FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

RUN mkdir -p /app && pip install poetry && poetry config virtualenvs.create false

WORKDIR /app

COPY . /app

RUN poetry install --no-dev --no-root

CMD ["python", "main.py"]