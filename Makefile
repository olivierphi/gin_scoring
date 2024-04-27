DATABASE_URL ?= sqlite:///db.sqlite3
PYTHON_BINS ?= .venv/bin
PYTHON ?= ${PYTHON_BINS}/python

.DEFAULT_GOAL := help

.PHONY: help
help:
# @link https://github.com/marmelab/javascript-boilerplate/blob/master/makefile
	@grep -P '^[a-zA-Z/_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: dev
dev: uvicorn_opts ?= --reload --reload-dir src/gin_scoring
dev:
	@DEBUG=1 ${PYTHON_BINS}/uvicorn gin_scoring.http:app ${uvicorn_opts}

.PHONY: db/make_migration
db/make_migration: ## Create a new database migration, via Alembic
	@${PYTHON_BINS}/alembic revision --autogenerate

.PHONY: db/migrate_latest
db/migrate_latest: ## Migrate database to latest version, via Alembic
	@${PYTHON_BINS}/alembic upgrade head
