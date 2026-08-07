# 🎯 Senior Staff Platform Engineer Interview Playbook & Criteria Audit

**Project**: Rolex Price API SaaS Platform  
**Target Roles**: Senior Staff Platform Engineer, Lead Cloud Architect, Principal SRE  
**Version**: `v1.0.0` (Reference Architecture)  

---

## 1. LinkedIn Engineering Criteria Self-Audit

### A. Real Business Problem
- **Use Case**: Delivers real-time and historical secondary market valuation, retail pricing, collection breakdowns, and search capabilities for high-value luxury timepieces.
- **Value**: Replaces fragmented data scraping with a high-performance (<500ms p95), reliable B2B REST API.

### B. End-to-End Engineering Traceability
- **Data Layer**: Cleaned JSON catalog dataset (`rolex_watches.json`) loaded into memory via `RolexService`.
- **Application Layer**: Modular FastAPI application with Pydantic validation schemas, dependency injection, and security middleware.
- **Deployment Layer**: Unprivileged Docker container running under AWS Lambda Web Adapter, provisioned via modular Terraform IaC.
- **Monitoring Layer**: CloudWatch operational dashboards, metric alarms, and SRE SLO frameworks.
- **Operations Layer**: Keyless OIDC CI/CD pipelines, automated S3 documentation publishing, and FinOps environment teardown scripts.

### C. Production Readiness Audit
- **Automated Testing**: 44 unit and integration tests passing (`pytest`).
- **Deployment Automation**: Single-command CD pipelines with post-deployment payload smoke testing.
- **Security Hardening**: Non-root container execution (UID 10001), API Gateway stage rate limits, and `X-Api-Key` middleware.
- **Cost Awareness**: Idle $0 compute costs by using serverless Lambda containers; unprovisioned Staging/Prod environments saved ~$30/mo.

---

## 2. Senior Architectural Tradeoff Justifications

### Why AWS Lambda Containers Instead of Kubernetes (EKS)?
- **Tradeoff**: Kubernetes introduces ~$$70-\$150/mo fixed control plane costs, cluster management overhead, and ingress controller complexity.
- **Decision**: AWS Lambda containers scale from 0 to thousands of requests/sec with zero idle compute cost, ideal for bursty SaaS API workloads.

### Why S3 Data Storage Instead of DynamoDB for Initial V1?
- **Tradeoff**: DynamoDB offers low-latency key-value querying but increases initial schema design overhead for static dataset reads.
- **Decision**: Loading a static ~900 watch catalog dataset into memory from S3 yields sub-15ms query response times while keeping architectural complexity minimal.

### Why Amazon API Gateway HTTP API (v2) Instead of REST API (v1)?
- **Tradeoff**: HTTP APIs lack legacy features like client certificates or built-in response transformations.
- **Decision**: HTTP API (v2) provides 70% lower latency, 70% cost reduction, and native CORS support ideal for modern ASGI container applications.

---

## 3. Core Engineering Fundamentals Interview Q&A

### Q1: Explain the OpenID Connect (OIDC) Authentication Flow in GitHub Actions
> *"We eliminated static `AWS_ACCESS_KEY_ID` secrets by configuring GitHub Actions as an OIDC identity provider. When a workflow executes, GitHub issues a short-lived, signed JSON Web Token (JWT). The `aws-actions/configure-aws-credentials` action exchanges this JWT with AWS STS using `sts:AssumeRoleWithWebIdentity`. AWS verifies GitHub's OIDC issuer signature and returns a 1-hour temporary IAM session credential with permissions strictly scoped to our deployment role."*

### Q2: How Does Terraform State Locking Work and Why Is It Necessary?
> *"Terraform state locking prevents concurrent pipeline runs from corrupting shared infrastructure state files. When a pipeline executes `terraform apply` or `plan`, Terraform writes a lock record containing a unique `LockID` string to an Amazon DynamoDB table (`rolex-price-api-tf-locks-dev`). Subsequent concurrent pipeline runs attempting to modify the same environment fail fast with a `LockError` until the active operation completes and releases the DynamoDB lock."*

### Q3: Why Decouple CI Validation Workflows from CD Deployment Pipelines?
> *"Running full infrastructure deployments on every feature branch push creates severe lock contention in DynamoDB, increases cloud costs, and slows developer feedback. We restricted `ci.yml` strictly to non-mutating checks (formatting, unit tests, DevSecOps scans, `terraform plan`) on PRs, while scoping mutating cloud deployments (`deploy-dev.yml`) strictly to merged commits on `develop`."*

### Q4: How Do You Execute Deployment Rollbacks in a Serverless Container Architecture?
> *"Because Lambda functions deploy using immutable container image tags (`${GITHUB_SHA::8}`), rolling back requires re-applying Terraform with the previous working commit SHA tag (`image_uri = $REGISTRY/rolex-price-api-dev:<PREVIOUS_STABLE_SHA>`). This updates the Lambda function code pointer in under 3 minutes without rebuilding container artifacts."*

### Q5: What Is the Difference Between Payload-Level Smoke Testing and HTTP 200 Pings?
> *"Basic HTTP 200 status checks pass even when endpoints return empty JSON arrays or unhandled error messages. Our post-deployment smoke test script (`scripts/smoke_test.py`) parses response payloads and validates domain contracts—confirming `status == 'healthy'`, `watches_loaded > 0`, and `total_watches > 0` before declaring deployment success."*
