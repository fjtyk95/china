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

  name = var.repository_name
}

module "ecs" {
  source = "../../modules/ecs"

  cluster_name   = var.cluster_name
  service_name   = var.service_name
  container_image = "${module.ecr.repository_url}:latest"
  container_port  = var.container_port
  desired_count   = var.desired_count
}

# Simple CodePipeline and CodeBuild for CI/CD
resource "aws_s3_bucket" "pipeline_artifacts" {
  bucket = "${var.service_name}-artifacts"
  force_destroy = true
}

resource "aws_iam_role" "codebuild_role" {
  name = "${var.service_name}-codebuild-role"
  assume_role_policy = data.aws_iam_policy_document.codebuild_assume.json
}

data "aws_iam_policy_document" "codebuild_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["codebuild.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "codebuild_ecr" {
  role       = aws_iam_role.codebuild_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser"
}

resource "aws_codebuild_project" "build" {
  name          = "${var.service_name}-build"
  service_role  = aws_iam_role.codebuild_role.arn
  artifacts { type = "NO_ARTIFACTS" }
  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:7.0"
    type                        = "LINUX_CONTAINER"
    privileged_mode             = true
    environment_variable {
      name  = "REPOSITORY_URI"
      value = module.ecr.repository_url
    }
  }
  source {
    type            = "NO_SOURCE"
    buildspec       = "buildspec.yml"
  }
}

resource "aws_iam_role" "codepipeline_role" {
  name = "${var.service_name}-codepipeline-role"
  assume_role_policy = data.aws_iam_policy_document.codepipeline_assume.json
}

data "aws_iam_policy_document" "codepipeline_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["codepipeline.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "codepipeline_basic" {
  role       = aws_iam_role.codepipeline_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSCodePipelineFullAccess"
}

resource "aws_codepipeline" "pipeline" {
  name     = "${var.service_name}-pipeline"
  role_arn = aws_iam_role.codepipeline_role.arn

  artifact_store {
    location = aws_s3_bucket.pipeline_artifacts.bucket
    type     = "S3"
  }

  stage {
    name = "Source"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "AWS"
      provider         = "S3"
      version          = "1"
      output_artifacts = ["source_output"]
      configuration = {
        S3Bucket = aws_s3_bucket.pipeline_artifacts.bucket
        S3ObjectKey = "source.zip"
      }
    }
  }

  stage {
    name = "Build"

    action {
      name             = "Build"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts  = ["source_output"]
      output_artifacts = ["build_output"]
      version          = "1"
      configuration = {
        ProjectName = aws_codebuild_project.build.name
      }
    }
  }
}

output "ecr_repo_url" {
  value = module.ecr.repository_url
}

output "ecs_service_name" {
  value = module.ecs.service_name
}
