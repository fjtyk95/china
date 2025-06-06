module "base" {
  source = "../.."

  aws_region   = var.aws_region
  bucket_name  = var.bucket_name
  db_name      = var.db_name
  db_username  = var.db_username
  db_password  = var.db_password
}

module "ecr" {
  source = "../../modules/ecr"
  name   = var.repository_name
}

module "ecs" {
  source = "../../modules/ecs"
  cluster_name   = var.cluster_name
  service_name   = var.service_name
  container_image = "${module.ecr.repository_url}:latest"
  container_port  = var.container_port
  desired_count   = var.desired_count
}

output "ecr_repo_url" {
  value = module.ecr.repository_url
}

output "ecs_service_name" {
  value = module.ecs.service_name
}
