.PHONY:
	help
	tf_init
	tf_plan
	tf_apply
	tf_destroy
	start-minikube-cluster
	stop-minikube-cluster
	start-kind-cluster
	stop-kind-cluster
	

.DEFAULT_GOAL := help 

export KUBE_CONTEXT ?= challenge-data-pipeline

# SET .env and override default envs
ifneq (,$(wildcard ./.env))
    include .env
	export $(shell sed 's/=.*//' .env)
endif

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}'


KUBECTL := kubectl --context=$(KUBE_CONTEXT)
HELM := helm --kube-context=$(KUBE_CONTEXT)
TERRAFORM := cd ./terraform && terraform


start-minikube-cluster: ## Start the minikube cluster
	@minikube start --profile=$(KUBE_CONTEXT) \
	--cpus=4 --memory=4g --ports 80 --ports 443 \
	--addons ingress --addons registry --addons metrics-server --addons csi-hostpath-driver --addons volumesnapshots

stop-minikube-cluster: ## Stop the minikube cluster
	@minikube delete --purge --profile=$(KUBE_CONTEXT)

start-kind-cluster: ## Start the kind cluster
	@echo "Creating kind registry" && \
	docker run \
		-d --restart=always -p "127.0.0.1:5001:5000" --name "kind-registry" \
		registry:2 && \
	echo "Creating k8s cluster" && \
	kind create cluster \
		--name ${KUBE_CONTEXT} \
		--config ./terraform/manifests/kind_cluster/config.yaml \
		--verbosity 2
	echo "Connect the registry to the cluster network if not already connected" && \
	docker network connect "kind" "kind-registry"

stop-kind-cluster: ## Stop the kind cluster
	@echo "Deleting kind registry" && \
	docker rm -f kind-registry && \
	echo "Deleting k8s cluster" && \
	kind delete clusters --name ${KUBE_CONTEXT} --verbosity 2

tf_init: ## Terraform init backend
	@${TERRAFORM} init

tf_plan: tf_init ## Terraform plan
	@${TERRAFORM} plan

tf_apply: tf_init ## Terraform apply
	@${TERRAFORM} apply -auto-approve

tf_destroy: tf_init ## Terraform destroy
	@${TERRAFORM} destroy