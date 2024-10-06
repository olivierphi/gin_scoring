FROM python:3.11-slim-bookworm AS backend_build

ENV POETRY_VERSION=1.8.3

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=0 PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN pip install poetry==${POETRY_VERSION}

RUN mkdir -p /app
WORKDIR /app

RUN python -m venv --symlinks .venv

COPY pyproject.toml poetry.lock ./
RUN poetry install --only=main --no-root --no-interaction --no-ansi

FROM python:3.11-slim-bookworm AS backend_run

ENV PYTHONDONTWRITEBYTECODE=0 PYTHONUNBUFFERED=1

RUN mkdir -p /app
WORKDIR /app

RUN addgroup -gid 1001 webapp
RUN useradd --gid 1001 --uid 1001 webapp
RUN chown -R 1001:1001 /app

COPY --chown=1001:1001 --from=backend_build /app/.venv .venv

COPY --chown=1001:1001 src src
COPY --chown=1001:1001 scripts scripts
COPY --chown=1001:1001 manage.py Makefile pyproject.toml LICENSE ./

ENV PATH="/app/.venv/bin:$PATH"
RUN python -V

USER 1001:1001

ENV PYTHONPATH="/app/src"

RUN mkdir -p /app/staticfiles
RUN DJANGO_SETTINGS_MODULE=gin_scoring.project.settings.docker_build \
    .venv/bin/python manage.py collectstatic --noinput

EXPOSE 8080

ENV DJANGO_SETTINGS_MODULE=gin_scoring.project.settings.production

ENV GUNICORN_CMD_ARGS="--bind 0.0.0.0:8080 --workers 2 --max-requests 120 --max-requests-jitter 20 --timeout 8"

RUN chmod +x scripts/start_server.sh
CMD ["scripts/start_server.sh"]
