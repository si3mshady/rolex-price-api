# S3 remote backend parameters for test environment
# Usage: terraform init -backend-config=environments/test/backend.tfvars
bucket         = "rolex-price-api-tf-state-test"
key            = "test/terraform.tfstate"
region         = "us-east-1"
dynamodb_table = "rolex-price-api-tf-locks-test"
encrypt        = true
