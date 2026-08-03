# ==============================================================================
# Root Outputs
# ==============================================================================
# Define top-level project outputs here as resources and modules are added.
# Examples: API Gateway URLs, S3 bucket names, Lambda function ARNs.
# ==============================================================================

output "aws_region" {
  description = "The AWS region where infrastructure is deployed."
  value       = var.aws_region
}

output "environment" {
  description = "The active deployment environment."
  value       = var.environment
}

output "project_name" {
  description = "The project name prefix."
  value       = var.project_name
}
