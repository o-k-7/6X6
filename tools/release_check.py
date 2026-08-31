#!/usr/bin/env python3
"""Zero-dependency public-release gate for 6X6."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md",
    "QUICKSTART.md",
    "6X6-PROMPT.txt",
    "INSTALL-WITH-AI.txt",
    "examples/BEFORE_AFTER.md",
    "LICENSE",
    "LEGAL.md",
    "PRIVACY.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
    "TRADEMARKS.md",
    "DCO.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "CHANGELOG.md",
    "SPEC.md",
    "docs/INSTALLATION.md",
    "docs/COMPATIBILITY.md",
    "docs/RELEASE_CHECKLIST.md",
    "skills/6x6/SKILL.md",
    "skills/6x6/references/SPEC.md",
    "skills/6x6/agents/openai.yaml",
    "prompts/universal.md",
    "tools/security_check.py",
)


def skill_version(text: str) -> str | None:
    match = re.search(r'^\s*version:\s*["\']?([^"\'\n]+)["\']?\s*$', text, re.MULTILINE)
    return match.group(1).strip() if match else None


def run(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    if (root / "SKILL.md").exists():
        errors.append("ambiguous root SKILL.md must not exist")

    skill_path = root / "skills/6x6/SKILL.md"
    if skill_path.is_file():
        skill = skill_path.read_text(encoding="utf-8")
        if not skill.startswith("---\n"):
            errors.append("canonical SKILL.md must start with YAML frontmatter")
        if not re.search(r"^name:\s*6x6\s*$", skill, re.MULTILINE):
            errors.append("canonical skill name must be 6x6")
        version = skill_version(skill)
        if not version:
            errors.append("canonical skill metadata.version is missing")
        else:
            changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8") if (root / "CHANGELOG.md").is_file() else ""
            if f"[{version}]" not in changelog:
                errors.append(f"CHANGELOG.md has no [{version}] entry")

    prompt = root / "6X6-PROMPT.txt"
    universal = root / "prompts/universal.md"
    if prompt.is_file() and universal.is_file():
        prompt_text = prompt.read_text(encoding="utf-8").strip()
        universal_text = universal.read_text(encoding="utf-8")
        if prompt_text not in universal_text:
            errors.append("6X6-PROMPT.txt must match the universal prompt instruction block")

    installer = root / "INSTALL-WITH-AI.txt"
    if installer.is_file():
        installer_text = installer.read_text(encoding="utf-8")
        if "skills/6x6/" not in installer_text:
            errors.append("INSTALL-WITH-AI.txt must point to the canonical skill")
        if "Do not install dependencies" not in installer_text:
            errors.append("INSTALL-WITH-AI.txt must preserve the safe installation guardrail")

    openai_path = root / "skills/6x6/agents/openai.yaml"
    if openai_path.is_file():
        metadata = openai_path.read_text(encoding="utf-8")
        for required_text in ("display_name:", "short_description:", "default_prompt:"):
            if required_text not in metadata:
                errors.append(f"openai.yaml missing {required_text[:-1]}")

    return errors


def main() -> int:
    errors = run()
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: public-release structure is consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
