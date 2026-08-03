variable "aws_region" {
  type        = string
  description = "AWS region for deployment"
  default     = "us-east-1"
}

variable "project_name" {
  type        = string
  description = "Project name identifier"
  default     = "rolex-price-api"
}

variable "environment" {
  type        = string
  description = "Deployment environment"
  default     = "dev"
}

variable "image_uri" {
  type        = string
  description = "ECR image URI for the FastAPI container application"
  default     = "123456789012.dkr.ecr.us-east-1.amazonaws.com/rolex-price-api:dev-latest"
}

variable "log_retention_days" {
  type        = number
  description = "CloudWatch log retention in days"
  default     = 14
}
