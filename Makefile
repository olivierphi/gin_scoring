PYTHON_BINS ?= ./.venv/bin
PYTHON ?= ${PYTHON_BINS}/python
PYTHONPATH ?= ${PWD}/src
DJANGO_SETTINGS_MODULE ?= project.settings.development

.DEFAULT_GOAL := help

help:
# @link https://github.com/marmelab/javascript-boilerplate/blob/master/makefile
	@grep -P '^[a-zA-Z/_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: .venv ## Install the Python dependencies
	${PYTHON_BINS}/poetry install

dev: ./.venv/bin/django ## Start the Django development server
	@PYTHONPATH=${PYTHONPATH} DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} \
		${PYTHON} src/manage.py runserver

.PHONY: test
test: pytest_opts ?=
test: ## Launch the pytest tests suite
	@PYTHONPATH=${PYTHONPATH} ${PYTHON_BINS}/pytest ${pytest_opts}

.PHONY: code-quality/all
code-quality/all: code-quality/black code-quality/isort code-quality/mypy  ## Run all our code quality tools

.PHONY: code-quality/black
code-quality/black: black_opts ?=
code-quality/black: ## Automated 'a la Prettier' code formatting
# @link https://black.readthedocs.io/en/stable/
	@${PYTHON_BINS}/black ${black_opts} src/ tests/

.PHONY: code-quality/isort
code-quality/isort: isort_opts ?=
code-quality/isort: ## Automated Python imports formatting
	@${PYTHON_BINS}/isort --settings-file=pyproject.toml ${isort_opts} src/ tests/

.PHONY: code-quality/mypy
code-quality/mypy: mypy_opts ?=
code-quality/mypy: ## Python's equivalent of TypeScript
# @link https://mypy.readthedocs.io/en/stable/
	@PYTHONPATH=${PYTHONPATH} ${PYTHON_BINS}/mypy src/ ${mypy_opts}

.venv: ## Initialises the Python virtual environment in a ".venv" folder
	python -m venv .venv
	${PYTHON_BINS}/pip install -U pip poetry

./.venv/bin/django: .venv install

# Here starts Docker-related stuff

DOCKER_IMG_NAME ?= gin-scoring
DOCKER_TAG ?= latest

.PHONY: docker/build
docker/build: use_buildkit ?= 1 # @link https://docs.docker.com/develop/develop-images/build_enhancements/
docker/build: docker_build_args ?=
docker/build: ## Docker: build the image
	DOCKER_BUILDKIT=${use_buildkit} docker build -t ${DOCKER_IMG_NAME}:${DOCKER_TAG} ${docker_build_args} .

.PHONY: docker/test-locally
docker/test-locally: port ?= 8080
docker/test-locally: docker_args ?=
docker/test-locally: docker_env ?= -e SECRET_KEY=does-not-matter-here -e DATABASE_URL=sqlite://:memory: -e ALLOWED_HOSTS=* -e DJANGO_SETTINGS_MODULE=project.settings.flyio
docker/test-locally: ## Docker: launch the previously built image, listening on port 8080
	docker run -p ${port}:8080 ${docker_env} ${docker_args} ${DOCKER_IMG_NAME}:${DOCKER_TAG}

.PHONY: fly.io/deploy
fly.io/deploy: deploy_build_args ?=
fly.io/deploy: ## Fly.io: deploy the previously built Docker image
	flyctl deploy ${deploy_build_args}

.PHONY: fly.io/ssh
fly.io/ssh: ## Fly.io: start a SSH session within our app
	flyctl ssh console
                
.PHONY: fly.io/db/local_backup
fly.io/db/local_backup: backup_name ?= $$(date --iso-8601=seconds | cut -d + -f 1)
fly.io/db/local_backup: ## Fly.io: backup the SQLite database locally
	@flyctl ssh sftp get /sqlite_dbs/gin-scoring.prod.sqlite3
	@mv gin-scoring.prod.sqlite3 "gin-scoring.prod.backup.${backup_name}.sqlite3"
	@echo "Saved to 'gin-scoring.prod.backup.${backup_name}.sqlite3'"
                
.PHONY: fly.io/db/prod_to_local
fly.io/db/prod_to_local: local_db ?= ./db.sqlite3
fly.io/db/prod_to_local: backup_name ?= ./db.local.backup.$$(date --iso-8601=seconds | cut -d + -f 1).sqlite3
fly.io/db/prod_to_local: ## Fly.io: replace our local SQLite database with the one from the prod environment
	@mv "${local_db}" "${backup_name}"
	@flyctl ssh sftp get /sqlite_dbs/gin-scoring.prod.sqlite3
	@mv gin-scoring.prod.sqlite3 "${local_db}"
	@echo "Replaced local DB with a copy from the production DB. The previous local DB has been saved as '${backup_name}'."
