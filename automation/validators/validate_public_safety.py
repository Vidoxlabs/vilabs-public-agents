#!/usr/bin/env python3
"""
Public Safety Validator

Checks repository content for banned public patterns:
- project-specific private overlays
- branded private import paths
- likely hardcoded credentials
"""

from pathlib import Path
import re
import sys


SCANNED_DIRS = [
    "agents",
    "prompts",
    "instructions",
    "skills",
    "tools",
    "mcp-servers",
    ".github",
]

SCANNED_SUFFIXES = {".md", ".yml", ".yaml", ".json", ".toml", ".txt"}

BANNED_PATTERNS = [
    (re.compile(r"vidoxlabs-studio", re.IGNORECASE), "project-specific private overlay reference"),
    (re.compile(r"@vidoxlabs/", re.IGNORECASE), "org-specific import path"),
    (re.compile(r"https?://[^\s'\"]*internal[^\s'\"]*", re.IGNORECASE), "internal endpoint URL"),
    (
        re.compile(r"\b(?:api[_-]?key|access[_-]?token|secret|password)\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"),
        "likely hardcoded credential",
    ),
]

PLACEHOLDER_HINTS = [
    "example",
    "sample",
    "dummy",
    "fake",
    "placeholder",
    "generated",
    "changeme",
    "abc123",
    "<",
    ">",
    "${",
]


def should_skip_credential_line(line: str) -> bool:
    lower = line.lower()
    return any(hint in lower for hint in PLACEHOLDER_HINTS)


def iter_files(repo_root: Path):
    for dirname in SCANNED_DIRS:
        root = repo_root / dirname
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in SCANNED_SUFFIXES:
                continue
            yield path


def main() -> int:
    repo_root = Path(__file__).parent.parent.parent
    violations = []

    for path in iter_files(repo_root):
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for lineno, line in enumerate(content.splitlines(), start=1):
            for regex, reason in BANNED_PATTERNS:
                if not regex.search(line):
                    continue
                if reason == "likely hardcoded credential" and should_skip_credential_line(line):
                    continue
                violations.append((path.relative_to(repo_root), lineno, reason, line.strip()))

    if violations:
        print("✗ Public-safety validation failed:\n")
        for rel, lineno, reason, snippet in violations:
            print(f"- {rel}:{lineno}: {reason}")
            print(f"  {snippet}")
        print(f"\nTotal violations: {len(violations)}")
        return 1

    print("✓ Public-safety validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
