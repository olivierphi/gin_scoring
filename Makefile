PYTHON_BINS ?= .venv/bin
PYTHON ?= $(PYTHON_BINS)/python
POETRY_VERSION ?= 1.8.3
MAKE_SILENT ?= ${MAKE} --silent

DATABASE_URL ?= sqlite+aiosqlite:///db.sqlite3

.DEFAULT_GOAL := help

help:
# @link https://github.com/marmelab/javascript-boilerplate/blob/master/makefile
	@grep -P '^[.a-zA-Z/_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: .venv ## Install the Python dependencies
	@pipx run poetry==${POETRY_VERSION} install
	@${MAKE_SILENT} .venv/bin/black

.PHONY: dev
dev: hostname ?= localhost
dev: port ?= 8000
dev: .env.local ## Run the FastAPI development server, via Uvicorn
	@${PYTHON_BINS}/fastapi dev \
		--host ${hostname} --port ${port} \
		src/gin_scoring/main.py

.PHONY: db/make-migration
db/make-migration: message ?= # mandatory
db/make-migration:
	@[ "${message}" ] || ( echo "! Make variable 'message' is not set"; exit 1 )
	@DATABASE_URL=${DATABASE_URL} ${PYTHON_BINS}/alembic \
		revision --autogenerate -m "${message}"

.PHONY: db/migrate
db/migrate: target ?= head
db/migrate:
	@DATABASE_URL=${DATABASE_URL} ${PYTHON_BINS}/alembic \
		upgrade ${target}

.env.local:
	@echo "DATABASE_URL=${DATABASE_URL}" > .env.local

.venv/bin/black: .venv ## A simple and stupid shim to use the IDE's Black integration with Ruff
	@echo '#!/usr/bin/env sh\n$$(dirname "$$0")/ruff format $$@' > ${PYTHON_BINS}/black
	@chmod +x ${PYTHON_BINS}/black
