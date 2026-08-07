variable "log_group_name" {
  type        = string
  description = "Name of the CloudWatch log group"
}

variable "retention_in_days" {
  type        = number
  description = "Log retention period in days"
  default     = 14
}

variable "function_name" {
  type        = string
  description = "Lambda function name for CloudWatch metric alarms and dashboard"
  default     = ""
}

variable "api_name" {
  type        = string
  description = "API Gateway HTTP API name for metric alarms and dashboard"
  default     = ""
}

variable "dashboard_name" {
  type        = string
  description = "Name of the CloudWatch dashboard"
  default     = "rolex-price-api-dashboard"
}

variable "tags" {
  type        = map(string)
  description = "Tags to apply to CloudWatch resources"
  default     = {}
}
