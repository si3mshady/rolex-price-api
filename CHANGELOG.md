# 📋 Changelog

All notable changes to the **Rolex Price API SaaS** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-08-07

### Added
- **Production API Protection**: Environment-specific `X-Api-Key` middleware (`app/main.py`) and API Gateway stage throttling limits (100 req/sec rate limit, 200 burst limit).
- **Security Unit Test Suite**: `tests/test_security.py` validating 401 unauthorized responses, valid headers, and unauthenticated public `/health` probes.
- **S3 Documentation Website**: Terraform module `terraform/modules/s3_website` managing static documentation hosting and public read policies.
- **Automated Documentation Deployment**: GitHub Actions `deploy-dev.yml` post-deployment step syncing `/docs/` contents to S3 website bucket.
- **CloudWatch Dashboards & Alarms**: Terraform-managed operational dashboard and metric alarms for Lambda errors, throttles, p95 latency, and API Gateway 5XX errors (`terraform/modules/cloudwatch`).
- **DevSecOps Pipeline Scanners**: Integrated `pip-audit`, `Checkov`, and `Trivy` security scanners into `.github/workflows/ci.yml`.
- **SRE & Reliability Blueprint**: `docs/sre-slos.md` defining SLIs, SLO targets (99.9% availability, <500ms p95 latency), and Error Budget burn rate policies.
- **Implementation Audit Trail**: `docs/plans/production-readiness-plan.md` and `docs/implementation-log.md`.

### Changed
- **Pipeline Architecture**: Decoupled PR validation (`ci.yml`) from environment deployments (`deploy-dev.yml`), eliminating state lock contention.
- **Container Tagging Strategy**: Updated Lambda deployment to use immutable `${GITHUB_SHA::8}` container image tags.
- **Decoupled Smoke Testing**: Replaced inline YAML scripts with standalone, testable `scripts/smoke_test.py` CLI runner.

### Security
- Keyless AWS OIDC identity federation (`AssumeRoleWithWebIdentity`) active across all deployment jobs.
- Unprivileged Docker container execution under non-root user `appuser` (UID 10001).
