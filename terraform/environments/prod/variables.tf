variable "aws_region" { type = string }
variable "bucket_name" { type = string }
variable "db_name" { type = string }
variable "db_username" { type = string }
variable "db_password" { type = string }
variable "repository_name" { type = string }
variable "cluster_name" { type = string }
variable "service_name" { type = string }
variable "container_port" { type = number default = 80 }
variable "desired_count" { type = number default = 1 }
