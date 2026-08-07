# ⚡ CI/CD Pipeline Architecture & Governance

**Engine**: GitHub Actions  
**Security Model**: OpenID Connect (OIDC) Identity Federation  
**Target Environments**: Dev (`develop`), Staging / Production (`main` / Git Tags)  

---

## 🗺️ Pipeline Governance Overview

The CI/CD delivery pipeline is organized into 3 single-responsibility workflows:

```
                  ┌───────────────────────────────────────────────┐
                  │   Feature Branch Development (feature/*)      │
                  └───────────────────────┬───────────────────────┘
                                          │
                                          ▼ (Open PR to develop)
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. Continuous Integration (ci.yml)                                                      │
│ ├─ Code Format Check (black --check app tests)                                          │
│ ├─ Lint Inspection (flake8 app tests)                                                   │
│ ├─ Unit & Integration Testing (pytest -v)                                               │
│ ├─ Docker Image Build Dry-Run (docker build -f Dockerfile .)                            │
│ └─ Terraform Format & Plan Validation (terraform fmt -check && terraform plan)           │
└─────────────────────────────────────────┬───────────────────────────────────────────────┘
                                          │
                                          ▼ (PR Merged)
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ 2. Deploy Development (deploy-dev.yml)                                                  │
│ ├─ Stage 1 Terraform Apply (ECR, S3, IAM, CloudWatch)                                    │
│ ├─ Build & Push ECR Container Image (Tagged :latest & :${GITHUB_SHA::8})                │
│ ├─ Local Container Smoke Test (scripts/smoke_test.py against http://localhost:8000)    │
│ ├─ Stage 2 Terraform Apply (Lambda & API Gateway with -var="image_uri=...")             │
│ ├─ Validate Direct AWS Lambda Invocation (aws lambda invoke)                            │
│ └─ Cloud Smoke Test (scripts/smoke_test.py against API Gateway endpoint)                │
└─────────────────────────────────────────┬───────────────────────────────────────────────┘
                                          │
                                          ▼ (Git Tag v*.*.* or Release Dispatch)
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ 3. Deploy Release (deploy-release.yml)                                                  │
│ ├─ Staging Environment Deployment & Smoke Test                                          │
│ ├─ 🛑 GitHub Environment Approval Gate (Manual UI Approval for Production)              │
│ └─ Production Environment Infrastructure Promotion                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔑 Security & Keyless Identity

### AWS OIDC Authentication
Zero long-lived credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) are stored in repository secrets. Workflows exchange GitHub Actions JSON Web Tokens (JWT) for short-lived AWS STS session tokens:

```yaml
- name: Configure AWS Credentials via OIDC
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::916923735465:role/OIDC_SAAS
    aws-region: us-east-1
    audience: sts.amazonaws.com
    role-skip-session-tagging: true
```

### GitHub Workflow Permissions
Workflows strictly declare minimum required permissions:
```yaml
permissions:
  id-token: write  # Grants permission to request GitHub OIDC JWT token
  contents: read   # Grants read access to repository code
```

---

## 🏷️ Immutable Container Tagging Strategy

Every container image built during CD is pushed to Amazon ECR with **two tags**:
1. **Immutable Git Commit SHA Tag**: `${REGISTRY}/${REPOSITORY}:${GITHUB_SHA::8}` (Used by Terraform Lambda deployment).
2. **Environment Rolling Tag**: `${REGISTRY}/${REPOSITORY}:latest` (Retained for convenient manual inspection).

This guarantees that every deployment points to an immutable, reproducible container digest.
