# Example: Build IDE Settings from Public Catalog

## Input

"Assist me in creating a VS Code settings baseline for this Python + TypeScript monorepo. Ask me what standards we should enforce, then generate the safest merge plan."

## Output

```markdown
### Objective and IDE Context

- Goal: Create a standardized VS Code settings profile for a Python + TypeScript monorepo
- IDE Signals:
  - `.vscode/extensions.json` present
  - `requirements.txt` and `package.json` both present
  - Existing formatter/linter configs detected

### Clarifying Questions Asked

1. Should formatting be strict-on-save for all contributors?
2. Should type-checking be warning or error level by default?
3. Do you want performance-focused defaults for low-resource machines?

### Settings Recommendation Matrix

| Bundle              | Why Selected                               | Priority | Confidence |
| ------------------- | ------------------------------------------ | -------: | ---------: |
| base/vscode-core    | consistent editor defaults                 |       P0 |       0.90 |
| language/python     | python tooling + analysis consistency      |       P1 |       0.86 |
| language/typescript | TS/JS diagnostics and formatting alignment |       P1 |       0.84 |
| quality/lint-format | shared lint/format ergonomics              |       P1 |       0.82 |

### Configuration Plan

Create/Update:

- `.vscode/settings.json`
- `.vscode/extensions.json`
- optional `.github/instructions/settings-policy.instructions.md`

Conflict Notes:

- Existing `.vscode/settings.json` found; apply merge mode (preserve user overrides).

### Execution Summary

- Status: Ready for apply (human approval required)
- Safe Apply Mode:
  1. backup existing settings files
  2. apply additive defaults
  3. preserve project-specific overrides
  4. run validation checklist
```

## Effectiveness Evaluation

- Confidence: 0.0 (seed)
- Notes: Designed for safe, interactive settings bootstrap with explicit merge strategy.
