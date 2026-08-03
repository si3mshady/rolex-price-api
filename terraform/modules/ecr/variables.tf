variable "repository_name" {
  type        = string
  description = "Name of the ECR repository"
}

variable "image_tag_mutability" {
  type        = string
  description = "The tag mutability setting for the repository (MUTABLE or IMMUTABLE)"
  default     = "MUTABLE"

  validation {
    condition     = contains(["MUTABLE", "IMMUTABLE"], var.image_tag_mutability)
    error_message = "image_tag_mutability must be either MUTABLE or IMMUTABLE."
  }
}

variable "scan_on_push" {
  type        = bool
  description = "Indicates whether images are scanned after being pushed to the repository"
  default     = true
}

variable "tags" {
  type        = map(string)
  description = "Tags to apply to ECR resources (Project, Environment, ManagedBy, etc.)"
  default     = {}
}
