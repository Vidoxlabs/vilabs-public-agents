# vidocs-agents

Public templates for agent configurations, prompts, skills, and automation.

This repository is intentionally **general-config only**. It is designed to be reusable across repositories without exposing private architecture, internal endpoints, or secrets.

## Purpose

- Provide reusable agent definitions and templates
- Support repository onboarding through analysis-first workflows
- Maintain public-safe defaults for tools and MCP configuration
- Validate quality and safety with repeatable automation

## Repository Layout

```text
vidocs-agents/
├── agents/
├── prompts/
├── instructions/
├── skills/
├── tools/
├── mcp-servers/
├── vscode-config/
├── schemas/
├── automation/
└── docs/
```

## Quick Start

### 1. Start with Repository Analysis

Use `agents/core/repository-introspector/` first when onboarding an unfamiliar codebase.

### 2. Select Templates

Choose relevant assets from:

- `agents/`
- `prompts/`
- `skills/`
- `tools/`
- `mcp-servers/`
- `vscode-config/`

### 3. Run Validation

```bash
pip install -r requirements.txt
python3 automation/validators/validate_metadata.py
python3 automation/validators/validate_skills.py
python3 automation/validators/validate_public_safety.py
REPO_ROOT=. python3 automation/scripts/analyze_agents.py
```

## Public-Safety Rules

- Do not commit secrets, credentials, or internal URLs
- Do not include private project architecture overlays
- Keep templates neutral and parameterized
- Use placeholders and environment variables for runtime wiring

## Documentation

- [Repository Structure](STRUCTURE.md)
- [Contributing](CONTRIBUTING.md)
- [Agent Creation Guide](docs/creating-agents.md)
- [Automation Guide](docs/automation-guide.md)
- [VS Code Configuration Guide](vscode-config/README.md)
- [Metadata Schema](schemas/agent-metadata.schema.json)

## License

[Specify your license here]
