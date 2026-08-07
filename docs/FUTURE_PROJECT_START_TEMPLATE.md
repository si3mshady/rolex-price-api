# 📐 Universal Future Project Start Template

**Applicable Domains**: SaaS Platforms, Mobile Backends, Serverless Apps, REST/GraphQL APIs, AI Microservices  
**Version**: `v1.0.0` (Reference Delivery Template)  

This template defines the standard **13-stage software engineering lifecycle** for bootstrapping any new technical project from concept to production.

---

## 📋 The 13-Stage Project Lifecycle Checklist

### Stage 1: Business Problem Definition
- [ ] Define user problem, target audience, and core business value.
- [ ] Establish target SLA expectations (Availability: 99.9%, Latency: <500ms p95).

### Stage 2: Functional & Non-Functional Requirements
- [ ] Document core API routes, data schema entities, and access patterns.
- [ ] Specify security requirements (Public, API Key, OAuth2/JWT) per environment.

### Stage 3: Architecture Decision Record (ADR)
- [ ] Select compute pattern (AWS Lambda Container, ECS Fargate, Kubernetes).
- [ ] Document technology stack choices (FastAPI, Python 3.12, Docker, Terraform).

### Stage 4: Local Application Development
- [ ] Scaffold standard directory layout (`/app`, `/data`, `/docs`, `/skills`, `/terraform`, `/tests`, `/scripts`).
- [ ] Implement core business logic, routers, and Pydantic schemas.
- [ ] Implement standard `/health` endpoint reporting system status and catalog records.

### Stage 5: Comprehensive Testing Strategy
- [ ] Write unit tests for routers, data parsers, and services (`pytest`).
- [ ] Achieve >85% code coverage for core business logic.

### Stage 6: Container & Runtime Strategy
- [ ] Write multi-stage Dockerfile (`python:3.12-slim`) executing under non-root `appuser` (UID 10001).
- [ ] Integrate runtime adapters (e.g. AWS Lambda Web Adapter) to maintain 100% local Uvicorn fidelity.

### Stage 7: Modular Infrastructure as Code (IaC)
- [ ] Provision S3 remote state storage bucket and DynamoDB state lock table (`terraform/bootstrap`).
- [ ] Author environment-agnostic modules (`ecr`, `iam`, `s3`, `cloudwatch`, `lambda`, `api_gateway`, `s3_website`).
- [ ] Structure environment definitions in `terraform/environments/dev` and `prod`.

### Stage 8: CI/CD Pipeline Automation
- [ ] Configure keyless GitHub Actions OIDC identity federation (`AssumeRoleWithWebIdentity`).
- [ ] Author `ci.yml` for non-mutating PR validation checks.
- [ ] Author `deploy-dev.yml` for automated Dev deployments upon push to `develop`.
- [ ] Author `deploy-release.yml` with manual approval gates for Staging/Production releases.

### Stage 9: DevSecOps & Shift-Left Security
- [ ] Integrate `pip-audit` for dependency vulnerability auditing.
- [ ] Integrate `Checkov` for IaC security scanning against CIS benchmarks.
- [ ] Integrate `Trivy` for container filesystem vulnerability scanning.

### Stage 10: Observability & Operational Readiness
- [ ] Codify CloudWatch log groups with defined retention policies.
- [ ] Provision CloudWatch operational dashboards and metric alarms (`Errors`, `Throttles`, `Duration`).
- [ ] Document SRE SLIs, SLOs, and Error Budget burn rate policies (`docs/sre-slos.md`).

### Stage 11: Deployable Documentation Architecture
- [ ] Create static docs site generator (`scripts/generate_docs.py`).
- [ ] Automatically publish interactive Swagger UI static documentation (`docs-site/`) to `s3://$DOCS_BUCKET/` in CD.

### Stage 12: Release Engineering & Versioning
- [ ] Maintain `CHANGELOG.md` adhering to Keep a Changelog and Semantic Versioning (`v1.0.0`).
- [ ] Automate GitHub Release creation upon Git tag push (`v*.*.*`).

### Stage 13: Operational Maintenance & FinOps
- [ ] Create automated environment teardown script (`scripts/destroy-environment.sh`).
- [ ] Audit cloud costs and destroy idle non-production compute resources when inactive.
