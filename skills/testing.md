# 🧪 AI Skill: Automated & Smoke Testing

## Objective
Establish high-confidence testing strategies spanning fast unit tests, API integration tests, local container validation, and post-deployment cloud smoke tests.

## When the AI Agent Should Use It
- When implementing new API routers, business logic, or data access methods.
- When creating automated pull request validation checks (`ci.yml`).
- When authoring post-deployment smoke test scripts to validate live cloud environments.

## Required Checks
- [ ] Pytest unit and integration test suite passes cleanly with zero failures.
- [ ] Test coverage covers positive paths, invalid input validation (422), and missing resources (404).
- [ ] Post-deployment smoke tests validate HTTP status codes AND response body payload contents (e.g., `status == "healthy"`, `total > 0`).
- [ ] Container tests validate runtime startup and port binding locally prior to cloud deployment.

## Expected Output
- Comprehensive pytest test suites (`tests/test_*.py`).
- Isolated, executable smoke test scripts (`scripts/smoke_test.py`).
- Structured test result reporting during CI/CD execution.

## Engineering Principles
1. **Testing Pyramid**: Maintain a heavy base of fast, isolated unit tests supported by targeted integration and smoke tests.
2. **Payload-Level Assertion**: HTTP 200 is necessary but insufficient; smoke tests must validate response schema data integrity.
3. **Fail Fast**: Run unit and lint checks early in the delivery pipeline before spending time on cloud provisioning.
