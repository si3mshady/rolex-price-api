# 📐 AI Skill: Architecture Review

## Objective
Evaluate system topology, component boundaries, serverless compute configurations, and data flow patterns against production stability, security, cost, and maintainability metrics.

## When the AI Agent Should Use It
- Prior to proposing or implementing major architectural modifications.
- When reviewing system documentation (`/docs/architecture.md`) against actual IaC definitions.
- When evaluating performance SLAs, cold-start latency, or operational cost trade-offs.

## Required Checks
- [ ] Architecture diagrams match actual Terraform resource definitions.
- [ ] API endpoints follow standard REST versioning (`/v1/`) and HTTP status semantics.
- [ ] Compute, memory, and timeout parameters are tuned for workload requirements.
- [ ] State storage (databases, S3 buckets) decoupled from compute layers (Lambda).
- [ ] Failure domains and circuit breakers analyzed for external dependencies.

## Expected Output
- Architectural drift report highlighting discrepancies between design docs and implementation.
- Architectural Decision Record (ADR) documenting proposed structural changes.
- Recommendations for performance, cost, and reliability optimizations.

## Engineering Principles
1. **Decoupled Architecture**: Separate compute, storage, and API gateway layers to enable independent scaling and maintenance.
2. **Single Responsibility**: Each service component should own its data access patterns and domain boundary.
3. **Living Documentation**: Keep technical blueprints in lockstep with codebase reality.
