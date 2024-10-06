PYTHON_VERSION ?= 3.11
PYTHON_BIN ?= ./.venv/bin
PYTHON ?= ${PYTHON_BIN}/python
DJANGO_SETTINGS_MODULE ?= gin_scoring.project.settings.development
SUB_MAKE = ${MAKE} --no-print-directory

.DEFAULT_GOAL := help

help:
# @link https://github.com/marmelab/javascript-boilerplate/blob/master/makefile
	@grep -P '^[a-zA-Z/_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: poetry_version ?= 1.8.3
install: check-python-version check-pipx .venv ## Install the Python dependencies, via `pipx run poetry install`
# Install Python dependencies:
	pipx run poetry==${poetry_version} install
# Install pre-commit hooks:
	${PYTHON_BINS}/pre-commit install

dev: address ?= localhost
dev: port ?= 8000
dev: dotenv_file ?= .env.local
dev: check-python-version .venv .env.local db.sqlite3 ## Start the Django development server
	@${SUB_MAKE} django/manage cmd='runserver ${address}:${port}'

.PHONY: test
test: pytest_opts ?=
test: dotenv_file ?= .env.local
test: ## Launch the pytest tests suite
	@${PYTHON_BIN}/dotenv -f '${dotenv_file}' run -- \
		${PYTHON_BIN}/pytest ${pytest_opts}

.PHONY: code-quality/all
code-quality/all: code-quality/black code-quality/isort code-quality/mypy  ## Run all our code quality tools

.PHONY: code-quality/black
code-quality/black: black_opts ?=
code-quality/black: ## Automated 'a la Prettier' code formatting
# @link https://black.readthedocs.io/en/stable/
	@${PYTHON_BIN}/black ${black_opts} src/ tests/

.PHONY: code-quality/isort
code-quality/isort: isort_opts ?=
code-quality/isort: ## Automated Python imports formatting
	@${PYTHON_BIN}/isort --settings-file=pyproject.toml ${isort_opts} src/ tests/

.PHONY: code-quality/mypy
code-quality/mypy: mypy_opts ?=
code-quality/mypy: dotenv_file ?= .env.local
code-quality/mypy: ## Python's equivalent of TypeScript
# @link https://mypy.readthedocs.io/en/stable/
	@DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} \
		${PYTHON_BIN}/dotenv -f '${dotenv_file}' run -- \
			${PYTHON_BIN}/mypy src/ ${mypy_opts}

django/manage: env_vars ?= 
django/manage: dotenv_file ?= .env.local
django/manage: cmd ?= --help
django/manage: .venv .env.local ## Run a Django management command
	@echo "Running Django management command: ${cmd}"
	@DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} ${env_vars} \
		${PYTHON_BIN}/dotenv -f '${dotenv_file}' run -- \
			${PYTHON} manage.py ${cmd}

.venv: ## Initialises the Python virtual environment in a ".venv" folder
	@python -m venv .venv

.env.local: ## Copies the ".env.dist" file to ".env.local" (git-ignored)
	cp .env.dist .env.local

db.sqlite3: dotenv_file ?= .env.local
db.sqlite3: .env.local ## Initialises the SQLite database
	touch db.sqlite3
	@${SUB_MAKE} django/manage cmd='migrate'
	@DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} \
		${PYTHON_BIN}/dotenv -f '${dotenv_file}' run -- \
		${PYTHON_BIN}/python scripts/optimise_db.py

.PHONY: check-pipx
check-pipx:
	@which pipx > /dev/null || (echo "'pipx' not found in PATH" && exit 1)

.PHONY: check-python-version
check-python-version:
	@which python > /dev/null || (echo "'python' not found in PATH" && exit 1)
	@PYTHON_VERSION=$$(python --version 2>&1) && \
	case $$PYTHON_VERSION in \
	  "Python ${PYTHON_VERSION}"*) ;; \
	  *) echo "Python ${PYTHON_VERSION}.x is required, but found $$PYTHON_VERSION" && exit 1 ;; \
	esac

# Here starts Docker-related stuff

DOCKER_IMG_NAME ?= gin-scoring
DOCKER_TAG ?= latest

