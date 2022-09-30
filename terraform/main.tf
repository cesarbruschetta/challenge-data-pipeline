terraform {
  required_version = ">= 1.2.8"

  required_providers {
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.6.0"
    }
  }

  backend "local" {
    path = "./terraform.tfstate"
    
  }

}

provider "helm" {
  kubernetes {
    config_path    = "~/.kube/config"
    config_context = "kind-${var.cluster_name}"
  }
}

resource "null_resource" "k8s" {

  triggers = {
    name = var.cluster_name
  }

  provisioner "local-exec" {
    command = <<EOF
            echo "Creating k8s cluster"
            kind create cluster \
              --name ${self.triggers.name} \
              --config ./manifests/kind_cluster/config.yaml
        EOF
  }

  provisioner "local-exec" {
    when    = destroy
    command = "kind delete clusters ${self.triggers.name}"
  }
}

resource "null_resource" "ingress-nginx" {
  depends_on = [null_resource.k8s]

  provisioner "local-exec" {
    command = <<EOF
      kubectl --context="kind-${var.cluster_name}" \
        apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
    EOF
  }
}

resource "null_resource" "cert-manager" {
  depends_on = [
    null_resource.ingress-nginx,
  ]

  provisioner "local-exec" {
    command = <<EOF
      kubectl --context="kind-${var.cluster_name}" \
        apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.7.3/cert-manager.crds.yaml && \
      kubectl --context="kind-${var.cluster_name}" \
        apply -f https://gist.githubusercontent.com/t83714/51440e2ed212991655959f45d8d037cc/raw/7b16949f95e2dd61e522e247749d77bc697fd63c/selfsigned-issuer.yaml
    EOF
  }
}

resource "null_resource" "metrics-server" {
  depends_on = [
    null_resource.ingress-nginx,
  ]

  provisioner "local-exec" {
    command = <<EOF
      kubectl --context="kind-${var.cluster_name}" \
        apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
    EOF
  }
}

resource "helm_release" "nfs-server" {

  depends_on = [
    null_resource.metrics-server,
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
    value = "standard"
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
    name  = "rootUser"
    value = "root"
  }

  set {
    name  = "rootPassword"
    value = var.minio_root_password
  }

  set {
    name = "users[0].secretKey"
    value = var.minio_user_service_password
  }

}

resource "null_resource" "airflow" {

  depends_on = [
    helm_release.minio,
  ]
  
  provisioner "local-exec" {
    command = <<EOF
      helm --kube-context="kind-${var.cluster_name}" \
        upgrade --install \
        --namespace airflow --create-namespace \
        --debug --values ./manifests/airflow/values.yaml \
        --set env[2].name=MINIO_SECRET_KEY \
        --set env[2].value="${var.minio_user_service_password}" \
        --set env[3].name=TWITTER_BEARER_TOKEN \
        --set env[3].value="${var.TWITTER_BEARER_TOKEN}" \
        --set webserverSecretKey="${var.airflow_secret_key}" \
        airflow apache-airflow/airflow
      EOF
  }
}
