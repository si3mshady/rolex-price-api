output "api_gateway_endpoint" {
  description = "Public URL of the API Gateway HTTP API exposing the FastAPI application"
  value       = module.api_gateway.api_endpoint
}

output "lambda_function_name" {
  description = "Name of the deployed Lambda function"
  value       = module.lambda.function_name
}

output "lambda_function_arn" {
  description = "ARN of the deployed Lambda function"
  value       = module.lambda.function_arn
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
