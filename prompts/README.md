# Prompts

Reusable prompt assets for agent workflows.

## Directory Layout

```text
prompts/
├── system-prompts/
├── task-prompts/
├── templates/
└── chains/
```

## Authoring Standard

Each prompt should define:

- Context
- Inputs/variables
- Output expectations
- Constraints or assumptions

## Public-Safety Standard

- Keep prompts repository-agnostic unless placeholders are explicit
- Avoid private architecture or internal service references
- Avoid embedding credentials or endpoint secrets
