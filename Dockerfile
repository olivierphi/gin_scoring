# Simplistic Dockerfile, does the job for the moment but we should rather use a multi-steps one :-)
ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION} AS build

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

RUN mkdir -p /app
WORKDIR /app

RUN python -m venv .venv

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

FROM python:${PYTHON_VERSION}-slim AS run

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    libpq5 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app
WORKDIR /app

RUN addgroup -gid 1001 webapp
RUN useradd --gid 1001 --uid 1001 webapp
RUN chown -R 1001:1001 /app 
USER 1001:1001

COPY --chown=1001:1001 --from=build /app/.venv .venv
COPY --chown=1001:1001 . .

ENV PYTHONPATH=/app/src

RUN SECRET_KEY=does-not-matter-for-this-command DATABASE_URL=sqlite://:memory: ALLOWED_HOSTS=fly.io \
    .venv/bin/python src/manage.py collectstatic --noinput

EXPOSE 8080

CMD [".venv/bin/gunicorn", "--bind", ":8080", "--workers", "2", "project.wsgi"]
