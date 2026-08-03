# ==============================================================================
# Terraform Core & Provider Version Constraints
# ==============================================================================

terraform {
  # Constrain Terraform core version to ensure compatibility and stability
  required_version = ">= 1.5.0, < 2.0.0"

  required_providers {
    # AWS Provider version 5.x for serverless resources
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
