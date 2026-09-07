#!/usr/bin/env python3
"""Offline 6X6 evaluation harness.

Evaluates recorded outputs without calling model APIs. Missing, duplicate, blocked,
or not-run cases fail strict evaluation so partial fixtures cannot produce a
misleading 100% score.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

try:
    from tools.check_6x6 import check_signal
except ModuleNotFoundError as exc:
    if exc.name != "tools":
        raise
    from check_6x6 import check_signal


VALID_STATUSES = {"pass", "fail", "blocked", "not_run"}


@dataclass(frozen=True)
class CaseScore:
    case_id: str
    status: str
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
    status = output.get("status", "pass")
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status for {output.get('id')}: {status}")
    signal = output.get("signal", "")
    if status in {"blocked", "not_run"}:
        return CaseScore(case["id"], status, False, 0.0, (), tuple(case.get("critical_terms", [])))
    if not signal.strip():
        raise ValueError(f"Missing signal for executed case: {case['id']}")
    protected_lines = set(output.get("protected_lines", []))
    structure = check_signal(signal, protected_lines=protected_lines)
    recall, found, missing = critical_term_recall(signal, case.get("critical_terms", []))
    passed = status == "pass" and structure.compliant and recall == 1.0
    return CaseScore(case["id"], "pass" if passed else "fail", structure.compliant, recall, found, missing)


def evaluate(cases: list[dict], outputs: list[dict], *, require_complete: bool = True) -> dict:
    case_ids = [case["id"] for case in cases]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("Duplicate case IDs in evaluation cases")
    output_ids = [output["id"] for output in outputs]
    if len(output_ids) != len(set(output_ids)):
        raise ValueError("Duplicate output IDs in evaluation outputs")

    case_by_id = {case["id"]: case for case in cases}
    unknown = sorted(set(output_ids) - set(case_ids))
    if unknown:
        raise ValueError("Unknown evaluation case(s): " + ", ".join(unknown))

    missing = sorted(set(case_ids) - set(output_ids))
    if require_complete and missing:
        raise ValueError("Missing evaluation output(s): " + ", ".join(missing))

    scores = [evaluate_case(case_by_id[output["id"]], output) for output in outputs]
    executed = [score for score in scores if score.status not in {"blocked", "not_run"}]
    passed = [score for score in scores if score.status == "pass"]
    complete = not missing and len(scores) == len(cases)
    all_passed = complete and len(passed) == len(cases)

    return {
        "required_cases": len(cases),
        "reported_cases": len(scores),
        "complete": complete,
        "all_passed": all_passed,
        "missing_cases": missing,
        "executed_cases": len(executed),
        "pass_rate": (len(passed) / len(cases)) if cases else 0.0,
        "mean_critical_term_recall": (
            sum(score.critical_term_recall for score in executed) / len(executed) if executed else 0.0
        ),
        "results": [asdict(score) for score in scores],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate recorded 6X6 outputs without model API calls.")
    parser.add_argument("--cases", type=Path, default=Path("evals/cases.json"))
    parser.add_argument("--outputs", type=Path, default=Path("evals/sample_outputs.json"))
    parser.add_argument("--allow-partial", action="store_true", help="Report partial evidence without treating missing cases as an input error")
    args = parser.parse_args()

    cases = json.loads(args.cases.read_text(encoding="utf-8"))
    outputs = json.loads(args.outputs.read_text(encoding="utf-8"))
    try:
        report = evaluate(cases, outputs, require_complete=not args.allow_partial)
    except ValueError as exc:
        print(json.dumps({"error": str(exc), "all_passed": False}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
