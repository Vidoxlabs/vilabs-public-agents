# Example: Recruit and Configure Agent Stack

## Input

"Assist me in creating an AI-assisted development setup for this repository. Start by understanding project scope, ask me clarifying questions, then recruit the right agents from the public vilabs catalog and set up `.github` configuration."

## Output

```markdown
### Project Objective and Scope

- Repository Type: Polyglot monorepo
- Primary Goal: Ship backend APIs + web frontend with CI/CD and observability
- Observed Signals:
  - `services/api/` (backend)
  - `apps/web/` (frontend)
  - `infrastructure/` (devops)
  - `docs/` (documentation maturity)

### Recruitment Matrix

| Agent                          | Why Selected                               | Priority | Confidence |
| ------------------------------ | ------------------------------------------ | -------: | ---------: |
| core/repository-introspector   | Baseline discovery and risk mapping        |       P0 |       0.90 |
| backend/backend-architect      | API and service architecture decisions     |       P1 |       0.85 |
| web/frontend-architect         | UI architecture and frontend guidance      |       P1 |       0.82 |
| devops/cicd-pipeline-generator | CI/CD scaffolding and pipeline consistency |       P1 |       0.80 |
| devops/observability-architect | Logging, metrics, and tracing setup        |       P2 |       0.76 |

### `.github` Configuration Plan

Create/Update:

- `.github/agents/` (agent configs derived from selected templates)
- `.github/instructions/` (workflow-specific instructions)
- `.github/prompts/` (task and chain prompts)
- `.github/copilot-instructions.md` (orchestration entrypoint notes)

Conflict Notes:

- Existing `.github/copilot-instructions.md` found; propose merge strategy instead of overwrite.

### Execution Summary

- Status: Ready for apply (human approval required)
- Safe Apply Mode:
  1. backup existing `.github/` files
  2. apply net-new files
  3. merge overlapping instruction files
  4. run validation checks

### Open Questions

1. Should security-focused agents be mandatory in all repositories?
2. Should recruiter auto-apply changes or only generate patch plans by default?
```

## Effectiveness Evaluation

- Confidence: 0.0 (seed)
- Notes: Strong onboarding pattern for an "agent that recruits agents"; requires iterative tuning for org-specific `.github` conventions.
