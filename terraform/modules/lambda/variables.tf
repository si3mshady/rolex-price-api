variable "function_name" {
  type        = string
  description = "Name of the Lambda function"
}

variable "role_arn" {
  type        = string
  description = "ARN of the IAM execution role"
}

variable "package_type" {
  type        = string
  description = "Lambda deployment package type: Image or Zip"
  default     = "Image"
}

variable "image_uri" {
  type        = string
  description = "ECR image URI for container package type"
  default     = null
}

variable "filename" {
  type        = string
  description = "Path to zip file for Zip package type"
  default     = null
}

variable "handler" {
  type        = string
  description = "Function entrypoint for Zip package type"
  default     = null
}

variable "runtime" {
  type        = string
  description = "Runtime environment for Zip package type"
  default     = null
}

variable "timeout" {
  type        = number
  description = "Function execution timeout in seconds"
  default     = 30
}

variable "memory_size" {
  type        = number
  description = "Allocated memory size in MB"
  default     = 512
}

variable "environment_variables" {
  type        = map(string)
  description = "Environment variables for the function"
  default     = {}
}

variable "tags" {
  type        = map(string)
  description = "Tags to apply to Lambda resources"
  default     = {}
}
