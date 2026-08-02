# S3 remote backend parameters for dev environment
# Usage: terraform init -backend-config=environments/dev/backend.tfvars
bucket         = "rolex-price-api-tf-state-dev"
key            = "dev/terraform.tfstate"
region         = "us-east-1"
dynamodb_table = "rolex-price-api-tf-locks-dev"
encrypt        = true
