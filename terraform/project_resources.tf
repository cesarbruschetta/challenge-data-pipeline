
resource "helm_release" "minio" {
  depends_on = [
    kubectl_manifest.this,
  ]

  repository = "https://charts.min.io/"
  chart      = "minio"
  version    = "5.0.7"

  name             = "minio"
  namespace        = "minio"
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
    name  = "users[0].secretKey"
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
        --tag ${minikube_cluster.k8s.ssh_ip_address}:5000/custom-local-airflow:latest \
        ./manifests/airflow/docker && \
        docker push ${minikube_cluster.k8s.ssh_ip_address}:5000/custom-local-airflow:latest
    EOF
  }
}

resource "helm_release" "airflow" {
  depends_on = [
    null_resource.build-airflow-image,
  ]

  repository = "https://airflow.apache.org"
  chart      = "airflow"
  version    = "1.8.0"

  name             = "airflow"
  namespace        = "airflow"
  create_namespace = true

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

  name             = "kafka"
  namespace        = "kafka"
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

  name             = "mongodb"
  namespace        = "mongodb"
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
    name  = "auth.password"
    value = var.mongodb_user_service_password
  }

}
