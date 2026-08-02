output "s3_bucket_name" {
  description = "Name of the S3 bucket created for Terraform remote state"
  value       = aws_s3_bucket.state.id
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket created for Terraform remote state"
  value       = aws_s3_bucket.state.arn
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table created for state locking"
  value       = aws_dynamodb_table.locks.name
}

output "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table created for state locking"
  value       = aws_dynamodb_table.locks.arn
}

output "backend_config" {
  description = "Terraform backend configuration snippet for environment configurations"
  value = {
    bucket         = aws_s3_bucket.state.id
    region         = var.aws_region
    dynamodb_table = aws_dynamodb_table.locks.name
  }
}
