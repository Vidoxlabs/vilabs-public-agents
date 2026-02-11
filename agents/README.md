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

1. Run `core/repository-introspector` for repository discovery.
2. Select domain agents based on the discovery output.
3. Keep recommendations human-reviewed before applying changes.

See `../docs/creating-agents.md` and `../CONTRIBUTING.md`.
