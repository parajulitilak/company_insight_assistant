# 1. Codebase

> One codebase tracked in revision control, many deploys

The RAG Fusemachines project uses a single Git repository hosted on GitHub, with branches for development, staging, and production. The codebase is deployed to multiple environments using Docker.

## Implementation
- **Git**: Initialized with `git init` and connected to a remote repository.
- **Pre-commit Hooks**: Use `pre-commit` with Ruff for linting and formatting (`ruff-pre-commit`).
- **CI/CD**: Configured with GitHub Actions for automated testing and deployment.

## Setup

git clone <repository-url>

cd company_insight_assistant

pre-commit install