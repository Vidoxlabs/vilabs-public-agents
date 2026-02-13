# vilabs-public-agents

Public templates for agent configurations, prompts, skills, and automation.

This repository is intentionally **general-config only**. It is designed to be reusable across repositories without exposing private architecture, internal endpoints, or secrets.

## Purpose

- Provide reusable agent definitions and templates
- Support repository onboarding through analysis-first workflows
- Maintain public-safe defaults for tools and MCP configuration
- Validate quality and safety with repeatable automation

## Repository Layout

```text
vilabs-public-agents/
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

### 1. Configure ViLabs Recruiter (Primary Entry Point)

Use `agents/core/vilabs-recruiter/` first when onboarding an unfamiliar codebase.

The recruiter is responsible for:

- understanding project objective and scope from repository evidence
- selecting best-fit agents from this public catalog
- mapping and applying configuration into the user repository’s `.github/` folder

#### Quick Access (Click to Open)

- [Open recruiter folder](agents/core/vilabs-recruiter/)
- [agent.md](agents/core/vilabs-recruiter/agent.md)
- [instructions.md](agents/core/vilabs-recruiter/instructions.md)
- [agent.yml](agents/core/vilabs-recruiter/agent.yml)
- [metadata.json](agents/core/vilabs-recruiter/metadata.json)
- [example-1.md](agents/core/vilabs-recruiter/examples/example-1.md)

#### Fast Configure in Your Repository (`.github`)

Use this from the **target repository** where you want recruiter configured:

```bash
mkdir -p .github/agents .github/instructions

curl -fsSL https://raw.githubusercontent.com/Vidoxlabs/vilabs-public-agents/main/agents/core/vilabs-recruiter/agent.md \
	-o .github/agents/vilabs-recruiter.agent.md

curl -fsSL https://raw.githubusercontent.com/Vidoxlabs/vilabs-public-agents/main/agents/core/vilabs-recruiter/instructions.md \
	-o .github/instructions/vilabs-recruiter.instructions.md
```

> Note: A true one-click "auto-configure" action is platform-limited for security reasons, but the commands above are the fastest safe setup path.

### 2. Review and Approve the Recruited Agent Stack

Confirm selected agents and generated `.github` files before finalizing.
For manual analysis-only onboarding, use `agents/core/repository-introspector/`.

### 3. Select Templates

Choose relevant assets from:

- `agents/`
- `prompts/`
- `skills/`
- `tools/`
- `mcp-servers/`
- `vscode-config/`

### 4. Run Validation

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
