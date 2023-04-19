
export DOCKER_IMAGE_NAME = localhost:5001/spark-submit:lastest

# SET .env and override default envs
ifneq (,$(wildcard ./.env))
    include .env
	export $(shell sed 's/=.*//' .env)
endif

.PHONY: help

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort


## docker
docker-build: ## Builds the docker image
	@docker build --platform linux/amd64 -t ${DOCKER_IMAGE_NAME} .

docker-push: ## Pushes the docker image
	@docker push ${DOCKER_IMAGE_NAME}