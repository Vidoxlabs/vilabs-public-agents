# Example: Create Instructions for a Python Monorepo

## Input

"Assist me in creating comprehensive instruction files for this Python monorepo. We have backend services, data pipelines, CLI tools, and we want AI agents to understand our coding standards, testing requirements, and architectural patterns. What guidelines should we document?"

## Output

```markdown
### Repository Profile and Analysis

- Project Purpose: Multi-domain Python monorepo with services, data, and tooling
- Primary Domains: Backend (FastAPI services), Data (ETL/ML pipelines), DevOps (infrastructure scripting)
- Tech Stack Signals:
  - Python 3.10+, FastAPI, Pydantic, SQLAlchemy
  - pytest with fixtures and parametrization
  - Docker, Kubernetes for deployment
  - GitHub Actions CI/CD pipeline detected
  - mypy/black type checking and formatting
  - Pre-commit hooks configured

### Instruction Categories Matrix

| Category              | Coverage Scope                                             | Priority | Confidence |
| --------------------- | ---------------------------------------------------------- | -------: | ---------: |
| Code Standards        | Naming (snake_case modules, PascalCase classes), structure |       P0 |       0.95 |
| Testing Requirements  | Unit/integration strategy, fixture patterns                |       P0 |       0.92 |
| API Design            | Contract-first, error codes, versioning                    |       P1 |       0.88 |
| Data Modeling         | Schema patterns, validation approach                       |       P1 |       0.87 |
| Agent Behavior        | How LLMs should interact with repo                         |       P1 |       0.85 |
| Security & Compliance | Secret handling, dependency scanning, auth                 |       P2 |       0.80 |
| Documentation         | Docstring style, architecture ADRs                         |       P2 |       0.82 |
| Performance           | Resource constraints, optimization targets                 |       P3 |       0.75 |

### File Organization Plan

Create/Update:

1. `.github/instructions/code-standards.instructions.md`
   - Naming conventions, module organization, import patterns
   - Type hints and linting rules
2. `.github/instructions/testing.instructions.md`
   - Pytest structure, fixture patterns, coverage expectations
   - GHA testing workflow alignment
3. `.github/instructions/api-design.instructions.md`
   - FastAPI endpoint patterns, request/response contracts
   - Error handling and status codes
4. `.github/instructions/agent-behavior.instructions.md`
   - How agents should modify code safely within this monorepo
   - Commit/PR conventions agents must follow
5. `.github/instructions/security-compliance.instructions.md`
   - Secret scanning, dependency checks, deployment approval

Conflict Notes:

- No existing `.github/instructions/` folder detected; safe to create all files.

### Generated Instruction Files (Preview)

#### `.github/instructions/code-standards.instructions.md`
```

# Code Standards for [Repository Name]

## Module Organization

Modules MUST follow snake_case naming: `user_service.py`, `data_pipeline.py`

Classes MUST use PascalCase: `UserService`, `DataProcessor`

## Import Organization

1. Standard library imports (alphabetical)
2. Third-party imports (alphabetical, grouped by category)
3. Local imports (alphabetical)

Example:
\`\`\`python
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

import pydantic
from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, Integer, String

from .models import User
from .services import user_service
\`\`\`

## Type Hints

ALL public functions MUST have type hints.

Example (REQUIRED):
\`\`\`python
def create_user(name: str, email: str) -> User:
"""Create a new user."""
return User(name=name, email=email)
\`\`\`

## Docstrings

Use Google-style docstrings for all public functions, classes, and modules.

Example:
\`\`\`python
def calculate_discount(price: float, rate: float) -> float:
"""Calculate discounted price.

    Args:
        price: Original price in dollars.
        rate: Discount rate as decimal (0.1 = 10%).

    Returns:
        Discounted price.

    Raises:
        ValueError: If rate < 0 or rate > 1.
    """

\`\`\`

## Linting and Formatting

- Black for code formatting (line length: 88 chars)
- mypy for type checking (strict mode)
- pylint for code quality
- Pre-commit hooks MUST pass before commit

Run locally:
\`\`\`bash
make lint
make type-check
\`\`\`

```

#### `.github/instructions/agent-behavior.instructions.md`

```

# Agent Behavior Guidelines

## Safe Modification Zones

Agents MAY modify:

- Implementation functions (preserve signatures)
- Test files (add tests, refactor test code)
- Documentation and comments
- Configuration files (with approval)

Agents MUST NOT modify:

- Public API signatures (breaking changes require discussion)
- Core data models without validation
- CI/CD workflows without explicit approval

## Commit Conventions

All commits MUST follow Conventional Commits:

\`fix: brief description\` — bug fixes
\`feat: brief description\` — new features
\`docs: brief description\` — documentation only
\`refactor: brief description\` — code restructuring
\`test: brief description\` — test additions/updates

Example:
\`\`\`
feat: add user role-based access control

- Implement Role model and permissions
- Add authorization middleware
- Extend user schema with role_id field

Closes #123
\`\`\`

## Pull Request Conventions

- Title: \`[domain] Brief description\` (e.g., \`[backend] Add user authentication\`)
- Link related issues: "Closes #123" or "Relates to #456"
- Include test coverage proof in description
- Request review from domain owners

```

### Execution Summary

- Status: Ready for apply (human approval required)
- Safe Application Plan:
  1. Create `.github/instructions/` directory
  2. Write instruction files in order: code-standards, testing, api-design, agent-behavior, security-compliance
  3. Add links in main README pointing to instruction files
  4. Notify team of new guidelines
  5. Schedule review in 2 weeks

### Open Questions / Follow-Ups

1. Should data pipeline code follow the same standards as service code? (Recommend: YES, with flexibility for notebook-style exploration)
2. How frequently should instructions be reviewed/updated? (Recommend: quarterly + ad-hoc)
3. Should pre-commit hooks be enforced or optional? (Recommend: enforced with bypass option for specific commits)
```

## Effectiveness Evaluation

- Confidence: 0.0 (seed)
- Notes: Designed for interactive, evidence-based instruction composition with explicit merge strategy and team approval gates. Generates production-ready instruction files that bridge repository conventions and AI agent behavior.
