#!/usr/bin/env python3
"""Offline 6X6 evaluation harness.

Evaluates pre-recorded or manually supplied Signal outputs without calling any
model API. This keeps the reference benchmark deterministic and zero-cost.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from tools.check_6x6 import check_signal


@dataclass(frozen=True)
class CaseScore:
    case_id: str
    compliant: bool
    critical_term_recall: float
    found_terms: tuple[str, ...]
    missing_terms: tuple[str, ...]


def _normalize(text: str) -> str:
    return " ".join(text.casefold().split())


def critical_term_recall(signal: str, critical_terms: list[str]) -> tuple[float, tuple[str, ...], tuple[str, ...]]:
    if not critical_terms:
        return 1.0, (), ()

    normalized = _normalize(signal)
    found = tuple(term for term in critical_terms if _normalize(term) in normalized)
    missing = tuple(term for term in critical_terms if term not in found)
    return len(found) / len(critical_terms), found, missing


def evaluate_case(case: dict, output: dict) -> CaseScore:
    signal = output["signal"]
    protected_lines = set(output.get("protected_lines", []))
    structure = check_signal(signal, protected_lines=protected_lines)
    recall, found, missing = critical_term_recall(signal, case.get("critical_terms", []))
    return CaseScore(
        case_id=case["id"],
        compliant=structure.compliant,
        critical_term_recall=recall,
        found_terms=found,
        missing_terms=missing,
    )


def evaluate(cases: list[dict], outputs: list[dict]) -> dict:
    case_by_id = {case["id"]: case for case in cases}
    scores: list[CaseScore] = []

    for output in outputs:
        case_id = output["id"]
        if case_id not in case_by_id:
            raise ValueError(f"Unknown evaluation case: {case_id}")
        scores.append(evaluate_case(case_by_id[case_id], output))

    if not scores:
        return {"cases": 0, "compliance_rate": 0.0, "mean_critical_term_recall": 0.0, "results": []}

    return {
        "cases": len(scores),
        "compliance_rate": sum(score.compliant for score in scores) / len(scores),
        "mean_critical_term_recall": sum(score.critical_term_recall for score in scores) / len(scores),
        "results": [asdict(score) for score in scores],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate saved 6X6 Signal outputs without model API calls.")
    parser.add_argument("--cases", type=Path, default=Path("evals/cases.json"))
    parser.add_argument("--outputs", type=Path, default=Path("evals/sample_outputs.json"))
    args = parser.parse_args()

    cases = json.loads(args.cases.read_text(encoding="utf-8"))
    outputs = json.loads(args.outputs.read_text(encoding="utf-8"))
    report = evaluate(cases, outputs)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
