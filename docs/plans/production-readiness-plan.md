# 🗺️ Production Readiness Plan & Baseline Assessment

**Project**: Rolex Price API SaaS  
**Author**: Senior Staff Platform Engineer  
**Date**: August 2026  
**Status**: ACTIVE — Implementation Blueprint  

---

## 1. Executive Summary & Purpose

This document serves as a persistent learning artifact and production-readiness roadmap for the **Rolex Price API SaaS** platform. It documents the current baseline architecture, pipeline workflow state, identified engineering gaps, phased implementation schedule, risk mitigations, and interview talking points.

The primary objective is to transform this repository into a **reusable, portfolio-grade SaaS reference template** demonstrating senior platform engineering practices without altering the underlying working application baseline.

---

## 2. Current Baseline Architecture

The system operates as a serverless containerized HTTP API hosted on AWS:

```
[REST Client / Frontend] 
        │
        ▼ (HTTPS REST Calls)
[Amazon API Gateway HTTP API ($default stage)]
        │
        ▼ (Payload Proxy Format v2.0)
[AWS Lambda (FastAPI Container)] ◄─── [AWS Lambda Web Adapter (/opt/extensions/lambda-adapter)]
        │
        ▼ (Read Data Assets)
[Amazon S3 Bucket (rolex-price-api-dev-data)]
        │
        ▼ (Logs & Monitoring)
[Amazon CloudWatch Log Group (/aws/lambda/rolex-price-api-dev-app)]
```

### Key Technical Details
- **Application Engine**: Python 3.12 FastAPI running Uvicorn on port 8000.
- **Containerization**: Multi-stage Docker build running under unprivileged user `appuser` (UID 10001) with AWS Lambda Web Adapter (`v0.8.4`).
- **Infrastructure as Code**: Modular Terraform v1.5.7 (`ecr`, `s3`, `iam`, `cloudwatch`, `lambda`, `api_gateway`).
- **State Storage**: Remote S3 state backend (`rolex-price-api-tf-state`) with DynamoDB locking (`rolex-price-api-tf-locks-dev`).
- **Authentication**: Keyless identity federation via OpenID Connect (GitHub Actions OIDC -> AWS IAM `AssumeRoleWithWebIdentity`).

---

## 3. Current CI/CD Workflow State

The project utilizes 3 consolidated single-responsibility workflows:

