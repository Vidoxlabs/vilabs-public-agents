# Example: Unified Agent + Settings Bootstrap

## Input

"Assist me in creating a full AI-assisted setup for this repository. I want one agent to handle both recruiting the right sub-agents and composing IDE settings."

## Output

```markdown
### Project Objective and Context

- Mode: Existing repository onboarding
- Goal: Single-entrypoint configuration for agent workflows and IDE settings
- Signals:
  - `.github/` exists with partial configuration
  - polyglot codebase (Python + TypeScript)
  - `.vscode/` present with minimal defaults

### Clarifying Questions Asked

1. Should setup prioritize delivery speed or strict governance?
2. Should settings enforce formatting/linting on save for all contributors?
3. Should initial rollout include only P0/P1 agents and base settings?

### Recruitment Matrix

| Agent                        | Why Selected                            | Priority | Confidence |
| ---------------------------- | --------------------------------------- | -------: | ---------: |
| core/repository-introspector | baseline discovery and risk mapping     |       P0 |       0.90 |
| backend/backend-architect    | backend structure and service contracts |       P1 |       0.84 |
| web/frontend-architect       | frontend architecture alignment         |       P1 |       0.82 |

### Settings Matrix

| Bundle              | Why Selected                              | Priority | Confidence |
| ------------------- | ----------------------------------------- | -------: | ---------: |
| base/vscode-core    | consistent editor baseline                |       P0 |       0.91 |
| language/python     | Python tooling and diagnostics            |       P1 |       0.87 |
| language/typescript | TS/JS analysis and formatting consistency |       P1 |       0.85 |

### Unified Configuration Plan

Create/Update:

- `.github/agents/` and `.github/instructions/` entries for selected agents
- `.vscode/settings.json` and `.vscode/extensions.json`

Conflict Notes:

- Existing `.vscode/settings.json` detected: use merge mode and preserve explicit team overrides.
- Existing `.github/copilot-instructions.md` detected: patch in configurator entrypoint instead of replacing file.

### Execution Summary

- Status: Ready for apply (approval required)
- Apply order:
  1. backup overlapping files
  2. apply net-new files
  3. merge overlap changes
  4. run validation checks
```

## Effectiveness Evaluation

- Confidence: 0.0 (seed)
- Notes: Consolidates recruiter + setting into one controlled, question-first onboarding flow.
