# Agents

Reusable agent definitions grouped by domain.

## Directory Layout

```text
agents/
├── backend/
├── core/
├── data/
├── devops/
├── web/
└── template-agent/
```

## Expected Files per Agent

- `agent.md`
- `agent.yml`
- `instructions.md`
- `metadata.json`
- `examples/example-1.md`

## Recommended Usage Order

1. Run `core/vilabs-configurator` for a single-agent onboarding flow (agents + settings together).
2. Use `core/vilabs-recruiter` and `core/vilabs-setting` separately when you want modular control.
3. Approve output before writing/updating `.github/` configuration or workspace settings.
4. Use `core/repository-introspector` directly for analysis-only workflows.
5. Keep recommendations human-reviewed before applying changes.

See `../docs/creating-agents.md` and `../CONTRIBUTING.md`.
