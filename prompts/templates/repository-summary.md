# Repository Summary Template

## Context

Use this template to summarize repository structure and recommend next-step agent/skill configuration.

## Variables

- `{{languages}}`
- `{{frameworks}}`
- `{{key_directories}}`
- `{{recommended_domains}}`
- `{{suggested_skills}}`
- `{{open_questions}}`

## Template

```markdown
### Repository Summary

Languages: {{languages}}
Frameworks/Libraries: {{frameworks}}

Key Directories:
{{#each key_directories}}
- {{this}}
{{/each}}

Recommended Agent Domains: {{recommended_domains}}
Suggested Skills: {{suggested_skills}}

Open Questions:
{{#each open_questions}}
- {{this}}
{{/each}}

### Evidence Notes

State the file or config evidence used for each major conclusion.
```

## Effectiveness Metrics

- Confidence: 0.0 (seed)
- Success Rate: 0% (seed)
- Last Updated: 2026-02-08
