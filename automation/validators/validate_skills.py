#!/usr/bin/env python3
"""
Skill Validator

Validates skill structure and SKILL.md frontmatter requirements.
"""

from pathlib import Path
import re
import sys

import yaml


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def validate_skill_md(skill_md: Path) -> tuple[bool, str]:
    content = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(content)
    if not match:
        return False, "missing YAML frontmatter"

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return False, f"invalid YAML frontmatter: {exc}"

    if not isinstance(frontmatter, dict):
        return False, "frontmatter must be a mapping"

    keys = set(frontmatter.keys())
    if keys != {"name", "description"}:
        return False, "frontmatter must contain only 'name' and 'description'"

    if not isinstance(frontmatter["name"], str) or not frontmatter["name"].strip():
        return False, "'name' must be a non-empty string"

    if not isinstance(frontmatter["description"], str) or not frontmatter["description"].strip():
        return False, "'description' must be a non-empty string"

    return True, "valid"


def main() -> int:
    repo_root = Path(__file__).parent.parent.parent
    skills_root = repo_root / "skills"

    if not skills_root.exists():
        print("✓ skills/ directory not present; nothing to validate")
        return 0

    skill_files = sorted(skills_root.glob("*/SKILL.md"))

    if not skill_files:
        print("✗ No skill files found under skills/*/SKILL.md")
        return 1

    valid_count = 0
    for skill_md in skill_files:
        ok, message = validate_skill_md(skill_md)
        rel = skill_md.relative_to(repo_root)
        if ok:
            print(f"✓ {rel} is valid")
            valid_count += 1
        else:
            print(f"✗ {rel} is invalid: {message}")

    print(f"\n{valid_count}/{len(skill_files)} skills are valid")
    return 0 if valid_count == len(skill_files) else 1


if __name__ == "__main__":
    sys.exit(main())
