# VS Code Configuration Templates

Modular VS Code configuration templates for tailored development environments.

## Overview

This directory provides a flexible system for assembling VS Code configurations using composable JSON modules. Configurations are assembled according to stack manifests (YAML files in `stacks/`) which define which modules to include and what variables to substitute.

## Directory Structure

```text
vscode-config/
├── core/              # Core editor and security settings
├── settings/          # Editor behavior and tool configurations
├── extensions/        # Extension recommendations
├── tasks/             # VS Code task definitions
├── platforms/         # Platform-specific settings (macOS, Linux)
├── hardware/          # Hardware-optimized settings
├── mcp/               # Model Context Protocol server configs
├── stacks/            # Stack manifest files (YAML)
└── examples/          # Example configurations and usage
```

## Available Modules

### Core Modules (`core/`)

- **editor.json** - Base editor settings (formatting, autosave, themes, rulers)
- **security.json** - Security policies and auto-approval lists for agentic tools

### Settings Modules (`settings/`)

- **base.json** - General workspace settings (search, terminal, file watching)
- **copilot.json** - GitHub Copilot configuration
- **python.json** - Python-specific settings (formatter, linter, type checking)
- **violet.json** - Violet orchestrator settings (Jinja2, YAML, Docker, SQL)
- **advanced.json** - Advanced editor features (suggestions, git integration)

### Extensions Modules (`extensions/`)

- **essentials.json** - Core extensions (Copilot, GitLens, Remote SSH/Containers, Trunk, Prettier)
- **python.json** - Python development extensions (Python, Pylance, Ruff, Mypy, Jupyter)
- **violet.json** - Violet infrastructure extensions (Jinja2, YAML, Docker, SQL, Vault, Makefile, HTTP client)

### Tasks Modules (`tasks/`)

- **general.json** - General purpose tasks (health check)
- **violet.json** - Violet orchestrator tasks (format, lint, test, compose, deploy)

### Platform Modules (`platforms/`)

- **macos.json** - macOS-specific settings
- **linux.json** - Linux-specific settings

### Hardware Modules (`hardware/`)

- **m4-16gb.json** - Settings optimized for lower-end hardware (disables minimap, smooth scrolling, etc.)

### MCP Modules (`mcp/`)

- **base.json** - Model Context Protocol server configurations

## Stack Manifests

Stack manifests are YAML files that define which modules to include and what variables to use.

### Available Stacks

#### python-dev.yaml
General Python development environment with essential tools and extensions.

#### violet-dev.yaml
Full development environment for the Violet orchestrator, including:
- Jinja2 template support
- YAML and Docker Compose integration
- PostgreSQL client tools
- HashiCorp Vault support
- Makefile task automation
- HTTP client for API testing

## Using Stack Manifests

### Quick Start with Builder Script

The easiest way to use these configurations is with the provided builder script:

```bash
# Build a stack to your project's .vscode directory
cd /path/to/your/project
python3 /path/to/vscode-config/scripts/build_stack.py \
    /path/to/vscode-config/stacks/violet-dev.yaml

# Build with variable overrides
python3 /path/to/vscode-config/scripts/build_stack.py \
    /path/to/vscode-config/stacks/violet-dev.yaml \
    -v VILABS_VIOLET_PATH=/home/user/my-violet-repo

# Build to a specific output directory
python3 /path/to/vscode-config/scripts/build_stack.py \
    /path/to/vscode-config/stacks/python-dev.yaml \
    -o /custom/path/.vscode
```

The builder script will:
1. Parse the stack manifest
2. Merge all specified JSON modules
3. Substitute variables
4. Generate `settings.json`, `extensions.json`, and `tasks.json` in the output directory

### Stack Manifest Format

```yaml
name: "Stack Name"
description: "Stack description"
modules:
  core:
    - editor.json
    - security.json
  settings:
    - base.json
    - python.json
  extensions:
    - essentials.json
  tasks:
    - general.json
variables:
  VARIABLE_NAME: "value"
```

### Variable Substitution

Variables defined in the manifest can be used in module files with the syntax `{{VARIABLE_NAME}}`.

Common variables:
- `VILABS_REMOTE_NODE` - Remote node identifier for SSH connections
- `VILABS_VIOLET_PATH` - Path to Violet orchestrator repository
- `${workspaceFolder}` - VS Code built-in workspace folder variable
- `${userHome}` - VS Code built-in user home directory variable

## Integration Guide

### Manual Assembly

1. Choose a stack manifest from `stacks/` (e.g., `violet-dev.yaml`)
2. Read the manifest to identify required modules
3. Merge the JSON modules into your `.vscode/` directory
4. Replace variables with actual values
5. Install recommended extensions

