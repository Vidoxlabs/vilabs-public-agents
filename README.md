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

### 1. Configure ViLabs Configurator (Unified Entry Point)

Use `agents/core/vilabs-configurator/` when you want **one agent** to handle both:

- recruiting/configuring agent workflows from `vilabs-public-agents`
- composing IDE settings from `vilabs-public-settings`

The configurator is responsible for:

- understanding project objective/scope (existing repo or greenfield project)
- building a combined agent + settings implementation plan
- applying merge-safe configuration updates with human approval checkpoints

#### Quick Access (Click to Open)

- [Open configurator folder](agents/core/vilabs-configurator/)
- [agent.md](agents/core/vilabs-configurator/agent.md)
- [instructions.md](agents/core/vilabs-configurator/instructions.md)
- [agent.yml](agents/core/vilabs-configurator/agent.yml)
- [metadata.json](agents/core/vilabs-configurator/metadata.json)
- [example-1.md](agents/core/vilabs-configurator/examples/example-1.md)

#### Fast Configure in Your Repository (`.github`)

Use this from the **target repository** where you want unified configurator support:

```bash
mkdir -p .github/agents .github/instructions

curl -fsSL https://raw.githubusercontent.com/Vidoxlabs/vilabs-public-agents/main/agents/core/vilabs-configurator/agent.md \
	-o .github/agents/vilabs-configurator.agent.md

curl -fsSL https://raw.githubusercontent.com/Vidoxlabs/vilabs-public-agents/main/agents/core/vilabs-configurator/instructions.md \
	-o .github/instructions/vilabs-configurator.instructions.md
```

**Interactive prompt supported:**

> `assist me in creating X`

When used, configurator shifts to question-first planning and asks what to implement first (agents, settings, or both).

### 1.1 Configure ViLabs Recruiter (Modular Path)

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

**Interactive prompt supported:**

> `assist me in creating X`

When used, recruiter shifts to question-first planning (goal, scope, constraints, and implementation targets) before applying changes.

### 1.2 Configure ViLabs Setting (IDE Settings Composer)

Use `agents/core/vilabs-setting/` to build IDE-specific settings using:

`https://github.com/Vidoxlabs/vilabs-public-settings`

The settings agent is responsible for:

- detecting IDE/editor context from repository signals
- selecting best-fit settings bundles from the public settings catalog
- creating merge-safe settings plans and configuration updates

#### Quick Access (Click to Open)

- [Open settings agent folder](agents/core/vilabs-setting/)
- [agent.md](agents/core/vilabs-setting/agent.md)
- [instructions.md](agents/core/vilabs-setting/instructions.md)
- [agent.yml](agents/core/vilabs-setting/agent.yml)
- [metadata.json](agents/core/vilabs-setting/metadata.json)
- [example-1.md](agents/core/vilabs-setting/examples/example-1.md)

#### Fast Configure in Your Repository (`.github`)

Use this from the **target repository** where you want settings-agent support:

```bash
mkdir -p .github/agents .github/instructions

curl -fsSL https://raw.githubusercontent.com/Vidoxlabs/vilabs-public-agents/main/agents/core/vilabs-setting/agent.md \
	-o .github/agents/vilabs-setting.agent.md

curl -fsSL https://raw.githubusercontent.com/Vidoxlabs/vilabs-public-agents/main/agents/core/vilabs-setting/instructions.md \
	-o .github/instructions/vilabs-setting.instructions.md
```

**Interactive prompt supported:**

> `assist me in creating X`

When used, `vilabs-setting` asks clarifying questions about IDE, team conventions, and implementation intent before generating settings plans.

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
