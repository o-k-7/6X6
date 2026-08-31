#!/usr/bin/env python3
"""Deterministic 6X6 Signal conformance checker.

No third-party dependencies are required.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CheckResult:
    compliant: bool
    content_lines: int
    violating_lines: tuple[int, ...]


def count_words(line: str) -> int:
    """Count whitespace-separated words after trimming."""
    return len(line.strip().split())


def check_signal(text: str, protected_lines: set[int] | None = None) -> CheckResult:
    """Check deterministic 6X6 formatting.

    Blank lines are ignored. `protected_lines` uses 1-based physical line numbers.
    Protected lines are preserved but excluded from the six-word check.
    """
    protected = protected_lines or set()
    content = [(number, line.strip()) for number, line in enumerate(text.splitlines(), 1) if line.strip()]
    violations = tuple(
        number
        for number, line in content
        if number not in protected and count_words(line) > 6
    )
    return CheckResult(
        compliant=len(content) <= 6 and not violations,
        content_lines=len(content),
        violating_lines=violations,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a Signal block for strict 6X6 formatting.")
    parser.add_argument("file", type=Path, help="UTF-8 text file containing a Signal block")
    parser.add_argument(
        "--protect",
        default="",
        help="Comma-separated 1-based physical line numbers exempt from word-count checks",
    )
    args = parser.parse_args()

    protected = {int(item) for item in args.protect.split(",") if item.strip()}
    result = check_signal(args.file.read_text(encoding="utf-8"), protected)

    print(f"content_lines={result.content_lines}")
    if result.violating_lines:
        print("word_limit_violations=" + ",".join(map(str, result.violating_lines)))
    print("PASS" if result.compliant else "FAIL")
    return 0 if result.compliant else 1


if __name__ == "__main__":
    raise SystemExit(main())