1. **[`ci.yml`](file:///home/si3mshady/rolex-price-api/.github/workflows/ci.yml)** (Triggers on PRs to `develop`/`main`):
   - Python format check (`black --check app tests`).
   - Lint inspection (`flake8 app tests`).
   - Pytest unit & integration test suite (39 passing tests).
   - Docker container build dry-run.
   - Terraform format & plan validation.
2. **[`deploy-dev.yml`](file:///home/si3mshady/rolex-price-api/.github/workflows/deploy-dev.yml)** (Triggers on push to `develop`):
   - Stage 1 Terraform Apply (ECR, S3, IAM, CloudWatch).
   - Build & push Docker image to ECR tagged with `${GITHUB_SHA::8}` and `:latest`.
   - Local container smoke test via [`scripts/smoke_test.py`](file:///home/si3mshady/rolex-price-api/scripts/smoke_test.py).
   - Stage 2 Terraform Apply (Lambda & API Gateway using immutable SHA image URI).
   - Direct AWS Lambda invocation check.
   - Cloud smoke test validating deep JSON response fields.
3. **[`deploy-release.yml`](file:///home/si3mshady/rolex-price-api/.github/workflows/deploy-release.yml)** (Triggers on git tags `v*.*.*` or manual dispatch):
   - Deploys to Staging.
   - Halts at `environment: production` manual approval gate in GitHub UI.

---

## 4. Identified Engineering Gaps

| Domain | Current Gap | Impact | Target Enhancement |
| :--- | :--- | :--- | :--- |
| **API Security** | Endpoints lack API Key authentication and request rate limiting. | Vulnerable to abuse/DDoS in production. | Add API Key authorization, Usage Plans, and rate limits in `staging`/`prod`. |
| **Docs Hosting** | Technical blueprints exist only in local markdown files. | Reviewers must clone repository to inspect docs. | Provision S3 static website hosting and automated docs deployment. |
| **Observability** | Only basic CloudWatch log groups exist; no visual metrics or alarms. | Incidents require manual log queries; no proactive alerting. | Build CloudWatch Dashboard and alarms (5XX, latency, throttling, errors). |
| **DevSecOps** | CI pipeline lacks automated security vulnerability scanning. | Security flaws in dependencies or IaC could slip into builds. | Integrate Checkov, Trivy, tfsec, pip-audit, and Infracost into `ci.yml`. |
| **Release Engineering**| Git tags require manual creation; no automated GitHub releases. | Release notes and version history are unmanaged. | Automate semantic versioning, GitHub Releases, and CHANGELOG updates. |
| **Playbook & Audit** | Principles are scattered across multiple markdown files. | Hard to replicate workflow on future applications. | Author `PROJECT_FINAL_AUDIT.md` and `ENGINEERING_PLAYBOOK.md`. |

---

## 5. Phased Implementation Roadmap

Enhancements will be delivered sequentially across short-lived feature branches:

```
 Phase 1: feature/api-security      ➡️ Add API Key Auth, Throttling, & Security Docs
 Phase 2: feature/docs-hosting     ➡️ Add S3 Website Module & Docs Sync Workflow
 Phase 3: feature/observability    ➡️ Add CloudWatch Dashboards, Alarms, & SLI/SLOs
 Phase 4: feature/devsecops        ➡️ Add Checkov, Trivy, tfsec, pip-audit, Infracost
 Phase 5: feature/release-eng      ➡️ Add Semantic Versioning, Releases, & CHANGELOG
 Phase 6: feature/project-audit    ➡️ Add PROJECT_FINAL_AUDIT.md & ENGINEERING_PLAYBOOK.md
```

---

## 6. Commit & Branching Strategy

For each phase:
1. Create a dedicated feature branch from updated `develop` (e.g., `feature/api-security`).
2. Implement focused, single-purpose changes.
3. Open a Pull Request targeting `develop`.
4. Validate CI checks and smoke tests.
5. Merge into `develop` using a clear git commit message (`feat(security): ...`, `feat(observability): ...`).

---

## 7. Risks & Mitigations

1. **API Gateway v2 API Key Constraints**:
   - *Risk*: Standard API Gateway v2 HTTP APIs do not natively support v1 `aws_api_gateway_usage_plan` resources.
   - *Mitigation*: Implement lightweight header validation / Lambda Authorizer in the `api_gateway` module to validate `X-Api-Key` headers without breaking HTTP API v2 low latency.
2. **S3 Website Public Bucket Policies**:
   - *Risk*: Account-level S3 Block Public Access can reject bucket policy creation.
   - *Mitigation*: Explicitly manage `aws_s3_bucket_public_access_block` and scope public read access strictly to the documentation bucket.
3. **CI Pipeline Slowdown from Scanners**:
   - *Risk*: Adding Trivy, Checkov, tfsec, and pip-audit increases PR check time.
   - *Mitigation*: Run security scans in parallel jobs, cache vulnerability DBs, and set non-blocking severity thresholds (`continue-on-error: true`).

---

## 8. Future Interview Talking Points

- **Environment-Specific Security**: *"We kept `dev` unauthenticated to maximize developer velocity while enforcing mandatory API Key authentication and rate limiting in `staging` and `prod`."*
- **Living Static Documentation**: *"To ensure architectural blueprints were accessible to external stakeholders without cloning code, we engineered a Terraform S3 static documentation site synced directly via GitHub Actions."*
- **Shift-Right Observability**: *"We established SLIs for latency and availability, backed by native AWS CloudWatch dashboards and metric alarms that trigger before error budgets are depleted."*
- **DevSecOps Shift-Left**: *"We integrated automated security scanners (Checkov, Trivy, tfsec, pip-audit) into CI to catch infrastructure misconfigurations and dependency CVEs before code reaches code review."*
