terraform {
  required_version = ">= 1.2.8"

  required_providers {
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.6.0"
    }
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = "1.14.0"
    }
  }

  backend "local" {
    path = "./terraform.tfstate"
    
  }

}

provider "helm" {
  kubernetes {
    config_path    = "~/.kube/config"
    config_context = "${var.cluster_name}"
  }
}

provider "kubectl" {
  config_path    = "~/.kube/config"
  config_context = "${var.cluster_name}"
}

data "kubectl_filename_list" "manifests" {
    pattern = "./manifests/k8s/*.yaml"
}

resource "kubectl_manifest" "k8s-apply" {
  count = length(data.kubectl_filename_list.manifests.matches)
  yaml_body = file(
    element(data.kubectl_filename_list.manifests.matches, count.index)
  )
}

resource "helm_release" "nfs-server" {

  depends_on = [
    kubectl_manifest.k8s-apply,
  ]

  repository = "https://charts.helm.sh/stable/"
  chart      = "nfs-server-provisioner"
  version    = "1.1.3"

  name       = "nfs-serve"
  namespace  = "nfs-serve"
  create_namespace = true

  timeout = 600

  set {
    name = "persistence.enabled"
    value = true
  }
  set {
    name = "persistence.storageClass"
    value = "${var.nfs-server-storageClass}"
  }
  set {
    name = "persistence.size"
    value = "200Gi"
  }

}

resource "helm_release" "minio" {

  depends_on = [
    helm_release.nfs-server,
  ]
  
  repository = "https://charts.min.io/"
  chart      = "minio"
  version    = "4.0.13"

  name       = "minio"
  namespace  = "minio"
  create_namespace = true
  
  timeout = 600

  values = [
    "${file("./manifests/minio/values.yaml")}"
  ]

  set {
    name  = "rootPassword"
    value = var.minio_root_password
  }

  set {
    name = "users[0].secretKey"
    value = var.minio_user_service_password
  }

}

resource "null_resource" "build-airflow-image" {
  depends_on = [
    helm_release.minio,
  ]

  provisioner "local-exec" {
    command = <<EOF
        docker build \
        --platform=linux/arm64 \
        --tag localhost:${var.registry_port}/custom-local-airflow:latest \
        ./manifests/airflow/docker && \
        docker push localhost:${var.registry_port}/custom-local-airflow:latest
    EOF
  }
}

resource "helm_release" "airflow" {
  depends_on = [
    null_resource.build-airflow-image,
  ]

  repository = "https://airflow.apache.org"
  chart      = "airflow"
  version    = "1.7.0"

  name             = "airflow"
  namespace        = "airflow"
  create_namespace = true
  wait             = false

  timeout = 600

  values = [
    "${file("./manifests/airflow/values.yaml")}"
  ]

  set {
    name  = "webserverSecretKey"
    value = var.airflow_secret_key
  }

  set {
    name  = "env[2].name"
    value = "MINIO_SECRET_KEY"
  }

  set {
    name  = "env[2].value"
    value = var.minio_user_service_password
  }

  set {
    name  = "env[3].name"
    value = "TWITTER_BEARER_TOKEN"
  }

  set {
    name  = "env[3].value"
    value = var.TWITTER_BEARER_TOKEN
  }
}

resource "helm_release" "kafka" {

  depends_on = [
    helm_release.airflow,
  ]
  
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "kafka"
  version    = "19.0.0"

  name       = "kafka"
  namespace  = "kafka"
  create_namespace = true
  
  timeout = 600

  values = [
    "${file("./manifests/kafka/values.yaml")}"
  ]
}

resource "helm_release" "mongoDB" {

  depends_on = [
    helm_release.kafka,
  ]
  
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "mongodb"
  version    = "13.1.7"

  name       = "mongodb"
  namespace  = "mongodb"
  create_namespace = true
  
  timeout = 600

  values = [
    "${file("./manifests/mongodb/values.yaml")}"
  ]

  set {
    name  = "auth.rootPassword"
    value = var.mongodb_root_password
  }

  set {
    name = "auth.password"
    value = var.mongodb_user_service_password
  }

}