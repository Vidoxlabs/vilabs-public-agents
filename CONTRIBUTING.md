# Contributing to vidocs-agents

Thank you for contributing.

## Contribution Standard

All contributions must preserve the repository's public-safe, reusable posture.

- Keep content general and environment-agnostic
- Avoid private architecture details and internal URLs
- Do not commit credentials, tokens, or secret-like values

## Scope of Contributions

1. New or improved agents
2. New or improved prompts
3. New or improved skills
4. Tool and MCP template updates
5. Automation and validation improvements
6. Documentation improvements

## Required Validation

Run these checks before opening a pull request:

```bash
pip install -r requirements.txt
python3 automation/validators/validate_metadata.py
python3 automation/validators/validate_skills.py
python3 automation/validators/validate_public_safety.py
REPO_ROOT=. python3 automation/scripts/analyze_agents.py
```

## Required Agent Files

Each agent directory should include:

- `agent.md`
- `agent.yml`
- `instructions.md`
- `metadata.json`
- `examples/example-1.md`

## Required Skill Files

Each skill directory must include:

- `SKILL.md` with YAML frontmatter containing only `name` and `description`

## Pull Request Checklist

- Validation commands pass locally
- Links and references are valid
- Examples remain generic and non-sensitive
- Documentation is updated for behavior or structure changes
