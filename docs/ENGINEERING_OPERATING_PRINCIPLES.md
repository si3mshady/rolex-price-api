# 📜 Engineering Operating Principles & Portable Standards

**Project**: Rolex Price API SaaS Platform  
**Version**: `v1.0.0` (Reference Architecture)  
**Role**: Senior Staff Platform Engineer / Cloud Architect  

This playbook codifies **14 core operating principles** extracted from the Rolex Price API reference architecture. These principles are framework-agnostic and apply to any cloud, SaaS, mobile, AI, or serverless application.

---

## 1. Start with the Business Problem
- **Why It Matters**: Technical architecture must serve a clear business purpose, data access model, and user persona.
- **Mistake Prevented**: Over-engineering complex microservices or Kubernetes clusters for simple, low-traffic data access patterns.
- **Rolex Implementation**: Focused on providing fast, predictable REST access (<500ms p95) to Rolex watch catalog pricing and collection statistics.
- **Future Application**: Always document target SLAs, user load, and data requirements before picking cloud compute frameworks.

---

## 2. Build Working Software Before Infrastructure
- **Why It Matters**: Infrastructure should conform to software requirements, not the other way around.
- **Mistake Prevented**: Spending weeks provisioning cloud VPCs and IAM policies before proving application code feasibility.
- **Rolex Implementation**: Built the core FastAPI routes, schemas, and unit tests locally before writing Terraform modules.
- **Future Application**: Deliver a fully testable local HTTP engine with unit test coverage before writing IaC scripts.

---

## 3. Containerize Early
- **Why It Matters**: Containers eliminate "works on my machine" bugs and guarantee identical local and cloud runtime environments.
- **Mistake Prevented**: Environmental drift between local developer machines and cloud deployment runtimes.
- **Rolex Implementation**: Authored a multi-stage Dockerfile (`python:3.12-slim`) executing under non-root `appuser` (UID 10001) with embedded AWS Lambda Web Adapter (`v0.8.4`).
- **Future Application**: Standardize container base images and unprivileged execution models across all microservices.

---

## 4. Use Infrastructure as Code (IaC)
- **Why It Matters**: Manual console clicks cannot be audited, version-controlled, or reliably reproduced.
- **Mistake Prevented**: Hidden configuration drift, lost cloud resources, and un-reproducible environments.
- **Rolex Implementation**: Codified 100% of infrastructure in Terraform v1.5.7 with reusable modules (`ecr`, `iam`, `s3`, `cloudwatch`, `lambda`, `api_gateway`, `s3_website`).
- **Future Application**: Mandate Terraform or OpenTofu for all infrastructure provisioning.

---

## 5. Separate Environments
- **Why It Matters**: Isolating Development, Staging, and Production environments prevents test activity from corrupting live customer data.
- **Mistake Prevented**: Accidental deletion or mutation of production data during feature testing.
- **Rolex Implementation**: Created isolated directories (`terraform/environments/dev` and `prod`) with separate S3 state backends and DynamoDB lock tables.
- **Future Application**: Use environment-specific variables and state files for every deployment target.

---

