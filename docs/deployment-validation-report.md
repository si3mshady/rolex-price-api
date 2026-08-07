# 📋 Deployment Validation Report

**Project**: Rolex Price API SaaS  
**Author**: Senior Staff Platform Engineer  
**Date**: August 2026  
**Status**: Validation Phase Complete — Target Architecture Verified  

---

## 1. Pipeline Execution Order & Flow

The newly introduced pipeline separates non-mutating pull request checks from environment deployments, establishing a deterministic delivery flow:

```
[Developer Feature Branch: feature/*]
                   │
                   ▼ (Open Pull Request)
┌─────────────────────────────────────────────────────────────┐
│ 1. CI Workflow (.github/workflows/ci.yml)                   │
│ ├─ Code Format Check (black --check app tests)              │
│ ├─ Lint Check (flake8 app tests)                            │
│ ├─ Unit & Integration Tests (pytest -v)                     │
│ ├─ Docker Container Build Dry-Run                           │
│ └─ Terraform Format & Plan Validation                       │
└─────────────────────────────────────────────────────────────┘
                   │
                   ▼ (PR Merged)
[Integration Branch: develop]
                   │
                   ▼ (Automated Push Trigger)
┌─────────────────────────────────────────────────────────────┐
│ 2. Dev Deployment Workflow (.github/workflows/deploy-dev.yml)│
│ ├─ Terraform Stage 1 Apply (ECR, S3, IAM, CloudWatch)        │
│ ├─ Build & Push Docker Image to ECR (tagged :latest & :sha) │
│ ├─ Local Container Smoke Test (scripts/smoke_test.py)       │
│ ├─ Terraform Stage 2 Apply (Lambda Function & API Gateway)  │
│ ├─ Direct AWS Lambda Invocation Check                       │
│ └─ Cloud Smoke Test (scripts/smoke_test.py against APIGW)  │
└─────────────────────────────────────────────────────────────┘
                   │
                   ▼ (Git Tag v*.*.* or Manual Release)
┌─────────────────────────────────────────────────────────────┐
│ 3. Release Workflow (.github/workflows/deploy-release.yml)  │
│ ├─ Staging Deployment & Validation                          │
│ ├─ 🛑 Production Environment Manual Approval Gate           │
│ └─ Production Infrastructure Promotion                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Execution Time Metrics

| Pipeline Stage | Jobs & Steps Included | Estimated Time | Key Performance Factors |
| :--- | :--- | :--- | :--- |
| **CI Workflow (`ci.yml`)** | Black, Flake8, Pytest (39 tests), Docker Dry-Run, TF Plan | ~1m 30s | Parallel jobs (`lint-and-test`, `docker-validate`, `terraform-validate`), cached pip dependencies. |
| **Deploy Dev (`deploy-dev.yml`)** | Stage 1 Apply, ECR Build/Push, Local Smoke Test, Stage 2 Apply, Cloud Smoke Test | ~4m 15s | Single sequential flow eliminating DynamoDB lock contention; Docker build cached on runner layer. |
| **Deploy Release (`deploy-release.yml`)** | Staging validation, Approval gate, Prod promotion | ~2m 00s + Manual gate duration | Clean decoupling of approval gate from build execution. |

---

## 3. Failures Encountered & Fixes Applied

During local and pipeline validation, 3 critical issues were identified and resolved:

### Issue 1: Monolithic State Lock Contention
- **Symptom**: Simultaneous pushes to `feature/*` and `develop` triggered 5 workflows at once, resulting in `ResourceInUseException` / state lock collisions in DynamoDB (`rolex-price-api-tf-locks-dev`).
- **Fix Applied**: Updated all 5 legacy workflows (`terraform-dev-apply.yml`, `terraform-dev-plan.yml`, `terraform-bootstrap.yml`, `terraform-bootstrap-apply.yml`, `verify-aws-oidc.yml`) to disable automatic `push` triggers (`on: workflow_dispatch:` only).

### Issue 2: Code Formatting Drift (`black`)
- **Symptom**: `black --check app tests` identified 18 unformatted Python files across routers, schemas, services, and test suites.
- **Fix Applied**: Executed `black app tests` locally prior to committing, ensuring 100% formatting compliance in `ci.yml`.

### Issue 3: Inline Shell Script Maintenance Overhead
- **Symptom**: Smoke tests were written as multi-line inline bash/python commands in GitHub Actions YAML, making them fragile and hard to debug.
- **Fix Applied**: Externalized smoke testing into a dedicated, standalone CLI script [`scripts/smoke_test.py`](file:///home/si3mshady/rolex-price-api/scripts/smoke_test.py) that asserts HTTP status codes AND response payload fields (`status == "healthy"`, `watches_loaded > 0`, `total_watches > 0`).

### Issue 4: YAML Syntax Error on Unquoted Step Name (Line 46)
- **Symptom**: `deploy-dev.yml` failed GitHub Actions parser validation on line 46 due to unquoted colon-space (`Base Infra: ECR...`).
- **Fix Applied**: Enclosed the step name in double quotes (`- name: "Terraform Stage 1 Apply (Base Infra: ECR, IAM, S3, CloudWatch)"`) and verified syntax across all workflow files using `pyyaml`.

---

## 4. Verification Checklist Results

- [x] **Lambda Deployment**: AWS Lambda container updates cleanly using ECR image tagged with `${GITHUB_SHA::8}` and `:latest`.
- [x] **API Gateway Payload**: HTTP API Gateway routes requests directly to Lambda via Web Adapter (`/health`, `/watches`, `/collections`, `/statistics`).
- [x] **Payload-Level Smoke Tests**: `scripts/smoke_test.py` validates deep JSON fields, preventing empty HTTP 200 false positives.
- [x] **Race Conditions Eliminated**: Clear branch ownership ensures only `develop` triggers dev deployments.
- [x] **State Lock Stability**: Single active deployment job prevents DynamoDB state lock contention.
- [x] **Production Approval Gate**: `environment: production` defined in `deploy-release.yml` enforces manual approval in GitHub UI.

---

## 5. Remaining Technical Debt

1. **Environment Parity in Terraform**:
   - `terraform/environments/prod` and `test` currently contain simple stubs. While `dev` functions cleanly, promoting to `prod` in Terraform requires instantiating environment variables in `environments/prod/main.tf`.
2. **Pytest Deprecation Warnings**:
   - `starlette._exception_handler` and `fastapi.testclient` emit minor deprecation warnings regarding `HTTP_422_UNPROCESSABLE_ENTITY` and `httpx`.

---

## 6. Recommendations Before Archiving Legacy Workflows

1. **Keep Disabled Triggers Active for 1 Sprint**: Retain the 5 legacy workflows in `.github/workflows/` with `on: workflow_dispatch:` for fallback manual execution if needed.
2. **Archive Strategy**: Once `ci.yml` and `deploy-dev.yml` complete 3 consecutive successful deployment cycles, execute Phase 4:
   - Move `terraform-bootstrap.yml` and `terraform-bootstrap-apply.yml` to `.github/workflows/archive/`.
   - Move `verify-aws-oidc.yml` to `/docs/learning/`.
   - Remove `terraform-dev-apply.yml` and `terraform-dev-plan.yml`.
