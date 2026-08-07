# 🏁 Final Project Review & Technical Blueprint

**Project**: Rolex Price API SaaS  
**Version**: `v1.0.0` (Frozen Production Reference Implementation)  
**Role**: Senior Staff Platform Engineer Audit  

---

## 1. Project Evolution Timeline

```
[Kaggle Dataset Script]
       │
       ▼
[FastAPI REST Application (Routers, Schemas, Services)]
       │
       ▼
[Multi-Stage Unprivileged Docker Container]
       │
       ▼
[AWS Lambda Container + AWS Lambda Web Adapter (/opt/extensions/lambda-adapter)]
       │
       ▼
[Amazon API Gateway HTTP API (v2) Ingress]
       │
       ▼
[Modular Infrastructure as Code (Terraform v1.5.7)]
       │
       ▼
[Keyless GitHub OIDC Identity Federation (sts:AssumeRoleWithWebIdentity)]
       │
       ▼
[Decoupled 3-Tier CI/CD Pipeline (ci.yml, deploy-dev.yml, deploy-release.yml)]
       │
       ▼
[Payload-Level Post-Deployment Smoke Testing (scripts/smoke_test.py)]
       │
       ▼
[DevSecOps Pipeline Scanners (pip-audit, Checkov, Trivy) + CloudWatch Observability]
       │
       ▼
[S3 Public Documentation Hosting + Production API Key Security Controls]
```

---

## 2. Major Engineering Challenges & Solutions

### Challenge 1: Terraform Lambda/ECR Circular Dependency
- **Problem**: Deploying an AWS Lambda container function via Terraform (`PackageType = "Image"`) fails if the target Amazon ECR image URI does not exist prior to function provisioning.
- **Root Cause**: Terraform cannot create the Lambda resource without a valid container image digest already present in the remote ECR repository.
- **Solution**: Engineered a **Two-Stage Apply Pattern**:
  - Stage 1 (`enable_app_services=false`) provisions ECR, IAM roles, S3 buckets, and CloudWatch log groups.
  - Docker builds and pushes the initial image to ECR.
  - Stage 2 (`enable_app_services=true`) provisions Lambda and API Gateway using the published image URI.
- **Engineering Principle**: Explicitly model infrastructure dependency stages when serverless compute depends on container registries.

### Challenge 2: AWS Lambda Web Adapter Runtime Execution
- **Problem**: Traditional ASGI serverless wrappers (e.g. Mangum) tie application code directly to AWS Lambda event formats, causing friction during local Uvicorn development.
- **Root Cause**: Vendor-specific event handlers create tight coupling between application logic and cloud provider runtimes.
- **Solution**: Integrated the **AWS Lambda Web Adapter** (`/opt/extensions/lambda-adapter`) into the multi-stage `Dockerfile`. The extension translates incoming Lambda JSON events into HTTP requests sent to Uvicorn running on `0.0.0.0:8000`.
- **Engineering Principle**: Maintain 100% local container fidelity by using runtime sidecars rather than refactoring application code for cloud handlers.

### Challenge 3: Terraform DynamoDB State Lock Contention
- **Problem**: Concurrent GitHub Actions workflow runs triggered `ResourceInUseException` and `ActiveLockExists` errors in DynamoDB (`rolex-price-api-tf-locks-dev`).
- **Root Cause**: 5 separate legacy workflows triggered simultaneously on every push to `feature/*` and `develop`, fighting for state locks.
- **Solution**: Scoped legacy workflows to `on: workflow_dispatch:` and consolidated delivery into 3 distinct, branch-owned pipelines ([`ci.yml`](file:///home/si3mshady/rolex-price-api/.github/workflows/ci.yml), [`deploy-dev.yml`](file:///home/si3mshady/rolex-price-api/.github/workflows/deploy-dev.yml), [`deploy-release.yml`](file:///home/si3mshady/rolex-price-api/.github/workflows/deploy-release.yml)).
- **Engineering Principle**: Isolate non-mutating checks (CI) from mutating cloud operations (CD) to eliminate pipeline friction and lock collisions.

### Challenge 4: CI/CD Workflow Race Conditions
- **Problem**: Feature branch pushes triggered full infrastructure deployments before pull requests were reviewed or unit tests passed.
- **Root Cause**: Overly broad `on: push: branches: ['feature/*']` triggers in deployment workflows.
- **Solution**: Restricted `ci.yml` strictly to PR validation and `deploy-dev.yml` strictly to push events on `develop`.
- **Engineering Principle**: Fail fast in CI before spending time and cloud resources on CD environment provisioning.

### Challenge 5: Environment Separation & Cost Control
- **Problem**: Provisioning 3 active, idle cloud environments (Dev, Staging, Prod) creates unnecessary AWS account charges (~$30+/mo).
- **Root Cause**: Over-provisioning infrastructure for demonstration purposes.
- **Solution**: Maintained **2 active environments (`dev` and `staging`)**, keeping `prod` fully codified in Terraform but unprovisioned by default.
- **Engineering Principle**: Optimize cloud infrastructure for cost-efficiency without compromising environment promotion models or approval gates.

### Challenge 6: Security Hardening & Zero Static Credentials
- **Problem**: Storing static `AWS_ACCESS_KEY_ID` credentials in GitHub Secrets creates severe key leakage risks.
- **Root Cause**: Reliance on legacy long-lived IAM user keys.
- **Solution**: Configured GitHub OIDC identity federation with AWS IAM (`AssumeRoleWithWebIdentity`) and restricted workflow permissions (`id-token: write`, `contents: read`).
- **Engineering Principle**: Eliminate static secrets in favor of short-lived, federated cryptographic identity tokens.
