# ==============================================================================
# Environment: Development (dev)
# ==============================================================================
# Entrypoint for deploying the development environment infrastructure.
# Invokes shared modules from ../../modules/ with development-specific settings.
# ==============================================================================

locals {
  name_prefix = "${var.project_name}-${var.environment}"
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# 1. ECR Container Repository
module "ecr" {
  source = "../../modules/ecr"

  repository_name = local.name_prefix
  tags            = local.common_tags
}

# 2. Application S3 Storage Bucket
module "s3" {
  source = "../../modules/s3"

  bucket_name   = "${local.name_prefix}-data"
  force_destroy = true
  tags          = local.common_tags
}

# 2. IAM Execution Role & Policies
module "iam" {
  source = "../../modules/iam"

  role_name     = "${local.name_prefix}-lambda-role"
  s3_bucket_arn = module.s3.bucket_arn
  tags          = local.common_tags
}

# 3. CloudWatch Log Group for Lambda
module "cloudwatch" {
  source = "../../modules/cloudwatch"

  log_group_name    = "/aws/lambda/${local.name_prefix}-app"
  retention_in_days = var.log_retention_days
  tags              = local.common_tags
}

# 4. Lambda Function (FastAPI Container Application)
module "lambda" {
  source = "../../modules/lambda"

  function_name = "${local.name_prefix}-app"
  role_arn      = module.iam.role_arn
  package_type  = "Image"
  image_uri     = var.image_uri

  timeout     = 30
  memory_size = 512

  environment_variables = {
    ENVIRONMENT  = var.environment
    PROJECT_NAME = var.project_name
    LOG_LEVEL    = "DEBUG"
    S3_BUCKET    = module.s3.bucket_id
  }

  tags = local.common_tags

  depends_on = [
    module.cloudwatch,
    module.iam
  ]
}

# 5. API Gateway HTTP API
module "api_gateway" {
  source = "../../modules/api_gateway"

  api_name             = "${local.name_prefix}-http-api"
  lambda_function_name = module.lambda.function_name
  lambda_invoke_arn    = module.lambda.invoke_arn
  environment          = var.environment
  tags                 = local.common_tags
}
