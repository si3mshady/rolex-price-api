# 🚚 Pipeline Migration Plan & Workflow Inventory

**Project**: Rolex Price API SaaS  
**Author**: Senior Staff Platform Engineer  
**Status**: Phase 1 & Phase 2 Active (New workflows created alongside legacy workflows)

---

## 1. Workflow Inventory

The table below catalogs all 5 pre-existing GitHub Actions workflows in `.github/workflows/`:

| Workflow File | Name & Purpose | Trigger | Dependencies | Still Needed? | Target Action | Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `terraform-dev-apply.yml` | Monolithic Dev Apply: Infrastructure provisioning, Docker build & push, local container testing, Lambda/APIGW deploy, smoke testing. | `workflow_dispatch`, `push` (`feature/*`, `develop`) | AWS OIDC, Terraform 1.5.7, Docker, Python 3, Curl | Logic needed, structure obsolete | Replace with `deploy-dev.yml` & `scripts/smoke_test.py` | **Deprecated / Production Workflow** |
| `terraform-dev-plan.yml` | Dev Plan: Formats, validates, and plans `terraform/environments/dev`. Contains hardcoded `force-unlock`. | `workflow_dispatch`, `push` (`feature/*`, `develop`) | AWS OIDC, Terraform 1.5.7 | Plan step needed in PRs | Replace with `ci.yml` (PR check) | **Deprecated / Production Workflow** |
| `terraform-bootstrap.yml` | Bootstrap Plan: Validates and plans foundational state bucket & lock table in `terraform/bootstrap`. | `workflow_dispatch`, `push` (`feature/*`, `develop`) | AWS OIDC, Terraform 1.5.7 | No (Bootstrap is complete) | Archive to `.github/workflows/archive/` | **Learning Artifact / One-time Bootstrap** |
| `terraform-bootstrap-apply.yml` | Bootstrap Apply: Provisions S3 bucket `rolex-price-api-tf-state` and DynamoDB `rolex-price-api-tf-locks-dev`. | `workflow_dispatch`, `push` (`feature/*`, `develop`) | AWS OIDC, Terraform 1.5.7 | No (State storage is live) | Archive to `.github/workflows/archive/` | **One-time Bootstrap** |
| `verify-aws-oidc.yml` | OIDC Verification: Inspects GitHub JWT claims and tests `aws sts get-caller-identity`. | `workflow_dispatch`, `push` (`feature/*`, `develop`) | AWS OIDC, `jq`, `aws-cli` | No (Identity federation verified) | Archive to `/docs/learning/` | **Learning Artifact** |

---

## 2. Step-by-Step Migration Plan

```
 Phase 1: Lock & Tag        Phase 2: Add New          Phase 3: Validate           Phase 4: Archive
┌───────────────────┐    ┌──────────────────┐    ┌─────────────────────────┐    ┌──────────────────────────┐
│ Document current  │ -> │ Create ci.yml    │ -> │ Trigger PR & Develop    │ -> │ Archive legacy workflows │
│ state & tag commit│    │ & deploy-dev.yml │    │ pipeline executions     │    │ to archive/ & learning/  │
└───────────────────┘    └──────────────────┘    └─────────────────────────┘    └──────────────────────────┘
```

### Phase 1: Preserve Current Working State (COMPLETE)
- Document baseline architecture and working endpoints.
- Create git tag `v0.1.0-legacy-working` on `develop` branch.
- Keep all pre-existing `.github/workflows/*.yml` files untouched.

### Phase 2: Introduce Consolidated Workflows (COMPLETE)
- Add `.github/workflows/ci.yml`: Validates formatting (`black`), linting (`flake8`), unit tests (`pytest`), Docker dry-run, and Terraform dev plan on PRs.
- Add `.github/workflows/deploy-dev.yml`: Automates Dev Stage 1 apply, ECR push, local container test via `scripts/smoke_test.py`, Dev Stage 2 apply, Lambda validation, and cloud smoke tests on push to `develop`.
- Add `scripts/smoke_test.py`: Modular python smoke test runner.

