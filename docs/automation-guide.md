# Automation Guide

This guide describes the automation and validation workflow for `vilabs-public-agents`.

## Tooling Overview

### Validators

- `automation/validators/validate_metadata.py`
  Validate `metadata.json` files against `schemas/agent-metadata.schema.json`.

- `automation/validators/validate_skills.py`
  Validate `skills/*/SKILL.md` presence and frontmatter constraints.

- `automation/validators/validate_public_safety.py`
  Detect banned public-repo patterns (private overlays, branded private imports, likely hardcoded credentials).

### Reporting Scripts

- `automation/scripts/analyze_agents.py`
  Generate `docs/cross-reference-analysis.md`.

- `automation/scripts/calculate_confidence.py`
  Update confidence ratings and generate `docs/confidence-ratings.md`.

## Local Workflow

```bash
pip install -r requirements.txt
python3 automation/validators/validate_metadata.py
python3 automation/validators/validate_skills.py
python3 automation/validators/validate_public_safety.py
REPO_ROOT=. python3 automation/scripts/analyze_agents.py
```

## CI Workflow

The canonical CI validation workflow is:

- `.github/workflows/validate-agents.yml`

It runs metadata, skills, and public-safety validation, then publishes report artifacts.

## Weekly Maintenance Workflow

The scheduled workflow:

- `.github/workflows/weekly-update.yml`

runs confidence and analysis updates on a weekly cadence.

## Notes

- Keep `docs/` as the canonical report output directory.
- Do not bypass public-safety checks for convenience.
- Treat generated reports as artifacts derived from repository state.
