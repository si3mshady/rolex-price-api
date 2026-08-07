variable "api_name" {
  type        = string
  description = "Name of the HTTP API Gateway"
}

variable "lambda_function_name" {
  type        = string
  description = "Name of the target Lambda function"
}

variable "lambda_invoke_arn" {
  type        = string
  description = "Invoke ARN of the target Lambda function"
}

variable "environment" {
  type        = string
  description = "Deployment environment"
  default     = "dev"
}

variable "tags" {
  type        = map(string)
  description = "Tags to apply to API Gateway resources"
  default     = {}
}

variable "throttling_burst_limit" {
  type        = number
  description = "Throttling burst limit for default stage"
  default     = 200
}

variable "throttling_rate_limit" {
  type        = number
  description = "Throttling rate limit (requests per second) for default stage"
  default     = 100
}

