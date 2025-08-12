FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/* && \
    pip install uv


WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --python=/usr/local/bin/python

COPY . .

ENV PYTHONUNBUFFERED=1