## 6. Use CI for Validation
- **Why It Matters**: Pull requests must be automatically verified for quality, formatting, unit test pass rates, and security compliance.
- **Mistake Prevented**: Merging broken code, failing unit tests, or syntax errors into main integration branches.
- **Rolex Implementation**: Created [`.github/workflows/ci.yml`](file:///home/si3mshady/rolex-price-api/.github/workflows/ci.yml) to run `black`, `flake8`, `pytest`, `docker build` dry-run, `terraform plan`, and DevSecOps scanners on PRs.
- **Future Application**: Block PR merges until all non-mutating CI validation checks pass 100%.

---

## 7. Use CD for Controlled Deployment
- **Why It Matters**: Deployment to higher environments must be automated, repeatable, and gated by explicit release approvals.
- **Mistake Prevented**: Uncontrolled, manual production pushes or race conditions in deployment pipelines.
- **Rolex Implementation**: Separated [`.github/workflows/deploy-dev.yml`](file:///home/si3mshady/rolex-price-api/.github/workflows/deploy-dev.yml) (auto on `develop`) from [`.github/workflows/deploy-release.yml`](file:///home/si3mshady/rolex-price-api/.github/workflows/deploy-release.yml) (gated by `environment: production` manual approval).
- **Future Application**: Enforce single-responsibility CD workflows triggered by branch merges or version tags.

---

## 8. Use OIDC Instead of Static Credentials
- **Why It Matters**: Static cloud access keys stored in CI/CD secrets invite credential leaks and key management overhead.
- **Mistake Prevented**: Exposed IAM credentials granting permanent administrative cloud access.
- **Rolex Implementation**: Configured GitHub OIDC identity federation (`AssumeRoleWithWebIdentity`), eliminating all long-lived AWS keys from GitHub Secrets.
- **Future Application**: Standardize keyless OIDC identity federation across all cloud platforms (AWS, GCP, Azure).

---

## 9. Automate Security Scanning (DevSecOps)
- **Why It Matters**: Catching dependency CVEs and IaC security misconfigurations early in CI prevents production vulnerabilities.
- **Mistake Prevented**: Deploying vulnerable third-party libraries or overly permissive IAM roles.
- **Rolex Implementation**: Integrated `pip-audit`, `Checkov`, and `Trivy` in `ci.yml` with soft-fail reporting (`continue-on-error: true`).
- **Future Application**: Run shift-left security scanners on every pull request.

---

## 10. Add Observability Before Production
- **Why It Matters**: Production systems require real-time visibility into errors, latency spikes, and traffic volume.
- **Mistake Prevented**: Flying blind during outages and relying on end users to report system failures.
- **Rolex Implementation**: Codified CloudWatch log groups, operational dashboards, metric alarms (`lambda_errors`, `lambda_throttles`, `lambda_high_latency`), and SRE SLO frameworks (`docs/sre-slos.md`).
- **Future Application**: Provision operational dashboards and metric alarms in IaC alongside compute resources.

---

## 11. Create Smoke Tests Based on Business Behavior
- **Why It Matters**: HTTP 200 checks can pass even when backend database queries fail or return empty payloads.
- **Mistake Prevented**: False-positive CI/CD deployment passes when services are degraded.
- **Rolex Implementation**: Authored [`scripts/smoke_test.py`](file:///home/si3mshady/rolex-price-api/scripts/smoke_test.py) to assert response JSON fields (`status == "healthy"`, `watches_loaded > 0`, `total_watches > 0`).
- **Future Application**: Always validate business domain payload contracts post-deployment.

---

## 12. Treat Documentation as a Deployable Artifact
- **Why It Matters**: API documentation stored only in git repositories requires cloning and local setup to inspect.
- **Mistake Prevented**: Out-of-date API documentation and friction for API consumers.
- **Rolex Implementation**: Created [`scripts/generate_docs.py`](file:///home/si3mshady/rolex-price-api/scripts/generate_docs.py) to compile Swagger UI HTML bundles (`docs-site/`) and sync them to `s3://$DOCS_BUCKET/` post-deployment.
- **Future Application**: Publish static interactive documentation websites during automated CD pipelines.

---

## 13. Maintain Audit History
- **Why It Matters**: Recording implementation decisions, problems solved, and architectural trade-offs provides crucial context for future maintainers.
- **Mistake Prevented**: Loss of historical context leading to repeated past mistakes.
- **Rolex Implementation**: Maintained structured implementation logs ([`docs/implementation-log.md`](file:///home/si3mshady/rolex-price-api/docs/implementation-log.md)) and architecture decisions ([`docs/PROJECT_FINAL_AUDIT.md`](file:///home/si3mshady/rolex-price-api/docs/PROJECT_FINAL_AUDIT.md)).
- **Future Application**: Require dated, branch-referenced implementation logs for all major technical milestones.

---

## 14. Use AI Agents with Engineering Guardrails
- **Why It Matters**: AI coding assistants accelerate development velocity but require clear architectural boundaries and automated quality controls.
- **Mistake Prevented**: Uncontrolled AI code drift, unvetted packages, or inconsistent repository structures.
- **Rolex Implementation**: Created version-controlled AI skill specifications in [`skills/`](file:///home/si3mshady/rolex-price-api/skills) and enforced human PR approvals and CI validation gates.
- **Future Application**: Equip AI agents with explicit repository skill instructions and mandatory automated test gates.
