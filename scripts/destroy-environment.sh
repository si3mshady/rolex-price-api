#!/usr/bin/env bash
# ==============================================================================
# Rolex Price API - Infrastructure Destruction & Teardown Script
# ==============================================================================
# Safely tears down Terraform-managed AWS resources for a target environment
# while protecting production and preserving remote state backend infrastructure.
# ==============================================================================

set -euo pipefail

ENV="${1:-}"

if [[ -z "$ENV" ]]; then
  echo "❌ ERROR: Environment argument required."
  echo "Usage: ./scripts/destroy-environment.sh <dev|staging|prod>"
  exit 1
fi

if [[ "$ENV" != "dev" && "$ENV" != "staging" && "$ENV" != "prod" ]]; then
  echo "❌ ERROR: Invalid environment '$ENV'. Must be one of: dev, staging, prod."
  exit 1
fi

echo "=========================================================="
echo "⚠️  WARNING: INFRASTRUCTURE DESTRUCTION REQUESTED"
echo "Target Environment: $ENV"
echo "=========================================================="

if [[ "$ENV" == "prod" ]]; then
  echo "🚨 CRITICAL WARNING: YOU ARE ATTEMPTING TO DESTROY PRODUCTION!"
  echo "To confirm, type exact phrase 'DESTROY-PROD-EXPLICITLY':"
  read -r PROD_CONFIRM
  if [[ "$PROD_CONFIRM" != "DESTROY-PROD-EXPLICITLY" ]]; then
    echo "❌ Production destruction aborted. Input did not match required confirmation."
    exit 1
  fi
else
  echo "Are you sure you want to tear down all $ENV resources? (y/N):"
  read -r CONFIRM
  if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
    echo "Destruction cancelled."
    exit 0
  fi
fi

# Determine Terraform working directory
TF_DIR="terraform/environments/dev"
if [[ "$ENV" == "prod" ]]; then
  TF_DIR="terraform/environments/prod"
fi

echo "Initializing Terraform for $ENV environment in $TF_DIR..."
cd "$TF_DIR"

terraform init -backend-config="backend.tfvars" -reconfigure

echo "Step 1: Destroying Application Services (Lambda, API Gateway)..."
terraform destroy -var="environment=$ENV" -var="enable_app_services=true" -auto-approve

echo "Step 2: Destroying Base Infrastructure (ECR, S3, IAM, CloudWatch)..."
terraform destroy -var="environment=$ENV" -var="enable_app_services=false" -auto-approve

echo "=========================================================="
echo "✅ Infrastructure teardown for '$ENV' complete."
echo "Remote S3 state bucket and DynamoDB lock table remain intact."
echo "=========================================================="
