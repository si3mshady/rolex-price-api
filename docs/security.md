# 🛡️ DevSecOps & Security Architecture Policy

This document outlines the DevSecOps strategy, security controls, API authentication flow, rate limiting policy, and IAM identity controls for the **Rolex Price API**.

---

## 🔑 Production API Protection Strategy

The platform implements environment-tiered API access control to balance developer velocity in lower environments with strict access protection in staging and production.

| Environment | Authentication Policy | Enforcement Mechanism | Rate Limiting Policy |
| :--- | :--- | :--- | :--- |
| **Development (`dev`)** | **Public / Unauthenticated** | Fast local testing; `API_KEY_REQUIRED=False` | Burst: 200 req, Rate: 100 req/sec |
| **Staging (`staging`)** | **API Key Required** | `X-Api-Key` header validation (`API_KEY_REQUIRED=True`) | Burst: 200 req, Rate: 100 req/sec |
| **Production (`prod`)** | **API Key Required** | `X-Api-Key` header validation + WAF protection | Burst: 200 req, Rate: 100 req/sec |

---

## 📡 API Authentication Flow & Client Usage

### Header Specification
Clients requesting protected endpoints (`/watches`, `/collections`, `/search`, `/statistics`) must provide a valid API key in the `X-Api-Key` HTTP header. The `/health` liveness probe remains unauthenticated across all environments for load balancer health checking.

```http
GET /v1/watches HTTP/1.1
Host: api.rolex.example.com
X-Api-Key: rolex-api-secret-key
Accept: application/json
```

### Client Request Examples

#### cURL
```bash
curl -H "X-Api-Key: rolex-api-secret-key" \
  "https://api.rolex.example.com/watches?collection=Submariner"
```

#### Python (`httpx` / `requests`)
```python
import requests

headers = {"X-Api-Key": "rolex-api-secret-key"}
response = requests.get("https://api.rolex.example.com/watches", headers=headers)
print(response.json())
```

---

## 🚦 Rate Limiting & Throttling Limits

Rate limiting is enforced at the **Amazon API Gateway $default Stage** level to prevent Denial of Service (DoS) attacks and downstream resource exhaustion:

- **Throttling Rate Limit**: 100 requests per second.
- **Throttling Burst Limit**: 200 requests.
- **Error Response**: HTTP 429 (`Too Many Requests`) returned automatically by API Gateway when limits are exceeded.

---

## 🔮 Future Auth Migration Path (OAuth2 / JWT / AWS Cognito)

As the SaaS platform scales, API Key authentication will transition to identity-based OAuth2 / JWT authentication:

```
[Client App] ───(1. Authenticate)───► [AWS Cognito / Auth0]
     │                                       │
     │ (2. Returns JWT Token) ───────────────┘
     ▼
[API Gateway HTTP API] ───(3. Validate JWT)───► [JWT Authorizer] ───► [FastAPI Lambda]
```

1. **Phase 1 (Current)**: API Key header checking for B2B API access.
2. **Phase 2 (Planned)**: AWS Cognito User Pools issuing RS256 JWT tokens.
3. **Phase 3 (Enterprise)**: API Gateway native JWT Authorizer (`aws_apigatewayv2_authorizer`) performing key rotation and scope validation at ingress.

---

## 🛑 Security Controls Matrix

| Domain | Control Mechanism | Tooling / Enforcement |
| :--- | :--- | :--- |
| **Static Code Scanning** | Automated Python code vulnerability scan | `bandit` / `flake8` in GitHub Actions |
| **IaC Security Scanning** | Terraform policy compliance scanning | `checkov` / `tfsec` in CI pipeline |
| **Dependency Security** | Third-party package vulnerability audit | `pip-audit` / GitHub Dependabot |
| **Keyless Identity** | Short-lived STS session assumption | OpenID Connect (GitHub OIDC -> AWS IAM) |
| **Unprivileged Container** | Execution under non-root user | Dockerfile `USER appuser` (UID 10001) |
