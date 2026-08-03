output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.app_storage.arn
}

output "bucket_id" {
  description = "ID / Name of the S3 bucket"
  value       = aws_s3_bucket.app_storage.id
}

output "bucket_domain_name" {
  description = "Bucket domain name"
  value       = aws_s3_bucket.app_storage.bucket_domain_name
}
