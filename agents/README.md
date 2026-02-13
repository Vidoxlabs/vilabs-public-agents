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

1. Run `core/vilabs-recruiter` as the main onboarding coordinator.
2. Let recruiter analyze objective/scope and propose a role-based agent stack.
3. Approve recruiter output before writing/updating `.github/` configuration.
4. Use `core/repository-introspector` directly for analysis-only workflows.
5. Keep recommendations human-reviewed before applying changes.

See `../docs/creating-agents.md` and `../CONTRIBUTING.md`.
