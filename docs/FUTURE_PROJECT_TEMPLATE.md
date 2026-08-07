# 📋 Universal Project Checklist & Engineering Template

This document provides a **reusable project initialization checklist** extracted from the Rolex Price API reference architecture. Use this sequence for any SaaS, Mobile, AI, Serverless, API, or Data project.

---

## 🧭 The Core Software Delivery Sequence

```
Problem Definition ──► Architecture Design ──► Working Code ──► Unit Tests ──► Containerization
        │
        ▼
Terraform IaC ──► Keyless CI/CD ──► Shift-Left Security ──► Observability ──► Living Docs ──► Release
```

---

## Phase 1: Problem Definition & Business Context

Before writing code or provisioning infrastructure:

- [ ] **Define User Problem**: What specific friction or manual process does this service solve?
- [ ] **Identify Target Consumer**: Web client, mobile app, internal microservice, or B2B API integration?
- [ ] **Establish SLAs & Targets**: What are the expected request volume, p95 latency target (<500ms), and availability target (99.9%)?
- [ ] **Select Architecture Pattern**: Serverless compute (AWS Lambda), containerized service (ECS/Fargate), or static web app?

---

## Phase 2: Repository Foundation & AI Skill Setup

Initialize the repository structure and AI agent guardrails:

- [ ] **Create Directory Layout**:
  ```
  /app            # Core application domain logic
  /data           # Static assets / seed data
  /docs           # Living documentation & ADRs
  /skills         # AI agent operational guidelines
  /terraform      # Infrastructure as Code modules & environments
  /tests          # Pytest unit & integration test suites
  /scripts        # Standalone CLI tools (smoke tests)
  .github/        # GitHub Actions CI/CD workflows
  ```
- [ ] **Create AI Skill Specifications**:
  - `skills/project-init.md`: Project layout and dependency rules.
  - `skills/cloud-deployment.md`: IaC and keyless OIDC auth rules.
  - `skills/testing.md`: Unit and payload-level smoke test expectations.
  - `skills/security-review.md`: Non-root Docker execution and IAM least-privilege scoping.
- [ ] **Configure Baseline Files**: Add `.gitignore`, `.dockerignore`, `.editorconfig`, `requirements.txt` (pinned versions), and `pytest.ini`.

---

## Phase 3: Build & Validate Local Application

Construct the application engine locally before cloud deployment:

- [ ] **Build Application Logic**: Implement REST endpoints or core domain handlers using standard frameworks (FastAPI, Express, Go standard library).
- [ ] **Include Standard Endpoints**:
  - `GET /health`: Liveness & readiness probe reporting dependency status and record counts.
- [ ] **Write Unit & Integration Tests**: Author unit tests for routers, data parsers, and exception handlers (`pytest`).
- [ ] **Containerize Early**:
  - Multi-stage Dockerfile (`python:3.12-slim` builder + runner).
  - Execute under unprivileged non-root user (`USER appuser`).
  - Native container health check (`HEALTHCHECK`).
- [ ] **Local Validation**: Execute unit tests and verify local container execution (`docker run -p 8000:8000`).

---

## Phase 4: Author Infrastructure as Code (IaC)

Declare cloud infrastructure using environment-agnostic Terraform modules:

- [ ] **Remote State & Locking**: Configure S3 remote backend and DynamoDB state lock table (`terraform/bootstrap`).
- [ ] **Modular Architecture**:
  - `terraform/modules/ecr`: Container registry.
  - `terraform/modules/iam`: Execution roles scoped to minimum required permissions.
  - `terraform/modules/s3`: Encrypted data storage bucket.
  - `terraform/modules/cloudwatch`: Log groups, operational dashboard, and metric alarms.
  - `terraform/modules/lambda`: Compute function using container package type.
  - `terraform/modules/api_gateway`: HTTP API Gateway with route throttling limits (100 req/sec rate limit, 200 burst limit).
  - `terraform/modules/s3_website`: Public static documentation website bucket.
- [ ] **Environment Parity**: Structure environments under `terraform/environments/dev`, `staging`, `prod`.

---

## Phase 5: Build Keyless CI/CD Pipeline

Automate delivery using GitHub Actions:

- [ ] **Keyless OIDC Identity**: Configure GitHub OIDC federation (`sts:AssumeRoleWithWebIdentity`) and restrict permissions (`id-token: write`, `contents: read`).
- [ ] **Decoupled Workflow Model**:
  - `ci.yml`: Runs formatting (`black`), linting (`flake8`), unit tests (`pytest`), Docker dry-run, `terraform plan`, and DevSecOps scanners (`pip-audit`, `Checkov`, `Trivy`) on PRs.
  - `deploy-dev.yml`: Automates Stage 1 apply, builds/pushes ECR image tagged with `${GITHUB_SHA::8}`, runs local container smoke test, applies Stage 2, and validates live endpoints.
  - `deploy-release.yml`: Deploys to Staging, halts at `environment: production` manual approval gate, and publishes automated GitHub Releases upon git tag push (`v*.*.*`).
- [ ] **Decouple Test Scripts**: Use standalone CLI scripts (`scripts/smoke_test.py`) for post-deployment verification asserting JSON payload fields.

---

## Phase 6: Production Security, Observability & Docs

Hardened production controls:

- [ ] **Environment Security**: Enforce API Key authentication (`X-Api-Key`) in higher environments while keeping local `dev` unauthenticated.
- [ ] **CloudWatch Monitoring**: Provision operational dashboard (`Invocations`, `Errors`, `Throttles`, `Duration`) and metric alarms (`lambda_errors`, `lambda_throttles`, `lambda_high_latency`).
- [ ] **SRE SLO Framework**: Define SLIs (Availability, Latency, Error rate), SLO targets (99.9%), and Error Budget burn rate rules (`docs/sre-slos.md`).
- [ ] **Documentation Hosting**: Sync living `/docs/` blueprints to S3 public static website bucket post-deployment.
- [ ] **Release Engineering**: Maintain `CHANGELOG.md` adhering to SemVer and publish automated GitHub Releases.
