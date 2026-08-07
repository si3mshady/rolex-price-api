# 🚀 Deployment & Operations Guide

**Project**: Rolex Price API SaaS  
**Infrastructure Framework**: Terraform (v1.5.7)  
**CI/CD Engine**: GitHub Actions (Keyless AWS OIDC)  

---

## 🛠️ Prerequisites & Local Setup

- Docker Engine 24.0+
- Python 3.12+
- Terraform 1.5.7
- AWS CLI v2 (for local administrative tasks)

### Local Development Quickstart
```bash
# 1. Clone repository and initialize virtual environment
git clone git@github.com:si3mshady/rolex-price-api.git
cd rolex-price-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Run unit and integration tests
pytest -v

# 3. Launch application server locally
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🏗️ Terraform Infrastructure Structure

The infrastructure is defined under `/terraform`:

```
terraform/
├── bootstrap/               # One-time S3 state bucket & DynamoDB lock table provisioning
├── environments/
│   ├── dev/                 # Active development environment
│   ├── prod/                # Codified production environment
│   └── test/                # Test environment stub
└── modules/
    ├── api_gateway/         # HTTP API Gateway module
    ├── cloudwatch/          # Log Group and retention policies
    ├── ecr/                 # Amazon ECR container repository
    ├── iam/                 # Execution role & least-privilege policies
    ├── lambda/              # Container Lambda function
    └── s3/                  # Application data storage bucket
```

---

## 🔄 Two-Stage Terraform Apply Pattern

To prevent circular dependencies during initial provisioning (where Lambda requires an ECR image URI that cannot exist until ECR is created), deployments use a **Two-Stage Apply**:

### Stage 1: Base Infrastructure
Provisions Amazon ECR, IAM Roles, S3 Buckets, and CloudWatch Log Groups without creating Lambda compute:
```bash
cd terraform/environments/dev
terraform apply -var="enable_app_services=false" -auto-approve
```

### Stage 2: Application Provisioning
After the Docker container image is built and pushed to ECR, Stage 2 provisions Lambda and API Gateway using the immutable image URI (`${GITHUB_SHA::8}`):
```bash
terraform apply -var="enable_app_services=true" -var="image_uri=${IMAGE_URI}" -auto-approve
```

---

## 🧪 Post-Deployment Smoke Testing

Automated smoke tests execute immediately after Stage 2 apply using [`scripts/smoke_test.py`](file:///home/si3mshady/rolex-price-api/scripts/smoke_test.py):

```bash
# Execute smoke tests against deployed API Gateway endpoint
python3 scripts/smoke_test.py --base-url "https://xyz.execute-api.us-east-1.amazonaws.com" --timeout 120
```

The script verifies:
1. `GET /health` ➡️ HTTP 200, `status == "healthy"`, `watches_loaded > 0`.
2. `GET /watches` ➡️ HTTP 200, `total > 0`, `len(items) > 0`.
3. `GET /collections` ➡️ HTTP 200, `total_collections > 0`.
4. `GET /statistics` ➡️ HTTP 200, `total_watches > 0`, `price_stats` key present.

---

## 📚 Static API Documentation Generation & S3 Hosting

The platform provisions a public S3 static website hosting bucket (`rolex-price-api-dev-docs`) via `terraform/modules/s3_website`.

### How Static Documentation Works
1. **OpenAPI Schema Extraction**: FastAPI dynamically generates an OpenAPI 3.1 schema at `/openapi.json`.
2. **Artifact Generation**: [`scripts/generate_docs.py`](file:///home/si3mshady/rolex-price-api/scripts/generate_docs.py) fetches `/openapi.json` from the live API Gateway endpoint (or local FastAPI app) and produces a standalone Swagger UI web bundle in `docs-site/`:
   - `docs-site/openapi.json`: Complete OpenAPI specification.
   - `docs-site/index.html`: Interactive Swagger UI HTML loading `./openapi.json`.
3. **Automated Publishing**: Post-deployment in `.github/workflows/deploy-dev.yml`, `aws s3 sync docs-site/ "s3://$DOCS_BUCKET/" --delete` publishes the documentation site.
4. **Docs Smoke Test**: `scripts/smoke_test.py --docs-url "$DOCS_URL"` verifies `HTTP 200` from `index.html` and `openapi.json`.

### Accessing Documentation
- **Interactive Swagger UI Website**: `http://rolex-price-api-dev-docs.s3-website-us-east-1.amazonaws.com`
- **Raw OpenAPI Spec**: `http://rolex-price-api-dev-docs.s3-website-us-east-1.amazonaws.com/openapi.json`