### Automated Assembly

Use the provided `scripts/build_stack.py` script for automated assembly:

```bash
# Basic usage
python3 scripts/build_stack.py stacks/violet-dev.yaml

# With options
python3 scripts/build_stack.py stacks/violet-dev.yaml \
    -o /path/to/output/.vscode \
    -v VILABS_VIOLET_PATH=/custom/path \
    -v VILABS_REMOTE_NODE=my-node

# Get help
python3 scripts/build_stack.py --help
```

**Requirements:**
- Python 3.7+
- PyYAML: `pip install pyyaml`

**Features:**
- Automatic module discovery and merging
- Variable substitution
- Duplicate removal for extensions
- Input deduplication for tasks
- Validation of module paths

## Violet Orchestrator Support

The `violet-dev` stack provides comprehensive support for Violet development:

### Supported Languages & Tools
- Python (Black, Ruff, Mypy, Pytest)
- Jinja2 templates (blueprints)
- YAML & Docker Compose
- SQL (PostgreSQL client)
- HCL (Vault policies)
- Makefile syntax
- HTTP/REST APIs

### Available Tasks
All Violet Makefile targets are available via VS Code tasks:
- `Violet: Install Dev Tools` - Install development dependencies
- `Violet: Format` - Run Black formatter
- `Violet: Lint` - Run Ruff linter
- `Violet: Typecheck` - Run Mypy type checker
- `Violet: Test` - Run Pytest tests
- `Violet: Check All` - Run all checks
- `Violet: Compose Up` - Start Docker services
- `Violet: Compose Down` - Stop Docker services
- `Violet: Rebuild Images` - Rebuild Docker images
- `Violet: Deploy Dev Stack` - Deploy development stack (prompts for credentials)

### Security Configuration
The security module auto-approves common commands for agentic tools:
- Git operations
- Python testing (pytest)
- Make targets
- Docker commands

This enables autonomous operation of AI assistants within defined boundaries.

## Extension Recommendations

### Violet Stack Extensions

**Template & Infrastructure:**
- `wholroyd.jinja` / `samuelcolvin.jinjahtml` - Jinja2 syntax highlighting
- `redhat.vscode-yaml` - YAML language support
- `ms-azuretools.vscode-docker` - Docker & Compose integration
- `timonwong.shellcheck` - Shell script linting
- `ms-vscode.makefile-tools` - Makefile support

**Database & Infrastructure:**
- `mtxr.sqltools` - SQL client for PostgreSQL
- `hashicorp.terraform` - HCL/Vault syntax support

**API Development:**
- `humao.rest-client` - HTTP client
- `rangav.vscode-thunder-client` - Alternative HTTP client

**Version Control:**
- `eamodio.gitlens` - Advanced Git features
- `github.vscode-pull-request-github` - GitHub PR integration

## Dev Container Support

Example `.devcontainer/devcontainer.json` for Violet:

```json
{
  "name": "Violet Dev Container",
  "dockerFile": "Dockerfile",
  "settings": {
    "python.defaultInterpreterPath": "/usr/local/bin/python",
    "python.linting.enabled": true
  },
  "extensions": [
    "ms-python.python",
    "charliermarsh.ruff"
  ],
  "forwardPorts": [8000, 5432, 6379],
  "postCreateCommand": "pip install -e ."
}
```

## Multi-Root Workspace

Example `violet.code-workspace` for multi-project development:

```json
{
  "folders": [
    {
      "name": "Violet Manager",
      "path": "code-violet"
    },
    {
      "name": "VNA",
      "path": "vna"
    }
  ],
  "settings": {
    "python.testing.pytestEnabled": true
  }
}
```

## Best Practices

1. **Start with a base stack** - Use `python-dev` or `violet-dev` as a starting point
2. **Customize gradually** - Add or remove modules as needed
3. **Use variables** - Keep paths and identifiers parameterized
4. **Version control** - Commit your `.vscode/` directory for team consistency
5. **Document customizations** - Add comments explaining non-standard settings
6. **Test configurations** - Verify settings work across team members' machines
7. **Keep security updated** - Review auto-approval lists regularly

## Contributing

When adding new modules:
1. Follow existing JSON structure and naming conventions
2. Use descriptive module names (e.g., `violet.json`, not `v.json`)
3. Document new settings in this README
4. Add variables for environment-specific values
5. Update relevant stack manifests
6. Test module integration with existing stacks

## Public Safety

This configuration repository follows public-safety guidelines:
- No secrets or credentials in configuration files
- No internal URLs or service identifiers
- Use environment variables and placeholders for runtime wiring
- Keep settings neutral and reusable across projects

## License

[Specify your license here]
