variable "out_file" {
    default = "builtSource.zip"
}

variable "environment" {
    default = "development"
}

variable "db_port" {
    default = 5432
}

variable "log_level" {
    default = "info"
}

variable "db_host_encoded" {}