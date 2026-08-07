# 📚 AI Skill: Documentation & Knowledge Management

## Objective
Maintain concise, accurate, living documentation covering system architecture, operational deployment guides, security models, SRE SLOs, and post-incident lessons learned.

## When the AI Agent Should Use It
- After completing a major feature, refactoring, or infrastructure update.
- When resolving a complex bug or troubleshooting deployment issues (to log post-mortems).
- When updating technical blueprints in `/docs` to align with implementation changes.

## Required Checks
- [ ] System topology diagrams in `/docs/architecture.md` accurately reflect deployed cloud resources.
- [ ] Deployment and rollback procedures in `/docs/deployment.md` are step-by-step and repeatable.
- [ ] Post-incident root cause analyses logged under `/lessons-learned`.
- [ ] README provides a clear 5-minute local setup and quick start walkthrough.

## Expected Output
- Up-to-date Markdown documentation files in `/docs`.
- Standardized architectural decision records (ADRs) and post-mortem logs.
- Clickable markdown links to local repository paths and files.

## Engineering Principles
1. **Living Codebase Docs**: Treat documentation as code—versioned, reviewed, and kept in sync with implementation.
2. **Post-Mortem Culture**: Capture failure modes and root cause learnings to prevent recurring issues.
3. **Clarity and Context**: Document the *why* behind decisions, not just the *what*.
