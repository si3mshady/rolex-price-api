variable "log_group_name" {
  type        = string
  description = "Name of the CloudWatch log group"
}

variable "retention_in_days" {
  type        = number
  description = "Log retention period in days"
  default     = 14
}

variable "tags" {
  type        = map(string)
  description = "Tags to apply to CloudWatch resources"
  default     = {}
}
