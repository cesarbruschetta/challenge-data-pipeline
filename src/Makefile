export PYTHONPATH = .
export MYPYPATH = ./stubs
export SOURCE_PATH = ./pipeline_twitter

export DOCKER_IMAGE_NAME = cesarbruschetta/challenget-data-pipeline:lastest

# SET .env and override default envs
ifneq (,$(wildcard ./.env))
    include .env
	export $(shell sed 's/=.*//' .env)
endif

.PHONY: help

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

## tests
tests: ## Runs unit tests
	@make tests-matching-cov && \
	make coverage

define run-tests-matching
poetry run pytest -xvv ${SOURCE_PATH} -k "$(k)" $(1) \
--ignore="$(i)" \
--disable-warnings \
--import-mode=importlib
endef

tests-matching: ## Runs tests matching a patter with the 'k' parameter
	$(call run-tests-matching)

tests-matching-cov: ## Runs tests matching a patter with the 'k' parameter with coverage
	$(call run-tests-matching,--cov=${SOURCE_PATH} --no-cov-on-fail --cov-report=)

coverage: ## Runs the coverage command
	@echo "Running coverage..." && \
	poetry run coverage report && \
	poetry run coverage xml

report-html: ## Runs the coverage report in HTML
	@echo "Running coverage report in HTML..." && \
	poetry run coverage html
	
## evironment
dependencies: ## Installs dev dependencies
	@poetry install --no-root


## checks code quality
isort-save: ## Formats imports
	@poetry run isort ${SOURCE_PATH} && \
	echo 'Isort save success!\n'

black-save: ## Formats code
	@poetry run black ${SOURCE_PATH}  && \
	echo 'Black save success!\n'

flake8: ## Runs some checks on code
	@poetry run flake8 ${SOURCE_PATH}  && \
	echo 'Flake8 check success!\n'

mypy: ## Checks python typing
	@poetry run mypy ${SOURCE_PATH}  && \
	echo 'Mypy check success!\n'

checks: blank-line isort-save black-save flake8 mypy ## Runs security checks, format, flake8 and mypy

blank-line:
	@echo

## docker
docker-build: ## Builds the docker image
	@docker build --platform linux/amd64 -t ${DOCKER_IMAGE_NAME} .

docker-push: ## Pushes the docker image
	@docker push ${DOCKER_IMAGE_NAME}