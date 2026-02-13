# Creating Agents Guide

This guide defines the standard process for adding an agent to `vilabs-public-agents`.

## Recommended Onboarding Flow

For repository onboarding, start with `agents/core/vilabs-recruiter/` as the primary entry point.

- Use `vilabs-recruiter` to assess project scope and recruit/configure a best-fit agent stack.
- Use `agents/core/repository-introspector/` directly for analysis-only workflows.

## Required Agent Files

Create these files in `agents/<domain>/<agent-name>/`:

- `agent.md`
- `agent.yml`
- `instructions.md`
- `metadata.json`
- `examples/example-1.md`

## Step-by-Step

### 1. Choose a Domain

Use one of:

- `backend`
- `core`
- `data`
- `devops`
- `web`

### 2. Create the Directory

```bash
mkdir -p agents/<domain>/<agent-name>/examples
```

### 3. Author `agent.md`

Define the behavior contract in plain language:

- purpose
- responsibilities
- constraints
- expected output shape

### 4. Author `agent.yml`

Define structured runtime settings:

- `name`
- `description`
- `version`
- `agent` block
- `capabilities`
- `context`
- `behavior`

### 5. Author `instructions.md`

Document:

- when to use the agent
- capabilities
- workflow steps
- best practices
- limitations
- related agents

### 6. Author `metadata.json`

Ensure schema compatibility and initialize quality metrics to zero for new agents.

### 7. Add `examples/example-1.md`

Include a concise input/output example and a brief effectiveness note.

## Validation

```bash
python3 automation/validators/validate_metadata.py
python3 automation/validators/validate_public_safety.py
REPO_ROOT=. python3 automation/scripts/analyze_agents.py
```

## Public-Safety Rules

- Keep examples generic
- Avoid private/internal paths and URLs
- Never include credentials or secret-like values
