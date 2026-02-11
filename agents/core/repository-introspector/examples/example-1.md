# Example: Repository Introspection

## Input

"Analyze this repository and recommend which agent domains and skills should be enabled first."

## Output

```markdown
### Repository Summary

Languages: Python, TypeScript, YAML

Framework Signals:
- FastAPI indicators in Python service code
- React/Next.js indicators in frontend package metadata
- Container orchestration indicators in compose manifests

Key Directories:
- `services/api/`
- `apps/web/`
- `packages/shared/`
- `infrastructure/`

Recommended Agent Domains:
- backend
- web
- devops
- core

Suggested Skills:
- repo-analysis
- unit-test-troubleshooting
- ci-failure-triage

Open Questions:
- Are data migrations owned by service teams or platform teams?
- Is deployment monorepo-wide or per-service?
```

## Effectiveness Evaluation

- Confidence: 0.0 (seed)
- Notes: Good baseline triage; requires human confirmation before enabling domain-specialized workflows.
