#!/usr/bin/env python3
"""Zero-dependency security audit for the 6X6 repository.

The check scans UTF-8 project files for credential-like material and inspects
Python ASTs for execution/network capabilities that the reference tools do not
need.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
MAX_TEXT_FILE_BYTES = 1_000_000

SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv", "venv"}
KNOWN_FIXTURE_FILES = {"tests/test_security_check.py"}

SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "openai-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "aws access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "bearer token": re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{24,}\b", re.IGNORECASE),
}

FORBIDDEN_IMPORT_PREFIXES = (
    "subprocess",
    "socket",
    "requests",
    "urllib.request",
    "http.client",
)


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
        try:
            if path.stat().st_size > MAX_TEXT_FILE_BYTES:
                continue
        except OSError:
            continue
        yield path


def _dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _dotted_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return None


def _python_findings(path: Path, rel: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    try:
        tree = ast.parse(text, filename=rel)
    except SyntaxError:
        findings.append(Finding(rel, "invalid Python syntax", 1))
        return findings

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith(FORBIDDEN_IMPORT_PREFIXES):
                    findings.append(Finding(rel, "network or process import", node.lineno))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.startswith(FORBIDDEN_IMPORT_PREFIXES):
                findings.append(Finding(rel, "network or process import", node.lineno))
        elif isinstance(node, ast.Call):
            name = _dotted_name(node.func) or ""
            if name in {"eval", "exec"}:
                findings.append(Finding(rel, "dynamic execution", node.lineno))
            elif name == "os.system" or name.startswith("subprocess."):
                findings.append(Finding(rel, "shell execution", node.lineno))
            elif name.startswith(("socket.", "requests.", "urllib.request.", "http.client.")):
                findings.append(Finding(rel, "network client", node.lineno))

    return findings


def scan(root: Path = ROOT) -> list[Finding]:
    findings: list[Finding] = []
    for path in _iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        rel = path.relative_to(root).as_posix()
        for line_no, line in enumerate(text.splitlines(), 1):
            for category, pattern in SECRET_PATTERNS.items():
                if pattern.search(line):
                    findings.append(Finding(rel, category, line_no))

        if path.suffix.lower() == ".py":
            findings.extend(_python_findings(path, rel, text))

    return findings


def main() -> int:
    findings = scan()
    if findings:
        for item in findings:
            print(f"FAIL: {item.path}:{item.line}: {item.category}")
        return 1
    print("PASS: no credential-like material or forbidden execution/network capabilities found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
