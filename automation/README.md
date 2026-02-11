# Automation

Validation and reporting scripts for repository maintenance.

## Contents

```text
automation/
├── scripts/
│   ├── analyze_agents.py
│   └── calculate_confidence.py
└── validators/
    ├── validate_metadata.py
    ├── validate_skills.py
    └── validate_public_safety.py
```

## Install

```bash
pip install -r requirements.txt
```

## Run Validators

```bash
python3 automation/validators/validate_metadata.py
python3 automation/validators/validate_skills.py
python3 automation/validators/validate_public_safety.py
```

## Generate Reports

```bash
REPO_ROOT=. python3 automation/scripts/analyze_agents.py
REPO_ROOT=. python3 automation/scripts/calculate_confidence.py
```

Generated reports are written to `docs/`.
