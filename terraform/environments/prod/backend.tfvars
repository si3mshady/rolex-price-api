# S3 remote backend parameters for prod environment
# Usage: terraform init -backend-config=environments/prod/backend.tfvars
bucket         = "rolex-price-api-tf-state-prod"
key            = "prod/terraform.tfstate"
region         = "us-east-1"
dynamodb_table = "rolex-price-api-tf-locks-prod"
encrypt        = true
