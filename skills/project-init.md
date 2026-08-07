# 🚀 AI Skill: Project Initialization

## Objective
Establish a clean, standardized, production-ready project foundation for cloud-native Python microservices and SaaS APIs. Ensures consistent repository layout, virtual environment hygiene, dependency pinning, and baseline code quality tools.

## When the AI Agent Should Use It
- When bootstrapping a new microservice or API repository from scratch.
- When reorganizing an unstructured legacy repository into a production layout.
- When validating initial repository setup against platform engineering standards.

## Required Checks
- [ ] Virtual environment initialized at `.venv/`.
- [ ] Requirements pinned in `requirements.txt` with explicit version bounds.
- [ ] Standard directory layout created (`/app`, `/tests`, `/docs`, `/infrastructure`, `/scripts`).
- [ ] `.gitignore`, `.dockerignore`, `.editorconfig`, and `pytest.ini` present and configured.
- [ ] Application entrypoint defined with health check endpoint (`/health`).
- [ ] Pre-commit or basic linting tools (`black`, `ruff`, `flake8`) configured.

## Expected Output
- A fully functional, runnable local application layout.
- Passing baseline test verifying `/health` endpoint.
- Working Docker container build configuration.
- Clean git repository initialization with initial feature branch structure.

## Engineering Principles
1. **Convention Over Configuration**: Standardize project layouts so platform engineers and AI agents can navigate any repository instantly.
2. **Deterministic Environments**: Pin runtime and dependency versions to eliminate environment drift.
3. **Container-First Thinking**: Design local applications to run seamlessly inside containers from day one.
