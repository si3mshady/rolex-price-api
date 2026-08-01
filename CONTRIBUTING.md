# Contributing to Rolex Price API

Thank you for your interest in contributing to the **Rolex Price API SaaS Platform**! We welcome contributions from engineers of all skill levels. To maintain high standards of code quality, security, reliability, and architecture, please read through the following guidelines before submitting any issues or pull requests.

---

## 📜 Table of Contents

- [Code of Conduct & Core Principles](#-code-of-conduct--core-principles)
- [Development Workflow](#-development-workflow)
  - [Branch Naming Conventions](#branch-naming-conventions)
  - [Commit Message Standard](#commit-message-standard)
- [Environment Setup & Tooling](#-environment-setup--tooling)
- [Code Quality & DevSecOps Standards](#-code-quality--devsecops-standards)
  - [Python Guidelines](#python-guidelines)
  - [Terraform Infrastructure Guidelines](#terraform-infrastructure-guidelines)
  - [Frontend Guidelines](#frontend-guidelines)
- [Testing Guidelines](#-testing-guidelines)
- [Pull Request Process](#-pull-request-process)
- [Security & Vulnerability Reporting](#-security--vulnerability-reporting)

---

## 🤝 Code of Conduct & Core Principles

We adhere to the following core engineering principles:

1. **Security by Design (DevSecOps)**: Zero-trust configuration, least-privilege IAM policies, static code analysis, and secret scanning on every commit.
2. **Reliability & Observability (SRE)**: Design for failure, maintain clear SLAs/SLOs, and ensure metrics, logs, and traces are first-class citizens.
3. **Infrastructure as Code (IaC)**: All infrastructure changes must be declared in Terraform and reviewed via CI/CD. No manual AWS console edits.
4. **Test-Driven Rigor**: Code is not complete without unit, integration, and contract tests maintaining high test coverage (>85%).

---

## 🔄 Development Workflow

### Branch Naming Conventions

All work must be conducted on feature branches branched off `main`. Use descriptive branch names adhering to the following structure:

```bash
<type>/<short-description>
```

**Allowed Types:**
- `feat/`: A new application feature or API endpoint (e.g., `feat/analytics-dashboard`)
- `fix/`: A bug fix (e.g., `fix/jwt-auth-expiry`)
- `infra/`: Terraform or AWS infrastructure updates (e.g., `infra/dynamodb-autoscaling`)
- `ci/`: GitHub Actions pipeline or tooling changes (e.g., `ci/add-checkov-scan`)
- `docs/`: Documentation additions or updates (e.g., `docs/architecture-diagram`)
- `refactor/`: Code restructuring without functional changes (e.g., `refactor/app-layout`)

---

### Commit Message Standard

We enforce the [Conventional Commits specification](https://www.conventionalcommits.org/). Commit messages must be clear and structured:

```bash
<type>(<scope>): <short summary in imperative mood>

[optional body providing rationale and details]

[optional footer(s) referencing issue/PR IDs, e.g. Fixes #42]
```

**Examples:**
- `feat(api): add GET /v1/watches/{id}/history endpoint`
- `fix(auth): handle expired token exception gracefully`
- `infra(terraform): add KMS encryption to DynamoDB price table`
- `ci(github-actions): integrate bandit python security scanner`

---

## 🛠️ Environment Setup & Tooling

### Prerequisites
- **Python**: `^3.12`
- **Terraform**: `^1.7`
- **Node.js**: `^20.x` (for frontend tooling)
- **Docker**: Optional, for local container testing
- **AWS CLI**: `^2.x` (configured with sandbox credentials for local infra testing)

---

## 🛡️ Code Quality & DevSecOps Standards

Before submitting code, ensure all local checks pass.

### Python Guidelines
- **Formatter & Linter**: [Ruff](https://github.com/astral-sh/ruff) (`ruff check .`, `ruff format .`)
- **Type Checking**: [MyPy](https://github.com/python/mypy) (`mypy app tests`)
- **Security Scanner**: [Bandit](https://github.com/PyCQA/bandit) (`bandit -r app/`)

### Terraform Infrastructure Guidelines
- **Formatting**: `terraform fmt -check -recursive terraform/`
- **Linting**: `tflint --recursive`
- **Security & Compliance Scan**: [Checkov](https://github.com/bridgecrewio/checkov) (`checkov -d terraform/`)

### Frontend Guidelines
- **Linter & Formatter**: ESLint and Prettier (`npm run lint`, `npm run format`)

---

## 🧪 Testing Guidelines

Testing is mandatory for all code contributions:
- **Unit Tests**: Test individual components/modules in isolation (`tests/unit/`).
- **Integration Tests**: Test interactions with databases, AWS mocks, or HTTP client handlers (`tests/integration/`).
- **Test Runner**: Pytest (`pytest --cov=app tests/`).
- Code changes must maintain or increase overall test coverage (>85%).

---

## 📥 Pull Request Process

1. **Keep PRs Atomic**: Submit small, focused pull requests rather than multi-purpose monorepos changes.
2. **Self-Review**: Review your own diff, ensure no temporary files or hardcoded credentials are included.
3. **CI Validation**: Ensure all GitHub Actions status checks pass (Linter, Security Scan, Unit Tests, Terraform Validation).
4. **Code Review**: At least one approval from a maintainer is required before merging into `main`.
5. **Merge Strategy**: Squash and merge is preferred to maintain a clean linear commit history on `main`.

---

## 🔐 Security & Vulnerability Reporting

Security issues should **never** be disclosed via public GitHub issues. If you discover a vulnerability:

1. Email security details directly to **security@rolexpriceapi.com** (or contact the repository maintainers privately).
2. Include reproduction steps, affected versions, and potential impact.
3. Allow up to 48 hours for an initial acknowledgment and status update.

Thank you for helping us build a secure, robust, and enterprise-grade SaaS platform!
