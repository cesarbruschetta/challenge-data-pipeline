terraform {
  required_version = ">= 1.2.8"

  required_providers {
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = "1.14.0"
    }
    minikube = {
      source  = "scott-the-programmer/minikube"
      version = ">= 0.2.4"
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

provider "minikube" {
  kubernetes_version = "v1.23.3"
}

provider "helm" {
  kubernetes {
    host = minikube_cluster.k8s.host

    client_certificate     = minikube_cluster.k8s.client_certificate
    client_key             = minikube_cluster.k8s.client_key
    cluster_ca_certificate = minikube_cluster.k8s.cluster_ca_certificate
  }
}

provider "kubectl" {
  host = minikube_cluster.k8s.host

  client_certificate     = minikube_cluster.k8s.client_certificate
  client_key             = minikube_cluster.k8s.client_key
  cluster_ca_certificate = minikube_cluster.k8s.cluster_ca_certificate

  load_config_file       = false
}
