# ☁️ AI Skill: Cloud Deployment

## Objective
Govern Infrastructure as Code (IaC) execution, environment promotion, container registry publishing, and keyless cloud authentication to ensure secure, automated, zero-downtime deployments.

## When the AI Agent Should Use It
- When modifying Terraform modules or environment configurations.
- When authoring or updating GitHub Actions deployment pipelines.
- When troubleshooting deployment failures or state locking issues in remote backends.

## Required Checks
- [ ] Terraform code modularized under `/terraform/modules` and environment-agnostic.
- [ ] Remote state stored in S3 with DynamoDB locking enabled.
- [ ] CI/CD authentication uses GitHub OIDC (`role-to-assume`); zero static access keys stored.
- [ ] Image tags use immutable git SHA hashes (`${GITHUB_SHA}`) alongside environment tags (`latest`).
- [ ] Two-stage apply strategy respected when bootstrapping ECR container dependencies.

## Expected Output
- Validated Terraform execution plans without unintended resource destructions.
- Repeatable GitHub Actions workflow YAML files following principle of least privilege.
- Deployment verification logs confirming healthy cloud resource creation.

## Engineering Principles
1. **Infrastructure as Code**: All infrastructure changes must be declared in code, versioned, and applied via CI/CD pipelines.
2. **Keyless Identity**: Eliminate long-lived secrets in favor of short-lived OIDC federated credentials.
3. **Immutable Artifacts**: Build once, tag with commit SHA, and promote the exact same container image across environments.
