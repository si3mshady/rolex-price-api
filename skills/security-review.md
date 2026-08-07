# 🛡️ AI Skill: Security Review

## Objective
Audit application code, Docker container build specifications, IAM policy roles, and GitHub Actions permissions for security hardening and compliance with least privilege best practices.

## When the AI Agent Should Use It
- When defining IAM roles, execution policies, or cloud permission scopes.
- When creating or modifying `Dockerfile` container specifications.
- When configuring GitHub Actions workflow permissions (`permissions:` block).

## Required Checks
- [ ] Docker containers execute under unprivileged non-root users (`USER appuser`).
- [ ] IAM roles strictly restrict resource ARNs and actions to minimum required privileges.
- [ ] GitHub Actions workflow permissions explicitly set (`id-token: write`, `contents: read`).
- [ ] No hardcoded secrets, AWS access keys, or API tokens committed to repository.
- [ ] CORS policies, security headers, and input validation schemas correctly configured.

## Expected Output
- Security audit report identifying privilege risks or container vulnerabilities.
- Least-privilege IAM policy definitions in Terraform.
- Hardened Dockerfile and workflow permission declarations.

## Engineering Principles
1. **Least Privilege**: Grant only the minimum permissions required for a service or pipeline step to function.
2. **Defense in Depth**: Secure application at multiple layers (unprivileged user, network isolation, IAM scoping).
3. **Zero Secrets**: Rely on federated identity (OIDC) and runtime secret stores rather than static credentials.
