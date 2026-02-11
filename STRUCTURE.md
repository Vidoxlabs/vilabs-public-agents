# Repository Structure Guide

This document defines the canonical structure for `vidocs-agents`.

## Top-Level Directories

### `agents/`

Reusable agents grouped by domain (`backend`, `core`, `data`, `devops`, `web`, `template-agent`).

### `prompts/`

Prompt assets organized as:

- `system-prompts/`
- `task-prompts/`
- `templates/`
- `chains/`

### `instructions/`

Neutral context overlays and workflow guidance.

### `skills/`

Reusable skill library for downstream `.github/skills` use.

### `tools/`

Generic tool interface templates.

### `mcp-servers/`

MCP server configuration templates with placeholder-based wiring.

### `vscode-config/`

Modular VS Code configuration templates for tailored development environments. Includes:

- Core editor and security settings
- Language-specific configurations (Python, Jinja2, YAML, Docker, SQL)
- Extension recommendations
- Task definitions for automated workflows
- Stack manifests for different development scenarios (Python dev, Violet orchestrator)
- Platform and hardware-optimized settings
- Dev container and workspace examples

### `schemas/`

Validation schemas used by automation.

### `automation/`

Validation and reporting scripts.

### `docs/`

Project guides and generated reports.

## Naming Conventions

- Directory names: kebab-case
- File names: kebab-case where applicable
- IDs: specific-generic form (for example `frontend-architect`)

## Public-Safety Constraints

- No private infrastructure details
- No internal service identifiers or endpoints
- No secrets or secret-like literals
