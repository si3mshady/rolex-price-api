# Terraform Architecture Foundation: Rolex Price API (Serverless SaaS)

This directory contains the production-grade Terraform infrastructure foundation for the **Rolex Price API** serverless SaaS application.

---

## Directory Structure

```text
terraform/
├── README.md             # Infrastructure documentation and workflow guide
├── versions.tf           # Core Terraform & AWS provider version requirements
├── providers.tf          # AWS provider configuration & global tags
├── backend.tf            # Remote S3 & DynamoDB backend setup guide/placeholder
├── variables.tf          # Top-level input variable definitions
├── outputs.tf            # Top-level output definitions
├── modules/              # Reusable Terraform infrastructure modules
│   ├── lambda/           # Serverless compute resources (Lambda functions & layers)
│   ├── api_gateway/      # API Gateway HTTP/REST routes & integrations
│   ├── iam/              # Service roles & execution policies
│   ├── cloudwatch/       # Monitoring, alarms, & Log Groups
│   └── s3/               # Object storage buckets & lifecycle rules
└── environments/         # Environment-specific deployment entrypoints
    ├── dev/              # Development environment configurations
    ├── test/             # Staging / Testing environment configurations
    └── prod/             # Production environment configurations
```

---

## Architecture Components

### 1. Root Configuration Files
- **`versions.tf`**: Sets minimum Terraform version (`>= 1.5.0, < 2.0.0`) and AWS provider version (`~> 5.0`).
- **`providers.tf`**: Configures default AWS provider parameters and standard resource tagging (`Project`, `Environment`, `ManagedBy`).
- **`backend.tf`**: Contains guidelines and configuration templates for remote S3 state storage and DynamoDB state locking.
- **`variables.tf`**: Declares root input parameters (region, environment, project name).
- **`outputs.tf`**: Exposes key infrastructure output attributes.

### 2. Modules (`modules/`)
Decoupled, reusable modules designed following AWS and HashiCorp best practices:
- **`lambda`**: AWS Lambda functions, container image support, environment variables, runtime configurations.
- **`api_gateway`**: HTTP/REST API endpoints, CORS policies, stage management.
- **`iam`**: Least-privilege IAM roles and access policies for AWS services.
- **`cloudwatch`**: Log retention policies, metric alarms, and dashboarding.
- **`s3`**: Secure storage buckets with SSE encryption, block public access, and lifecycle management.

### 3. Environments (`environments/`)
Isolation of deployment stages (`dev`, `test`, `prod`) using standard parameter files (`terraform.tfvars`) and backend configurations (`backend.tfvars`).

---

## Remote State Setup Guide

Before deploying infrastructure to AWS, set up the remote backend for shared state and lock management:

1. **Provision S3 & DynamoDB Infrastructure**:
   - **S3 Bucket**: Enable bucket versioning, default AES-256 or KMS encryption, and enable **Block All Public Access**.
   - **DynamoDB Table**: Create a table with a Partition key named `LockID` (type: `String`) for state locking.

2. **Enable Backend Configuration**:
   - Uncomment the `backend "s3"` block in `terraform/backend.tf`.
   - Update `environments/<env>/backend.tfvars` with your AWS Account-specific S3 bucket names.

---

## Terraform Command Workflow

### Initialize Workspace
```bash
# Navigate to the environment directory
cd terraform/environments/dev

# Initialize modules and provider plugins
terraform init -backend-config=backend.tfvars
```

### Validate & Plan
```bash
# Check syntax and configuration validity
terraform validate

# Preview changes against current AWS infrastructure
terraform plan -var-file=terraform.tfvars
```

### Apply Infrastructure
```bash
# Apply infrastructure changes
terraform apply -var-file=terraform.tfvars
```
