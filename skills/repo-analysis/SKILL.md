---
name: repo-analysis
description: Analyze an unfamiliar repository to identify structure, technologies, and constraints, then recommend generic agent and skill configuration using evidence-based summaries.
---

# Repository Analysis Skill

1. Enumerate files and directories at a high level.
2. Detect language/framework/build signals from standard config files.
3. Map key paths to likely responsibilities (API, UI, data, infra, tooling).
4. Summarize findings with explicit confidence notes.
5. Recommend generic agent domains and complementary skills.
6. List unresolved questions that need human confirmation.

## Guardrails

- Base conclusions on observed files only.
- Avoid project-specific assumptions when evidence is ambiguous.
- Do not expose secrets or private endpoint details.
- Keep recommendations in analyze-then-recommend mode.
