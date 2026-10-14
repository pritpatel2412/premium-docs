---
title: Developer Setup & Engineering Handbook
subtitle: Local development environment setup, architectural conventions, and repository standards
author: Core Engineering Team
date: October 2026
status: final
tags: [Developer-Guide, Onboarding, Engineering-Standards, Handbook]
theme: paper
toc: true
---

:::tldr Executive Summary
Welcome to the core engineering platform. This handbook walks you through onboarding in under 15 minutes, details local build commands, explains our directory conventions, and answers common onboarding questions.
:::

## 1. Quickstart Onboarding

Follow these sequential steps to set up your local development workspace:

:::steps
### Clone the Repository
Clone the codebase and initialize submodules:
```bash title="Terminal"
git clone https://github.com/example/platform-core.git
cd platform-core
```
### Configure Local Environment
Copy the example environment template and populate local secrets:
```bash title="Terminal"
cp .env.example .env.local
```
### Install Dependencies
Run the package manager setup command:
```bash title="Terminal"
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```
### Run Verification Tests
Verify that all unit and integration test suites pass locally:
```bash title="Terminal"
pytest tests/ -v
```
:::

## 2. Repository Layout & Architecture

The codebase is organized into modular directories with clear ownership boundaries:

:::filetree
platform-core/
├── src/
│   ├── api/             # FastAPI REST endpoints and request schemas
│   ├── core/            # Business domain models and logic
│   ├── db/              # SQLAlchemy models and migrations
│   └── workers/         # Background async queue consumers
├── tests/
│   ├── unit/            # Fast in-memory unit tests
│   └── integration/     # Docker-backed end-to-end integration tests
├── config/              # Environment-specific configuration files
├── scripts/             # Developer tooling and build scripts
└── docs/                # Architecture decision records and guides
:::

## 3. Environment & Runtime Specifications

:::kv
Runtime Language     | Python 3.12+
Package Manager      | Pip / Virtualenv
Primary Database     | PostgreSQL 16 (Amazon RDS)
Message Queue        | RabbitMQ 3.12 / Redis 7.2
CI/CD Pipeline       | GitHub Actions
Container Runtime    | Docker 26.0+ / Containerd
:::

## 4. Coding Standards & Conventions

:::tip Lazy Senior Dev Philosophy
Before writing code, stop at the first rung:
1. Does this need to be built at all? (YAGNI)
2. Does the standard library already do this? Use it.
3. Can this be one line? Make it one line.
4. Shortest working diff wins once the problem is thoroughly understood.
:::

Always write focused, single-responsibility functions with explicit type annotations:

```python title="src/core/auth.py"
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class SessionContext:
    user_id: str
    tenant_id: str
    scopes: tuple[str, ...]

def is_authorized(context: SessionContext, required_scope: str) -> bool:
    """Validate that the session context possesses the requested scope."""
    return required_scope in context.scopes
```

## 5. Frequently Asked Questions

:::faq
### How do I run integration tests against real databases?
Run `docker compose up -d postgres redis` before invoking `pytest tests/integration/`. The test suite automatically runs test migrations and truncates tables between test cases.

### What is the pull request review SLA?
Our team maintains a 24-hour review SLA for PRs under 400 lines of diff. Larger PRs should be split into thin, verifiable slices.

### How are database migrations executed in staging?
Migrations run automatically via Alembic during the GitHub Actions deployment pipeline after all test suites pass.
:::

## 6. Next Steps

1. Join the `#engineering-platform` Slack channel and introduce yourself.
2. Pick up your first task labeled `good-first-issue` on the sprint board.
3. Schedule a 30-minute 1:1 pair programming session with your onboarding buddy.
