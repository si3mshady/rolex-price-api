variable "bucket_name" {
  type        = string
  description = "Name of the S3 website bucket"
}

variable "force_destroy" {
  type        = bool
  description = "Whether to force destroy the bucket and all objects upon terraform destroy"
  default     = true
}

variable "tags" {
  type        = map(string)
  description = "Tags to apply to S3 bucket resources"
  default     = {}
}
