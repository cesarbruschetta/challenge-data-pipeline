variable "cluster_name" {
    type        = string
    description = "Name of the cluster"
    default     = "challenge-data-pipeline"
}

variable "registry_port" {
    type        = string
    description = "Port of the registry"
    default     = "5001"
}

variable "nfs_server_storageClass" {
    type        = string
    description = "default storage class for the nfs server"
    default     = "standard"
}

variable "minio_root_password" {
    type        = string
    description = "Password for the Min.io root user"
    sensitive = true
}

variable "minio_user_service_password" {
    type        = string
    sensitive = true
}

variable "airflow_secret_key" {
    type        = string
    sensitive = true
}

variable "TWITTER_BEARER_TOKEN" {
    type        = string
    sensitive = true
}

variable "mongodb_root_password" {
    type        = string
    sensitive = true
}

variable "mongodb_user_service_password" {
    type        = string
    sensitive = true
}
