variable "aws_region" {
  type        = string
  description = "AWS region for bootstrap infrastructure deployment"
  default     = "us-east-1"
}

variable "project_name" {
  type        = string
  description = "Project name identifier used in resource naming and tagging"
  default     = "rolex-price-api"
}

variable "environment" {
  type        = string
  description = "Target deployment environment"
  default     = "dev"
}

variable "state_bucket_name" {
  type        = string
  description = "Explicit name of the S3 bucket for Terraform remote state"
  default     = "rolex-price-api-tf-state-dev"
}

variable "lock_table_name" {
  type        = string
  description = "Explicit name of the DynamoDB table for Terraform state locking"
  default     = "rolex-price-api-tf-locks-dev"
}
