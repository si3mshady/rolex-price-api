output "api_gateway_endpoint" {
  description = "Public URL of the API Gateway HTTP API exposing the FastAPI application"
  value       = var.enable_app_services ? module.api_gateway[0].api_endpoint : ""
}

output "lambda_function_name" {
  description = "Name of the deployed Lambda function"
  value       = var.enable_app_services ? module.lambda[0].function_name : ""
}

output "lambda_function_arn" {
  description = "ARN of the deployed Lambda function"
  value       = var.enable_app_services ? module.lambda[0].function_arn : ""
}


output "iam_role_arn" {
  description = "ARN of the Lambda IAM execution role"
  value       = module.iam.role_arn
}

output "cloudwatch_log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = module.cloudwatch.log_group_name
}

output "s3_data_bucket_name" {
  description = "Name of the application S3 storage bucket"
  value       = module.s3.bucket_id
}

output "ecr_repository_url" {
  description = "URL of the ECR container repository"
  value       = module.ecr.repository_url
}

output "docs_website_url" {
  description = "Public URL of the static S3 documentation website"
  value       = module.s3_website.website_url
}

output "docs_bucket_name" {
  description = "Name of the S3 documentation bucket"
  value       = module.s3_website.bucket_id
}

