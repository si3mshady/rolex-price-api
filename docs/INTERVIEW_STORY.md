# 🎙️ Senior Platform Engineer Interview Playbook & STAR Stories

This document provides structured **STAR (Situation, Task, Action, Result)** responses for key Senior Platform Engineer and SRE interview scenarios, drawn directly from the **Rolex Price API SaaS** project.

---

## Story 1: Designing and Implementing a Keyless CI/CD Pipeline

### Question
> *"Tell me about a project where you designed and implemented a production-grade CI/CD pipeline."*

### Situation
Our cloud-native Rolex Price API SaaS project suffered from pipeline friction, state lock collisions in DynamoDB, and security risks stemming from monolithic workflow triggers that ran full Terraform applies on every feature branch push.

### Task
As the Senior Staff Platform Engineer, I needed to design a clean, automated, keyless CI/CD pipeline that separated PR validation from environment deployment, eliminated credential leakage risks, and enforced payload-level post-deployment verification.

### Action
1. **Pipeline Decoupling**: Architected a 3-tier delivery model:
   - `ci.yml`: Runs `black`, `flake8`, `pytest` (44 unit/integration tests), Docker dry-run, `terraform plan`, and DevSecOps scanners (`pip-audit`, `Checkov`, `Trivy`) on PRs.
   - `deploy-dev.yml`: Automates Stage 1 Terraform apply, builds/pushes ECR images tagged with `${GITHUB_SHA::8}`, runs local container smoke tests, applies Stage 2, and validates live API Gateway endpoints.
   - `deploy-release.yml`: Deploys to Staging, halts at a GitHub Environment manual approval gate, and promotes to Production upon release tag push (`v*.*.*`).
2. **Keyless Identity Security**: Replaced static AWS access keys in GitHub Secrets with **GitHub OpenID Connect (OIDC)** identity federation, assuming short-lived IAM session roles via `AssumeRoleWithWebIdentity`.
3. **Payload-Level Smoke Testing**: Engineered a standalone Python CLI tool ([`scripts/smoke_test.py`](file:///home/si3mshady/rolex-price-api/scripts/smoke_test.py)) that parses response JSON structures (`status == "healthy"`, `watches_loaded > 0`) to prevent false-positive HTTP 200 checks.

### Result
- Reduced CI/CD build noise and completely eliminated DynamoDB state lock contention (`rolex-price-api-tf-locks-dev`).
- Achieved zero static secret storage in GitHub while enforcing automated shift-left security and post-deployment validation.

---

## Story 2: Preventing Bad Deployments in Production

### Question
> *"How do you prevent bad deployments or broken code from reaching production environments?"*

### Situation
In microservice and serverless architectures, passing unit tests alone do not guarantee that deployed API endpoints will return valid data to end users post-deployment.

### Task
Establish a multi-layered defense-in-depth deployment safety strategy spanning pre-merge checks, IaC plan reviews, automated post-deployment validation, and operational alerting.

### Action
1. **Shift-Left Pull Request Validation**: Enforced mandatory PR status gates in `ci.yml` combining code linting, unit testing (44 tests), non-blocking security scans (`Checkov`, `Trivy`, `pip-audit`), and `terraform plan` execution.
2. **Two-Stage IaC & Immutable Container Tagging**: Deployed containers using immutable git commit SHA tags (`${GITHUB_SHA::8}`) rather than mutable `:latest` tags, guaranteeing exact image traceability.
3. **Payload-Level Smoke Testing**: Post-deployment steps automatically query live API Gateway endpoints (`/health`, `/watches`, `/collections`, `/statistics`) and assert deep JSON schema properties before considering CD successful.
4. **Approval Gates & CloudWatch Alarms**: Enforced manual GitHub Environment approval gates for production deployments, backed by automated CloudWatch metric alarms (`lambda_errors`, `lambda_throttles`, `lambda_high_latency`) and defined 99.9% availability SLO error budgets.

### Result
Zero broken builds or unhandled exceptions reached live endpoints during environment promotion. Broken container builds fail CD locally during smoke testing before Stage 2 API Gateway deployment occurs.

---

## Story 3: AI-Assisted Development & Engineering Guardrails

### Question
> *"How do you leverage AI-assisted development tools without sacrificing code quality or engineering standards?"*

### Situation
AI coding assistants increase velocity but can introduce architectural drift, unvetted dependencies, or inconsistent code style if operating without explicit repository guardrails.

### Task
Establish an AI-assisted development operating model where AI operates as a high-speed engineering assistant within strict human-defined standards and automated quality gates.

### Action
1. **Repository `/skills` Framework**: Created version-controlled AI skill instruction files ([`skills/project-init.md`](file:///home/si3mshady/rolex-price-api/skills/project-init.md), [`skills/cloud-deployment.md`](file:///home/si3mshady/rolex-price-api/skills/cloud-deployment.md), [`skills/testing.md`](file:///home/si3mshady/rolex-price-api/skills/testing.md), etc.) that explicitly instruct AI agents on project rules, unprivileged Docker execution, keyless OIDC auth, and testing expectations.
2. **Clear Division of Responsibility**:
   - **Human Engineer**: Defines system architecture, business requirements, IAM least-privilege boundaries, and approves pull requests.
   - **AI Agent**: Generates boilerplate code, authors pytest unit tests, validates YAML syntax, and updates technical documentation.
3. **Persistent Context & Enforcement**: Maintained living plans ([`docs/plans/`](file:///home/si3mshady/rolex-price-api/docs/plans)) and implementation logs ([`docs/implementation-log.md`](file:///home/si3mshady/rolex-price-api/docs/implementation-log.md)) in git to preserve context across work sessions.

### Result
Achieved a 5x increase in development velocity while maintaining 100% compliance with repository linting, unit test coverage, security policies, and living architectural documentation.
