#!/usr/bin/env python3
"""Validate schema-version 4 open-model acceptance evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_SCENARIOS = {
    "signal_en", "signal_he", "exact_command", "numbers_url",
    "full", "hierarchy", "safety_ops", "expand",
}
VALID_HOST_STATUS = {"pass", "blocked", "infrastructure_error"}


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != 4:
        return ["schema_version must be 4"]
    models = data.get("models")
    if not isinstance(models, list):
        return ["models must be a list"]

    providers = [m.get("provider") for m in models if isinstance(m, dict)]
    if len(providers) != len(set(providers)):
        errors.append("provider records must be unique")

    io_passed = host_passed = blocked = infrastructure = scenarios_total = 0
    for model in models:
        if not isinstance(model, dict):
            errors.append("model record must be an object")
            continue
        name = model.get("provider", "<unknown>")
        for field in ("provider", "model", "model_digest", "protocol_sha256", "timestamp"):
            if not isinstance(model.get(field), str) or not model[field].strip():
                errors.append(f"{name}: missing {field}")
        if not isinstance(model.get("runtime"), dict):
            errors.append(f"{name}: runtime must be an object")

        scenarios = model.get("scenarios")
        if not isinstance(scenarios, list):
            errors.append(f"{name}: scenarios must be a list")
            continue
        ids = [s.get("id") for s in scenarios if isinstance(s, dict)]
        if set(ids) != REQUIRED_SCENARIOS or len(ids) != len(REQUIRED_SCENARIOS):
            errors.append(f"{name}: scenario set is incomplete or duplicated")

        for scenario in scenarios:
            if not isinstance(scenario, dict):
                errors.append(f"{name}: scenario must be an object")
                continue
            scenario_id = scenario.get("id", "<unknown>")
            if not isinstance(scenario.get("prompt"), str) or not scenario["prompt"].strip():
                errors.append(f"{name}/{scenario_id}: missing prompt")
            instruction = scenario.get("instruction_only")
            host = scenario.get("host_enforced")
            if not isinstance(instruction, dict) or not isinstance(instruction.get("raw_final_output"), str):
                errors.append(f"{name}/{scenario_id}: missing instruction-only final output")
            else:
                score = instruction.get("score")
                if not isinstance(score, dict) or not isinstance(score.get("passed"), bool):
                    errors.append(f"{name}/{scenario_id}: invalid instruction-only score")
                else:
                    io_passed += int(score["passed"])
            if not isinstance(host, dict) or host.get("status") not in VALID_HOST_STATUS:
                errors.append(f"{name}/{scenario_id}: invalid host status")
                continue
            status = host["status"]
            released = host.get("released")
            if status == "pass":
                score = host.get("score")
                if released is not True or not isinstance(host.get("raw_final_output"), str) or not isinstance(score, dict) or score.get("passed") is not True:
                    errors.append(f"{name}/{scenario_id}: invalid released pass")
                else:
                    host_passed += 1
            elif status == "blocked":
                if released is not False:
                    errors.append(f"{name}/{scenario_id}: blocked output was released")
                blocked += 1
            else:
                if released is not False:
                    errors.append(f"{name}/{scenario_id}: infrastructure error was released")
                infrastructure += 1
            scenarios_total += 1

    expected = {
        "requested_models": 8,
        "models_executed": len(models),
        "instruction_only_passed": io_passed,
        "host_enforced_passed": host_passed,
        "blocked": blocked,
        "infrastructure_errors": infrastructure,
        "scenario_total": scenarios_total,
    }
    if data.get("summary") != expected:
        errors.append("summary does not match scenario records")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    data = json.loads(args.evidence.read_text(encoding="utf-8"))
    errors = validate(data)
    for error in errors:
        print(f"FAIL: {error}")
    if not errors:
        print("PASS: open-model evidence is internally consistent")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
