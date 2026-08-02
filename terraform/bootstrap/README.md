# Terraform Bootstrap Layer

This directory contains the foundational Terraform project responsible **only** for provisioning the AWS remote state backend infrastructure.

## Infrastructure Created

- **S3 Bucket**: `rolex-price-api-tf-state-dev`
  - Versioning enabled (protects against state corruption and accidental deletion)
  - Server-side encryption enabled (AES256)
  - Public access fully blocked (`aws_s3_bucket_public_access_block`)
- **DynamoDB Lock Table**: `rolex-price-api-tf-locks-dev`
  - Partition key: `LockID` (String)
  - Billing mode: `PAY_PER_REQUEST` (On-demand)

## Usage

### 1. Initialize Bootstrap Layer Locally
Run with local state initially:

```bash
cd terraform/bootstrap
terraform init
```

### 2. Plan and Apply
```bash
terraform plan -out=tfplan
terraform apply tfplan
```

### 3. Verify Outputs
```bash
terraform output
```

## How Application Environments Consume This Backend

Once the bootstrap layer has been applied, application Terraform layers (e.g., `terraform/environments/dev/backend.tfvars`) consume the backend as follows:

```hcl
bucket         = "rolex-price-api-tf-state-dev"
key            = "dev/terraform.tfstate"
region         = "us-east-1"
dynamodb_table = "rolex-price-api-tf-locks-dev"
encrypt        = true
```
