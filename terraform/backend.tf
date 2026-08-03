# ==============================================================================
# Terraform Remote Backend Configuration Placeholder
# ==============================================================================
# In production setups, Terraform state should be stored remotely in an AWS S3
# bucket with state locking enabled via AWS DynamoDB.
#
# Before enabling this remote backend:
# 1. Provision the S3 bucket and DynamoDB table (manually, via CLI, or via bootstrapper script).
# 2. Ensure S3 bucket has versioning enabled, default SSE-KMS encryption, and public access blocked.
# 3. Ensure DynamoDB table has a primary key named `LockID` (String type).
# 4. Uncomment the `backend "s3"` block below and run `terraform init -migrate-state`.
#
# Command to initialize backend with environment-specific config:
#   terraform init -backend-config=environments/<env>/backend.tfvars
# ==============================================================================

terraform {
  # Remote S3 Backend Configuration
  backend "s3" {
    bucket         = "rolex-price-api-tf-state-dev"
    key            = "dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "rolex-price-api-tf-locks-dev"
    encrypt        = true
  }
}
