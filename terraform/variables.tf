variable "cluster_name" {
    type        = string
    description = "Name of the cluster"
    default     = "challenge-data-pipeline"
}

variable "minio_root_password" {
    type        = string
    description = "Password for the Min.io root user"
    sensitive = true
    default = "11ddbaf3386a"
}

variable "minio_user_service_password" {
    type        = string
    sensitive = true
    default = "82e56b5b54ea2df54bcebcc897bb9f78"
}


