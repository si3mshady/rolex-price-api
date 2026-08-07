output "bucket_id" {
  description = "ID of the S3 website bucket"
  value       = aws_s3_bucket.website.id
}

output "bucket_arn" {
  description = "ARN of the S3 website bucket"
  value       = aws_s3_bucket.website.arn
}

output "website_endpoint" {
  description = "Public HTTP S3 static website endpoint"
  value       = aws_s3_bucket_website_configuration.website.website_endpoint
}

output "website_url" {
  description = "Website URL with HTTP scheme"
  value       = "http://${aws_s3_bucket_website_configuration.website.website_endpoint}"
}
