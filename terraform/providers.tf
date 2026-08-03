# ==============================================================================
# AWS Provider Configuration
# ==============================================================================

provider "aws" {
  region = var.aws_region

  # Default tags applied to all AWS resources created by Terraform
  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
