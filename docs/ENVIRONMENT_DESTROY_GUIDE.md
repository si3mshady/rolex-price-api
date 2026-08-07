# 🧹 Infrastructure Teardown & Destruction Guide

**Project**: Rolex Price API SaaS Platform  
**Version**: `v1.0.0` (Reference Architecture)  
**Role**: Senior Staff Platform Engineer / Operations  

---

## 1. Overview & When to Destroy

In cloud-native serverless architectures, non-production environments (Dev, Staging, Feature branches) should be torn down when inactive to eliminate unnecessary AWS account charges and prevent environment drift.

Use the automated teardown helper script:
```bash
./scripts/destroy-environment.sh <dev|staging|prod>
```

---

## 2. Infrastructure Dependency Ordering & Teardown Stages

Terraform destruction must be executed in **two reverse stages** to prevent dependency lock errors:

### Stage 1: Destroy Application Compute & Ingress
Target resources: `aws_apigatewayv2_api`, `aws_lambda_function`, `aws_cloudwatch_metric_alarm`.
```bash
terraform destroy -var="environment=dev" -var="enable_app_services=true" -auto-approve
```

### Stage 2: Destroy Base Infrastructure & Registries
Target resources: `aws_ecr_repository`, `aws_s3_bucket` (data & docs), `aws_iam_role`, `aws_cloudwatch_log_group`.
```bash
terraform destroy -var="environment=dev" -var="enable_app_services=false" -auto-approve
```

---

## 3. Preserving State & Preventing Orphaned Resources

### Remote State Backend Preservation
The bootstrap state storage bucket (`rolex-price-api-tf-state-dev`) and DynamoDB lock table (`rolex-price-api-tf-locks-dev`) are managed in [`terraform/bootstrap`](file:///home/si3mshady/rolex-price-api/terraform/bootstrap) and are **NEVER destroyed** by environment teardowns. This ensures historical state logs and lock capabilities remain intact for future provisioning.

### Preventing Orphaned S3 Buckets
Application data buckets (`rolex-price-api-dev-data`) and static docs buckets (`rolex-price-api-dev-docs`) set `force_destroy = true` in Terraform, allowing non-empty buckets to be destroyed cleanly without orphaned object errors.

---

## 4. Cost Management & FinOps Best Practices

- **Zero Compute Idle Charges**: Destroying API Gateway and Lambda reduces compute charges to $0/mo.
- **Minimal S3 Storage Costs**: S3 state storage and DynamoDB pay-per-request locks cost less than $0.05/month when idle.
- **Teardown Automation**: Integrate teardown scripts into branch cleanup workflows when feature branches are deleted or merged.
