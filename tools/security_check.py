#!/usr/bin/env python3
"""Zero-dependency security audit for the 6X6 repository.

The check is intentionally conservative. It scans project text files for
credential-like material and Python source for dangerous execution/network
primitives that are not needed by the reference implementation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()

TEXT_SUFFIXES = {".py", ".md", ".txt", ".json", ".yaml", ".yml"}
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv", "venv"}
KNOWN_FIXTURE_FILES = {"tests/test_security_check.py"}

SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "openai-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "aws access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}

DANGEROUS_PYTHON_PATTERNS = {
    "shell execution": re.compile(r"\b(?:os\.system|subprocess\.(?:run|Popen|call|check_call|check_output))\s*\("),
    "dynamic execution": re.compile(r"\b(?:eval|exec)\s*\("),
    "network client": re.compile(r"\b(?:requests\.|urllib\.request|http\.client|socket\.)"),
}


@dataclass(frozen=True)
class Finding:
    path: str
    category: str
    line: int


def _iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or path.resolve() == SELF:
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        try:
            relative = path.relative_to(root).as_posix()
        except ValueError:
            continue
        if relative in KNOWN_FIXTURE_FILES:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def scan(root: Path = ROOT) -> list[Finding]:
    findings: list[Finding] = []
    for path in _iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = str(path.relative_to(root))
        for line_no, line in enumerate(text.splitlines(), 1):
            for category, pattern in SECRET_PATTERNS.items():
                if pattern.search(line):
                    findings.append(Finding(rel, category, line_no))
            if path.suffix == ".py":
                for category, pattern in DANGEROUS_PYTHON_PATTERNS.items():
                    if pattern.search(line):
                        findings.append(Finding(rel, category, line_no))
    return findings


def main() -> int:
    findings = scan()
    if findings:
        for item in findings:
            print(f"FAIL: {item.path}:{item.line}: {item.category}")
        return 1
    print("PASS: no credential-like material or forbidden execution/network primitives found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
