# 📘 Staff Engineering Playbook & Portable Principles

**Author**: Senior Staff Platform Engineer  
**Scope**: Reusable Software Delivery & Platform Engineering Standards  

This playbook extracts universal engineering principles from the **Rolex Price API SaaS** project. These practices apply to any SaaS, mobile, serverless, AI, API, or data platform regardless of technology stack.

---

## 1. Project Initialization Workflow

1. **Start with the Problem Domain**: Define application boundaries, data access patterns, and SLA targets before picking cloud services.
2. **Standardize Directory Layout**: Use domain-driven folder structures (`/app`, `/tests`, `/docs`, `/infrastructure`, `/skills`, `/scripts`).
3. **Pin Dependencies**: Enforce explicit version bounds in dependency files (`requirements.txt`, `package.json`, `go.mod`) to eliminate environment drift.
4. **Containerize from Day One**: Author multi-stage Dockerfiles executing under unprivileged non-root users (`USER appuser`).

---

## 2. Git Strategy & Branching Model

```
feature/*  ──► PR (ci.yml) ──► develop (auto-deploy dev) ──► staging ──► main (v*.*.* release)
```

- **Short-Lived Feature Branches**: Branch off `develop` for specific features (`feature/api-security`).
- **PR Gate Validation**: Enforce passing CI checks (formatting, linting, unit tests, IaC plan, security scans) before merging.
- **Environment Promotion**: Promote immutable container tags (`${GITHUB_SHA::8}`) across environments instead of rebuilding artifacts.

---

## 3. AI-Assisted Development & Skills File Strategy

Treat AI coding agents as **high-velocity assistants operating within version-controlled guardrails**:

- **Repository `/skills/` Directory**: Maintain standardized skill instruction files (`project-init.md`, `architecture-review.md`, `cloud-deployment.md`, `testing.md`, `security-review.md`, `documentation.md`).
- **Persistent Context**: Store implementation plans ([`docs/plans/`](file:///home/si3mshady/rolex-price-api/docs/plans)) and implementation logs ([`docs/implementation-log.md`](file:///home/si3mshady/rolex-price-api/docs/implementation-log.md)) in git so AI agents and human engineers maintain shared context.

---

## 4. CI/CD Pipeline Standards

- **Single Responsibility Workflows**: Separate PR validation (`ci.yml`) from mutating environment deployments (`deploy-dev.yml`).
- **Keyless OIDC Identity**: Eliminate long-lived cloud keys in favor of short-lived federated credentials (`AssumeRoleWithWebIdentity`).
- **Decoupled Test Scripts**: Move multi-line inline YAML scripts into standalone CLI tools (`scripts/smoke_test.py`).

---

## 5. Infrastructure as Code (IaC) Standards

- **Environment Agnostic Modules**: Keep modules reusable in `infrastructure/modules/` and pass environment variables via `environments/<env>/main.tf`.
- **Remote State & Locking**: Always store state remotely in encrypted S3 buckets with DynamoDB locking.
- **Two-Stage Apply Pattern**: Model infrastructure initialization stages explicitly when compute depends on container registries.

---

## 6. Security & DevSecOps Practices

- **Least Privilege IAM**: Scope cloud execution roles strictly to required resources and actions.
- **Environment-Tiered Security**: Keep local/dev environments unauthenticated for developer speed while enforcing API key / OAuth authentication in staging and production.
- **Non-Blocking Security Scanners**: Run vulnerability scanners (`pip-audit`, `Checkov`, `Trivy`) in CI with soft-fail reporting (`continue-on-error: true`).

---

## 7. Testing & Observability Standards

- **Payload-Level Smoke Testing**: Assert business domain metrics (e.g., `status == "healthy"`, `records > 0`) post-deployment rather than relying on HTTP 200 pings.
- **Codified Monitoring**: Provision CloudWatch dashboards and metric alarms (`Errors`, `Throttles`, `Duration`) directly in Terraform IaC.
- **SLIs, SLOs, and Error Budgets**: Define 99%+ availability targets and enforce feature freeze policies when 30-day error budgets deplete.

---

## 8. Documentation Standards

- **Living Architecture Docs**: Maintain system blueprints in `/docs` and link them to root markdown files (`ARCHITECTURE.md`, `DEPLOYMENT.md`, `CI_CD.md`, `LESSONS_LEARNED.md`).
- **Public Documentation Hosting**: Host static technical documentation on S3 website buckets for instant stakeholder access without repository cloning.
