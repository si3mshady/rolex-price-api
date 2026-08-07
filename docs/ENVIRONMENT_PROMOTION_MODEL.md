# 🚀 Environment Promotion Model & Deployment Runbook

**Project**: Rolex Price API SaaS Platform  
**Version**: `v1.0.0` (Reference Architecture)  
**Role**: Senior Staff Platform Engineer / Cloud Architect  

---

## 1. Current Deployed State vs. Environment Architecture

The Rolex Price API platform uses a 3-tier environment progression model (**Dev ➡️ Staging ➡️ Production**):

| Environment | Deployed State | Active AWS Compute / API Gateway | Backend S3 State Bucket | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Dev** | **ACTIVE** | `rolex-price-api-dev-app` <br> `rolex-price-api-dev-http-api` | `rolex-price-api-tf-state-dev` | Rapid feature integration, automated PR deployments, unauthenticated testing. |
| **Staging** | **CODIFIED** | *Unprovisioned by default to prevent idle AWS costs* | `rolex-price-api-tf-state-staging` | Pre-release validation, load testing, integration with production-like security. |
| **Prod** | **CODIFIED** | *Unprovisioned by default; requires approval gate* | `rolex-price-api-tf-state-prod` | Live user traffic, high availability, rate limiting, and API key authorization. |

---

## 2. Staging Environment Activation Process

To provision and activate the **Staging** environment:

### Step 1: Initialize Terraform Staging Backend
```bash
cd terraform/environments/dev
terraform init -backend-config="bucket=rolex-price-api-tf-state-staging" \
               -backend-config="key=staging/terraform.tfstate" \
               -backend-config="dynamodb_table=rolex-price-api-tf-locks-staging" \
               -reconfigure
```

### Step 2: Stage 1 Apply (Base Infrastructure)
```bash
terraform apply -var="environment=staging" -var="enable_app_services=false" -auto-approve
```
*Resources Provisioned*:
- ECR Repository: `rolex-price-api-staging`
- IAM Execution Role: `rolex-price-api-staging-lambda-role`
- Application S3 Bucket: `rolex-price-api-staging-data`
- S3 Documentation Bucket: `rolex-price-api-staging-docs`
- CloudWatch Log Group: `/aws/lambda/rolex-price-api-staging-app` (Retention: 14 days)

### Step 3: Build & Push Staging Container Image
```bash
REGISTRY="916923735465.dkr.ecr.us-east-1.amazonaws.com"
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin "$REGISTRY"
docker build -t "$REGISTRY/rolex-price-api-staging:v1.0.0" -f Dockerfile .
docker push "$REGISTRY/rolex-price-api-staging:v1.0.0"
```

### Step 4: Stage 2 Apply (Compute, Ingress & Security)
```bash
terraform apply -var="environment=staging" \
                -var="enable_app_services=true" \
                -var="image_uri=$REGISTRY/rolex-price-api-staging:v1.0.0" \
                -auto-approve
```
*Resources Provisioned*:
- Lambda Function: `rolex-price-api-staging-app` (512MB RAM, 30s timeout)
- API Gateway HTTP API (v2): `rolex-price-api-staging-http-api`
- CloudWatch Operational Dashboard: `rolex-price-api-staging-dashboard`
- CloudWatch Metric Alarms: `errors-alarm`, `throttles-alarm`, `high-latency-alarm`

---

## 3. Production Environment Activation & Promotion Model

Production promotion is driven entirely by Git tag releases (`v*.*.*`) in [`.github/workflows/deploy-release.yml`](file:///home/si3mshady/rolex-price-api/.github/workflows/deploy-release.yml).

### Step 1: Release Tag Push Trigger
Creating and pushing a Git release tag initiates the release pipeline:
```bash
git checkout main
git tag -a v1.0.0 -m "Release v1.0.0: Production Baseline"
git push origin main --tags
```

### Step 2: Automated Staging Deployment & Verification
The `deploy-staging` job in `deploy-release.yml` executes:
1. Initializes Staging backend.
2. Validates infrastructure plan (`terraform plan`).
3. Executes post-deployment smoke tests via `scripts/smoke_test.py`.

### Step 3: Manual Approval Gate (`environment: production`)
The pipeline pauses before the `deploy-production` job. A designated Lead Platform Engineer must review the release diff and manually click **Approve and Deploy** in GitHub Actions.

### Step 4: Production Provisioning Sequence
Upon approval, the pipeline executes Terraform in `terraform/environments/prod`:
```bash
cd terraform/environments/prod
terraform init -backend-config=backend.tfvars
terraform apply -var="image_uri=$REGISTRY/rolex-price-api-prod:v1.0.0" -auto-approve
```

### Required Production Security Controls
- **Mandatory API Key**: `API_KEY_REQUIRED=true` enforced in `app/main.py`. Incoming requests must supply valid `X-Api-Key` headers (except `/health`).
- **Stage Throttling**: API Gateway default stage rate limit set to 100 req/sec (200 burst limit).
- **Keyless OIDC Identity**: Deployment uses GitHub OIDC `id-token: write` permissions; zero static keys exist in GitHub Secrets.

---

## 4. Rollback Strategy

If a production deployment fails cloud smoke testing or triggers CloudWatch metric alarms:

1. **Immediate Container Reversion (TTR < 3 mins)**:
   Re-apply Terraform pointing `image_uri` back to the previous stable release SHA tag:
   ```bash
   terraform apply -var="image_uri=$REGISTRY/rolex-price-api-prod:<PREVIOUS_STABLE_SHA>" -auto-approve
   ```
2. **Git Revert**:
   Revert the release commit on `main` and push a patch release tag (`v1.0.1`).
