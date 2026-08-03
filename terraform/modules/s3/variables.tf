variable "bucket_name" {
  type        = string
  description = "Name of the S3 bucket"
}

variable "force_destroy" {
  type        = bool
  description = "Boolean indicating whether all objects should be deleted when bucket is destroyed"
  default     = false
}

variable "tags" {
  type        = map(string)
  description = "Tags to apply to S3 resources"
  default     = {}
}
