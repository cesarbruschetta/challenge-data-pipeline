
integration-pipeline-local: poetry-check checks-nosave all-tests coverage ## Runs all steps for integrating locally or Bitbucket CI

integration-pipeline-docker: poetry-check checks-nosave docker-up ## Runs all steps for integrating in docker
	@sleep 20
	@make all-tests
	@make docker-down
	@poetry run docker-compose run coverage

poetry-check: safety ## Runs poetry check
	@poetry check

safety:
	@poetry run safety check --full-report -i 37894

docker-up: ## Starts all services on docker-compose as daemon
	@poetry run docker-compose up -d --force-recreate --build

docker-down: ## Stops all services on docker-compose
	@poetry run docker-compose down

docker-up-log: ## Starts all services on docker-compose as foreground
	@poetry run docker-compose up --force-recreate --build

docker-postgres: ## Starts postgres DB docker
	@poetry run docker-compose up -d --force-recreate --build postgres

docker-redis: ## Starts redis DB docker
	@poetry run docker-compose up -d --force-recreate --build redis

docker-flower: ## Starts flower DB docker
	@poetry run docker-compose up -d --force-recreate --build flower

docker-airflow-init: ## Starts airflow-init DB docker
	@poetry run docker-compose up -d --force-recreate --build airflow-init

docker-minio: ## Starts minio DB docker
	@poetry run docker-compose up -d --force-recreate --build minio

docker-airflow-all: ## Starts airflow-all DB docker
	@poetry run docker-compose up -d --force-recreate --build \
	airflow-webserver airflow-scheduler airflow-worker

docker-spark: ## Starts spark DB docker
	@poetry run docker-compose up -d --force-recreate --build \
	spark spark-worker-1 spark-worker-2

minio-init: ## Create buckets to setup project
	@docker run -ti --rm \
    	--env MC_HOST_minio=http://${MINIO_ACCESS_KEY}:${MINIO_SECRET_KEY}@minio:9000 \
    	--network challenge-data-pipeline_default \
    	minio/mc \
    	mb minio/lake-transient-challenge minio/lake-raw-challenge \
		minio/lake-trusted-challenge minio/lake-refined-challenge

minio-bash: ## Start docker minio/mc to manager minio server
	@docker run -ti --rm \
    	--env MC_HOST_minio=http://${MINIO_ACCESS_KEY}:${MINIO_SECRET_KEY}@minio:9000 \
    	--network challenge-data-pipeline_default \
		--entrypoint /bin/bash \
    	minio/mc

docker-dependencies: docker-postgres docker-redis docker-airflow-init docker-flower docker-minio ## Starts All docker dependencies

docker-apps-recreate:
	$(eval $(call check-var,APPS))
	@poetry run docker-compose up --force-recreate --build $(APPS)

wait:
	@sleep 20
