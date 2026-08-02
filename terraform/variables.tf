# ==============================================================================
# Root Input Variables
# ==============================================================================

variable "aws_region" {
  type        = string
  description = "The AWS region where resources will be deployed."
  default     = "us-east-1"
}

variable "environment" {
  type        = string
  description = "Target deployment environment (e.g., dev, test, prod)."
  default     = "dev"

  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "Environment must be one of: dev, test, prod."
  }
}

variable "project_name" {
  type        = string
  description = "Name of the project used for naming and tagging resources."
  default     = "rolex-price-api"
}
