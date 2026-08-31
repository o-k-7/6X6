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
    target_lines: int
    protected_lines: tuple[int, ...]
    violating_lines: tuple[int, ...]


def count_words(line: str) -> int:
    """Count whitespace-separated words after trimming."""
    return len(line.strip().split())


def check_signal(text: str, protected_lines: set[int] | None = None) -> CheckResult:
    """Check deterministic 6X6 formatting.

    Blank lines are ignored. ``protected_lines`` uses 1-based physical line
    numbers. Protected lines preserve exact content and are excluded from both
    the six-line and six-word mechanical targets.
    """
    protected = protected_lines or set()
    content = [(number, line.strip()) for number, line in enumerate(text.splitlines(), 1) if line.strip()]
    target = [(number, line) for number, line in content if number not in protected]
    violations = tuple(number for number, line in target if count_words(line) > 6)
    present_protected = tuple(number for number, _ in content if number in protected)

    return CheckResult(
        compliant=len(target) <= 6 and not violations,
        content_lines=len(content),
        target_lines=len(target),
        protected_lines=present_protected,
        violating_lines=violations,
    )


def _parse_protected_lines(raw: str) -> set[int]:
    protected: set[int] = set()
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        number = int(item)
        if number < 1:
            raise ValueError("protected line numbers must be >= 1")
        protected.add(number)
    return protected


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a Signal block for strict 6X6 formatting.")
    parser.add_argument("file", type=Path, help="UTF-8 text file containing a Signal block")
    parser.add_argument(
        "--protect",
        default="",
        help="Comma-separated 1-based physical line numbers exempt from line/word targets",
    )
    args = parser.parse_args()

    try:
        protected = _parse_protected_lines(args.protect)
    except ValueError as exc:
        parser.error(str(exc))

    result = check_signal(args.file.read_text(encoding="utf-8"), protected)

    print(f"content_lines={result.content_lines}")
    print(f"target_lines={result.target_lines}")
    if result.protected_lines:
        print("protected_lines=" + ",".join(map(str, result.protected_lines)))
    if result.violating_lines:
        print("word_limit_violations=" + ",".join(map(str, result.violating_lines)))
    print("PASS" if result.compliant else "FAIL")
    return 0 if result.compliant else 1


if __name__ == "__main__":
    raise SystemExit(main())
