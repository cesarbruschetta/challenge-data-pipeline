
resource "minikube_cluster" "k8s" {
  driver       = "docker"
  cluster_name = var.cluster_name
  addons = [
    "ingress",
    "registry",
    "metrics-server",
    "csi-hostpath-driver",
  ]
  cpus = 4
  memory = "4094mb"
}

data "kubectl_filename_list" "manifests" {
    pattern = "./manifests/k8s/*.yaml"
}

resource "kubectl_manifest" "this" {
  depends_on = [
    minikube_cluster.k8s,
  ]

  count = length(data.kubectl_filename_list.manifests.matches)
  yaml_body = file(
    element(data.kubectl_filename_list.manifests.matches, count.index)
  )
}

# resource "helm_release" "nfs-server" {

#   depends_on = [
#     kubectl_manifest.this,
#   ]

#   repository = "https://kvaps.github.io/charts"
#   chart      = "nfs-server-provisioner"
#   version    = "1.4.0"

#   name             = "nfs-serve"
#   namespace        = "nfs-serve"
#   create_namespace = true

#   timeout = 600

#   set {
#     name  = "persistence.enabled"
#     value = true
#   }

#   set {
#     name  = "persistence.storageClass"
#     value = "csi-hostpath-driver"
#   }

#   set {
#     name  = "persistence.size"
#     value = "5Gi"
#   }

# }