.PHONY: docker/build
docker/build: use_buildkit ?= 1 # @link https://docs.docker.com/develop/develop-images/build_enhancements/
docker/build: docker_build_args ?=
docker/build: ## Docker: build the image
	DOCKER_BUILDKIT=${use_buildkit} docker build -t ${DOCKER_IMG_NAME}:${DOCKER_TAG} ${docker_build_args} .

.PHONY: docker/local/run
docker/local/run: port ?= 8080
docker/local/run: port_exposed ?= 8080
docker/local/run: docker_args ?= --rm -it
docker/local/run: docker_env ?= -e SECRET_KEY=does-not-matter-here -e DATABASE_URL=sqlite:////app/shared_volume/db.sqlite3 -e ALLOWED_HOSTS=* -e SECURE_SSL_REDIRECT=
docker/local/run: cmd ?= scripts/start_server.sh
docker/local/run: GUNICORN_CMD_ARGS ?= --bind :8080 --workers 2 --max-requests 120 --max-requests-jitter 20 --timeout 8
docker/local/run: user_id ?= $$(id -u)
docker/local/run: ## Docker: launch the previously built image, listening on port 8080
	docker run -p ${port_exposed}:${port} -v "${PWD}/.docker/:/app/shared_volume/" \
		-u ${user_id} \
		${docker_env} ${docker_args} \
		-e DJANGO_SETTINGS_MODULE=gin_scoring.project.settings.production \
		-e GUNICORN_CMD_ARGS='${GUNICORN_CMD_ARGS}' \
		${DOCKER_IMG_NAME}:${DOCKER_TAG} \
		${cmd}

.PHONY: docker/local/shell
docker/local/shell: docker_args ?= --rm -it 
docker/local/shell: docker_env ?= -e SECRET_KEY=does-not-matter-here -e DATABASE_URL=sqlite:////app/shared_volume/db.sqlite3 -e ALLOWED_HOSTS=* -e SECURE_SSL_REDIRECT=
docker/local/shell: cmd ?= bash
docker/local/shell: user_id ?= $$(id -u)
docker/local/shell: entrypoint_args ?= 
docker/local/shell:
	docker run -v "${PWD}/.docker/:/app/shared_volume/" \
		-u ${user_id} \
		${docker_env} ${docker_args} \
		-e DJANGO_SETTINGS_MODULE=gin_scoring.project.settings.production \
		--entrypoint ${cmd} \
		${DOCKER_IMG_NAME}:${DOCKER_TAG} \
		${entrypoint_args}

.PHONY: docker/local/migrate
docker/local/migrate:
	${SUB_MAKE} docker/local/shell \
		cmd='/app/.venv/bin/python' entrypoint_args='manage.py migrate'
		
.PHONY: fly.io/deploy
fly.io/deploy: deploy_build_args ?=
fly.io/deploy: ## Fly.io: deploy the previously built Docker image
	flyctl deploy ${deploy_build_args}

.PHONY: fly.io/ssh
fly.io/ssh: ## Fly.io: start a SSH session within our app
	flyctl ssh console
                
.PHONY: fly.io/db/local_backup
fly.io/db/local_backup: remote_db_name ?= gin-scoring.mutiplayer.prod.sqlite3
fly.io/db/local_backup: backup_name ?= $$(date --iso-8601=seconds | cut -d + -f 1)
fly.io/db/local_backup: ## Fly.io: backup the SQLite database locally
	@flyctl ssh sftp get "/sqlite_dbs/${remote_db_name}"
	@mv "${gin-scoring.mutiplayer.prod.sqlite3}" "gin-scoring.prod.backup.${backup_name}.sqlite3"
	@echo "Saved to 'gin-scoring.prod.backup.${backup_name}.sqlite3'"
                
.PHONY: fly.io/db/prod_to_local
fly.io/db/prod_to_local: local_db ?= ./db.sqlite3
fly.io/db/prod_to_local: backup_name ?= ./db.local.backup.$$(date --iso-8601=seconds | cut -d + -f 1).sqlite3
fly.io/db/prod_to_local: ## Fly.io: replace our local SQLite database with the one from the prod environment
	@mv "${local_db}" "${backup_name}"
	@flyctl ssh sftp get /sqlite_dbs/gin-scoring.prod.sqlite3
	@mv gin-scoring.prod.sqlite3 "${local_db}"
	@echo "Replaced local DB with a copy from the production DB. The previous local DB has been saved as '${backup_name}'."
