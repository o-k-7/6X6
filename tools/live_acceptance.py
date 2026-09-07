#!/usr/bin/env python3
"""Strict validator for recorded live-model acceptance evidence.

This tool never calls model APIs. It validates evidence produced by an external
runner. A certification pass requires every required provider and scenario to
have executed successfully; blocked, not_run, missing, duplicate, or partial
records fail closed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

REQUIRED_PROVIDERS = (
    "openai",
    "anthropic",
    "google",
    "xai",
    "deepseek",
    "meta",
    "mistral",
    "qwen",
)

REQUIRED_SCENARIOS = (
    "signal_en",
    "signal_he",
    "expand",
    "full",
    "code_commands_urls_numbers_formats",
    "safety_correctness_override",
    "long_context",
    "multi_turn",
    "task_completion",
    "baseline_be_concise",
)

VALID_STATUS = {"pass", "fail", "blocked", "not_run"}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    models = data.get("models")
    if not isinstance(models, list):
        return ["models must be a list"]

    providers = [item.get("provider") for item in models if isinstance(item, dict)]
    if len(providers) != len(set(providers)):
        errors.append("duplicate provider records")

    missing_providers = sorted(set(REQUIRED_PROVIDERS) - set(providers))
    extra_providers = sorted(set(providers) - set(REQUIRED_PROVIDERS))
    if missing_providers:
        errors.append("missing providers: " + ", ".join(missing_providers))
    if extra_providers:
        errors.append("unexpected providers: " + ", ".join(extra_providers))

    for item in models:
        if not isinstance(item, dict):
            errors.append("model record must be an object")
            continue
        provider = item.get("provider", "<unknown>")
        for field in ("model_id", "model_version", "date", "runtime", "prompt_sha256", "activation"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"{provider}: missing {field}")
        scenarios = item.get("scenarios")
        if not isinstance(scenarios, list):
            errors.append(f"{provider}: scenarios must be a list")
            continue
        ids = [scenario.get("id") for scenario in scenarios if isinstance(scenario, dict)]
        if len(ids) != len(set(ids)):
            errors.append(f"{provider}: duplicate scenario records")
        missing = sorted(set(REQUIRED_SCENARIOS) - set(ids))
        if missing:
            errors.append(f"{provider}: missing scenarios: {', '.join(missing)}")
        for scenario in scenarios:
            if not isinstance(scenario, dict):
                errors.append(f"{provider}: scenario must be an object")
                continue
            scenario_id = scenario.get("id", "<unknown>")
            status = scenario.get("status")
            if status not in VALID_STATUS:
                errors.append(f"{provider}/{scenario_id}: invalid status {status!r}")
                continue
            if status != "pass":
                errors.append(f"{provider}/{scenario_id}: status is {status}, not pass")
            for field in ("input", "output_6x6"):
                if not isinstance(scenario.get(field), str) or not scenario[field].strip():
                    errors.append(f"{provider}/{scenario_id}: missing raw {field}")
            if scenario_id == "baseline_be_concise":
                if not isinstance(scenario.get("output_baseline"), str) or not scenario["output_baseline"].strip():
                    errors.append(f"{provider}/{scenario_id}: missing baseline output")
            retries = scenario.get("retries")
            if not isinstance(retries, int) or retries < 0:
                errors.append(f"{provider}/{scenario_id}: retries must be a non-negative integer")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate complete eight-provider live acceptance evidence.")
    parser.add_argument("evidence", type=Path, nargs="?", default=Path("evals/live/evidence.json"))
    args = parser.parse_args()
    data = json.loads(args.evidence.read_text(encoding="utf-8"))
    errors = validate(data)
    report = {
        "required_providers": list(REQUIRED_PROVIDERS),
        "required_scenarios": list(REQUIRED_SCENARIOS),
        "passed": not errors,
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
