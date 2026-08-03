variable "role_name" {
  type        = string
  description = "Name of the IAM execution role for Lambda"
}

variable "s3_bucket_arn" {
  type        = string
  description = "Optional S3 bucket ARN for Lambda read/write access"
  default     = ""
}

variable "tags" {
  type        = map(string)
  description = "Tags to apply to IAM resources"
  default     = {}
}