### Phase 3: Test New Workflow Execution (IN PROGRESS)
- Create feature branch and open Pull Request to test `ci.yml`.
- Merge PR into `develop` to trigger and verify `deploy-dev.yml`.
- Assert end-to-end API Gateway functionality without pipeline lock contention.

### Phase 4: Archive Legacy Workflows (AWAITING USER APPROVAL)
- Move `terraform-bootstrap.yml` and `terraform-bootstrap-apply.yml` to `.github/workflows/archive/`.
- Move `verify-aws-oidc.yml` to `/docs/learning/`.
- Archive old `terraform-dev-apply.yml` and `terraform-dev-plan.yml` once `ci.yml` and `deploy-dev.yml` pass cleanly.

---

## 3. Interview Demonstration Value & SRE Principles

| Workflow Change | Production Problem Solved | SRE / Platform Engineering Principle | Interview Talking Point |
| :--- | :--- | :--- | :--- |
| **Separating CI from CD** | Prevents untested code or failing builds from attempting cloud deployments or holding DynamoDB state locks. | **Fail Fast & Blast Radius Reduction**: Isolate non-mutating checks (lint, unit tests) from mutating cloud operations. | *"In our initial setup, every feature branch push triggered a full Terraform apply, causing state lock contention in DynamoDB. I decoupled PR validation (`ci.yml`) from environment deployment (`deploy-dev.yml`), reducing deployment noise and lock conflicts."* |
| **Keyless OIDC Authentication** | Eliminates static `AWS_ACCESS_KEY_ID` credentials stored in GitHub Secrets. | **Zero Static Credentials & Least Privilege**: Use short-lived, cryptographic STS session tokens scoped to specific repository branches. | *"We eliminated long-lived IAM keys by federating GitHub Actions with AWS IAM via OpenID Connect (OIDC). Workflows assume temporary, scoped session tokens via `AssumeRoleWithWebIdentity`."* |
| **Payload-Level Smoke Testing** | HTTP 200 responses can mask empty JSON bodies or database connection failures. | **Operational Readiness & Shift-Right Testing**: Assert business domain metrics (e.g., `watches_loaded > 0`) post-deployment. | *"Rather than relying on basic HTTP 200 pings, I engineered a Python smoke test runner that parses response JSON structures post-deployment to verify actual data availability."* |
| **Decoupling Custom Scripts** | Multi-line inline bash/python scripts in YAML are difficult to test locally and duplicate across workflows. | **Dry (Don't Repeat Yourself) Pipeline Engineering**: Externalize script logic into standalone, testable CLI tools (`scripts/smoke_test.py`). | *"Embedding 50 lines of inline Python inside GitHub Actions YAML made pipelines unmaintainable. I extracted the logic into a standalone `scripts/smoke_test.py` script usable both locally and in CI/CD."* |

---

## 4. AI Engineering Operating Model & `/skills` Directory

The `/skills` directory provides persistent, version-controlled operational guidance for AI coding agents:

- [`skills/project-init.md`](file:///home/si3mshady/rolex-price-api/skills/project-init.md): Standardizes Python SaaS project layout, virtual environment hygiene, and dependency pinning.
- [`skills/architecture-review.md`](file:///home/si3mshady/rolex-price-api/skills/architecture-review.md): Governs system topology, serverless compute limits, and documentation alignment.
- [`skills/cloud-deployment.md`](file:///home/si3mshady/rolex-price-api/skills/cloud-deployment.md): Controls keyless OIDC auth, immutable container tagging, and two-stage Terraform applies.
- [`skills/testing.md`](file:///home/si3mshady/rolex-price-api/skills/testing.md): Sets standards for unit test suites, integration tests, and payload-level smoke tests.
- [`skills/security-review.md`](file:///home/si3mshady/rolex-price-api/skills/security-review.md): Audits non-root Docker execution, least-privilege IAM policies, and workflow permission blocks.
- [`skills/documentation.md`](file:///home/si3mshady/rolex-price-api/skills/documentation.md): Enforces living architecture docs, ADRs, and post-mortem logs.
