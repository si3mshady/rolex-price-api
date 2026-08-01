# 🛡️ DevSecOps & Security Architecture Policy

This document outlines the DevSecOps strategy, security controls, static code analysis standards, IAM least-privilege policies, and compliance procedures for the **Rolex Price API**.

---

## 🔒 Security Pillars & Defense-in-Depth

The repository implements a **Shift-Left DevSecOps** model, embedding security checks into every phase of the software development lifecycle (SDLC).

```
   +-------------------+      +-------------------+      +-------------------+
   |   Pre-Commit      | ---> |  CI Build Gate    | ---> |  Production Runtime|
   | (Ruff, Checkov)   |      | (Bandit, SAST)    |      | (KMS, CloudWatch) |
   +-------------------+      +-------------------+      +-------------------+
```

---

## 🛑 Security Controls Matrix

| Domain | Control Mechanism | Tooling / Enforcement |
| :--- | :--- | :--- |
| **Static Application Security Testing (SAST)** | Automated Python code vulnerability scan | `bandit -r app/` in GitHub Actions |
| **Infrastructure as Code (IaC) Scanning** | Policy-as-code security compliance | `checkov -d terraform/` |
| **Secret Detection** | High-entropy token & private key detection | Git secret scanner & GHA secret prevention |
| **Data Encryption at Rest** | Customer-managed KMS encryption keys | AWS KMS applied to DynamoDB & S3 |
| **Data Encryption in Transit** | TLS 1.3 enforced across API Gateway & CloudFront | ACM Certificates + HSTS policy |
| **Identity & Access Management** | Granular IAM roles per Lambda function | AWS IAM Least-Privilege Scoping |
| **Dependency Auditing** | Vulnerability scanning for third-party packages | `pip-audit` / GitHub Dependabot |

---

## 🔑 IAM & Secret Management Rules

1. **No Hardcoded Secrets**: Plaintext passwords, API keys, or AWS secret keys are strictly forbidden in code or Terraform configurations.
2. **KMS Encryption**: All DynamoDB tables and S3 buckets must be encrypted using customer-managed KMS keys with key rotation enabled.
3. **Environment Separation**: Production IAM roles cannot be accessed from Development environments.
