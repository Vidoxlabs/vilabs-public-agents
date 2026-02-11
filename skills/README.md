# Skills

Public-safe reusable skill definitions.

## Directory Layout

```text
skills/
└── <skill-name>/
    └── SKILL.md
```

## Downstream Use

Copy selected skills into downstream repositories under `.github/skills/`.

## Skill Requirements

`SKILL.md` must contain YAML frontmatter with only:

- `name`
- `description`

## Public-Safety Standard

- Keep instructions generic
- Use placeholders for environment-specific values
- Do not include credentials or private endpoints
