PYTHON_BINS ?= ${PWD}/.venv/bin
PYTHON ?= ${PYTHON_BINS}/python
PYTHONPATH ?= ${PWD}/src
DJANGO_SETTINGS_MODULE ?= project.settings.development

dev:
	@PYTHONPATH=${PYTHONPATH} DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} \
		${PYTHON} src/manage.py runserver

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

# Here starts Docker-related stuff

DOCKER_IMG_NAME ?= gin-scoring
DOCKER_TAG ?= latest

.PHONY: docker/build
docker/build: use_buildkit ?= 1 # @link https://docs.docker.com/develop/develop-images/build_enhancements/
docker/build: docker_build_args ?=
docker/build:
	DOCKER_BUILDKIT=${use_buildkit} docker build -t ${DOCKER_IMG_NAME}:${DOCKER_TAG} ${docker_build_args} .

.PHONY: docker/test-locally
docker/test-locally: port ?= 8080
docker/test-locally: docker_args ?=
docker/test-locally: docker_env ?= -e SECRET_KEY=does-not-matter-here -e DATABASE_URL=sqlite://:memory: -e ALLOWED_HOSTS=* -e DJANGO_SETTINGS_MODULE=project.settings.flyio
docker/test-locally: 
	docker run -p ${port}:8080 ${docker_env} ${docker_args} ${DOCKER_IMG_NAME}:${DOCKER_TAG}

.PHONY: fly.io/deploy
fly.io/deploy: deploy_build_args ?=
fly.io/deploy: 
	flyctl deploy -i ${DOCKER_IMG_NAME}:${DOCKER_TAG} ${deploy_build_args}

.PHONY: fly.io/ssh
fly.io/ssh:
	flyctl ssh console
