# 🏆 Project Final Audit & Architectural Retrospective

**Project**: Rolex Price API SaaS  
**Author**: Senior Staff Platform Engineer  
**Date**: August 2026  
**Final Status**: **PORTFOLIO-GRADE REFERENCE IMPLEMENTATION COMPLETE**  

---

## 1. Project Evolution

The **Rolex Price API SaaS** originated as an AI-assisted cloud deployment exercise, evolving from a simple Kaggle dataset script into an enterprise-style, production-grade serverless API platform:

```
[Kaggle Dataset Tutorial] 
       │
       ▼
[FastAPI REST Application + Docker Containerization]
       │
       ▼
[AWS Lambda Container Deployment + AWS Lambda Web Adapter]
       │
       ▼
[Amazon API Gateway HTTP API Ingress + Modular Terraform IaC]
       │
       ▼
[Keyless GitHub OIDC Federation + Consolidated 3-Tier CI/CD Pipeline]
       │
       ▼
[Shift-Left Security Scanners + CloudWatch Observability + S3 Docs Hosting]
```

---

## 2. Architecture Decisions

| Decision Area | Architectural Choice | Technical Rationale |
| :--- | :--- | :--- |
| **Compute Engine** | AWS Lambda Container (`python:3.12-slim`) | Eliminates idle server costs while scaling automatically from 0 to thousands of requests/sec. |
| **Serverless Adapter** | AWS Lambda Web Adapter (`v0.8.4`) | Allows standard FastAPI / Uvicorn code to run natively inside Lambda without vendor-lock handlers. |
| **API Ingress** | Amazon API Gateway HTTP API (`v2`) | Reduces latency by up to 70% and cuts cost compared to legacy REST APIs. |
| **Data Storage** | Amazon S3 + In-Memory `RolexService` | Fast read performance (<15ms) for watch pricing, collection breakdown, and valuation statistics. |
| **IaC Provisioning** | Modular Terraform 1.5.7 (`ecr`, `s3`, `iam`, `cloudwatch`, `lambda`, `api_gateway`, `s3_website`) | Standardized, reusable infrastructure modules with remote state storage and DynamoDB locking. |
| **Docs Hosting** | Public S3 Static Website (`rolex-price-api-dev-docs`) | Allows reviewers and interviewers to inspect technical blueprints online without local setup. |

---

## 3. Security & Keyless OIDC Identity Model

- **Zero Static Credentials**: Workflows use OpenID Connect (OIDC) identity federation (`sts:AssumeRoleWithWebIdentity`). Zero long-lived `AWS_ACCESS_KEY_ID` secrets are stored in GitHub.
- **Unprivileged Execution**: Docker container executes under non-root user `appuser` (UID 10001).
- **Environment API Key Security**: `app/main.py` enforces `X-Api-Key` header checking in `staging` and `prod` while keeping local/dev testing friction-free.
- **Stage Throttling**: API Gateway default stage rate limit set to 100 req/sec (200 burst limit) to mitigate DoS attacks.

---

## 4. CI/CD & Delivery Pipeline Design

```
Feature Branch (feature/*) ──► PR ──► ci.yml (Lint, Pytest, Docker Build, TF Plan, DevSecOps)
                                       │
                                       ▼ (Merged)
Develop Branch (develop) ───────────► deploy-dev.yml (TF Stage 1 -> ECR Push -> TF Stage 2 -> Smoke Test -> S3 Docs Sync)
                                       │
                                       ▼ (Git Tag v*.*.*)
Main Branch (main) ─────────────────► deploy-release.yml (Staging Deploy -> 🛑 Approval Gate -> Prod Deploy -> Release)
```

---

## 5. Testing & Post-Deployment Smoke Test Approach

- **Unit & Integration Suite**: 44 passing `pytest` tests in [`tests/`](file:///home/si3mshady/rolex-price-api/tests) covering health, catalog, collections, search, statistics, and API key security.
- **Payload-Level Smoke Testing**: Externalized CLI script [`scripts/smoke_test.py`](file:///home/si3mshady/rolex-price-api/scripts/smoke_test.py) validates HTTP 200 AND deep JSON fields (`status == "healthy"`, `watches_loaded > 0`, `total_watches > 0`).

---

## 6. Observability & Operational Readiness

- **CloudWatch Dashboard**: [`terraform/modules/cloudwatch`](file:///home/si3mshady/rolex-price-api/terraform/modules/cloudwatch) provisions `rolex-price-api-dev-dashboard` visualizing Invocations, Errors, Throttles, and Avg/p95/p99 Duration.
- **CloudWatch Alarms**: Automated alarms for Lambda errors (`lambda_errors`), execution throttles (`lambda_throttles`), and p95 high latency (`lambda_high_latency`).
- **SRE SLO Framework**: [`docs/sre-slos.md`](file:///home/si3mshady/rolex-price-api/docs/sre-slos.md) defines 99.9% availability target and error budget burn rate policies.

---

## 7. Senior Platform Engineer Interview Talking Points

1. **Keyless OIDC Identity**: *"We eliminated long-lived IAM keys by federating GitHub Actions with AWS IAM via OpenID Connect. Workflows assume temporary, scoped session tokens dynamically."*
2. **Two-Stage Terraform Applies**: *"To resolve circular dependencies between Lambda functions and ECR repositories during initial provisioning, we structured Terraform into Stage 1 (Base infra) and Stage 2 (Lambda & API Gateway)."*
3. **AWS Lambda Web Adapter**: *"By using the AWS Lambda Web Adapter, we maintained 100% local container fidelity with Uvicorn while benefiting from serverless auto-scaling in AWS."*
4. **Payload-Level Smoke Testing**: *"Rather than relying on basic HTTP 200 pings, our post-deployment smoke test script parses JSON response structures to verify actual data catalog load status."*
5. **Environment-Tiered API Protection**: *"We kept `dev` unauthenticated to maximize developer velocity, while enforcing API Key authentication and stage rate limits in higher environments."*
