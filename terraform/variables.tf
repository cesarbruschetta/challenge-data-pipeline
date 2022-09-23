variable "cluster_name" {
    type        = string
    description = "Name of the cluster"
    default     = "challenge-data-pipeline"
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