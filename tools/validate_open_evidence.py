#!/usr/bin/env python3
"""Validate schema-version 4 open-model acceptance evidence."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re

REQUIRED_SCENARIOS = {
    "signal_en", "signal_he", "exact_command", "numbers_url",
    "full", "hierarchy", "safety_ops", "expand",
}
REQUIRED_PROVIDERS = {
    "DeepSeek", "Google", "HuggingFace", "IBM",
    "Meta", "Microsoft", "Mistral", "Qwen",
}
EXPECTED_MODES = {scenario: "signal" for scenario in REQUIRED_SCENARIOS}
EXPECTED_MODES.update({"expand": "expand", "full": "full"})
VALID_HOST_STATUS = {"pass", "blocked", "infrastructure_error"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _is_positive_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _valid_score(score: object) -> bool:
    return (
        isinstance(score, dict)
        and isinstance(score.get("nonempty"), bool)
        and isinstance(score.get("passed"), bool)
    )


def validate(data: dict) -> list[str]:
    if not isinstance(data, dict):
        return ["evidence must be an object"]
    errors: list[str] = []
    if data.get("schema_version") != 4:
        return ["schema_version must be 4"]
    models = data.get("models")
    if not isinstance(models, list):
        return ["models must be a list"]
    if len(models) != len(REQUIRED_PROVIDERS):
        errors.append("models must contain exactly 8 records")

    providers = [m.get("provider") for m in models if isinstance(m, dict)]
    string_providers = [provider for provider in providers if isinstance(provider, str)]
    if len(string_providers) != len(set(string_providers)):
        errors.append("provider records must be unique")
    if set(string_providers) != REQUIRED_PROVIDERS or len(string_providers) != len(providers):
        errors.append("provider set is incomplete or unexpected")

    protocol_hashes: set[str] = set()

    io_passed = host_passed = blocked = infrastructure = scenarios_total = 0
    for model in models:
        if not isinstance(model, dict):
            errors.append("model record must be an object")
            continue
        name = model.get("provider", "<unknown>")
        for field in ("provider", "model", "model_digest", "protocol_sha256", "timestamp"):
            if not isinstance(model.get(field), str) or not model[field].strip():
                errors.append(f"{name}: missing {field}")
        if isinstance(model.get("model_digest"), str) and not SHA256_RE.fullmatch(model["model_digest"]):
            errors.append(f"{name}: invalid model_digest")
        protocol_hash = model.get("protocol_sha256")
        if isinstance(protocol_hash, str):
            protocol_hashes.add(protocol_hash)
            if not SHA256_RE.fullmatch(protocol_hash):
                errors.append(f"{name}: invalid protocol_sha256")
        timestamp = model.get("timestamp")
        if isinstance(timestamp, str):
            try:
                datetime.fromisoformat(timestamp)
            except ValueError:
                errors.append(f"{name}: invalid timestamp")

        runtime = model.get("runtime")
        if not isinstance(runtime, dict):
            errors.append(f"{name}: runtime must be an object")
        else:
            if not isinstance(runtime.get("ollama"), dict):
                errors.append(f"{name}: missing Ollama runtime metadata")
            for field in ("num_predict", "num_ctx"):
                if not _is_positive_int(runtime.get(field)):
                    errors.append(f"{name}: invalid runtime {field}")
            temperature = runtime.get("temperature")
            if not isinstance(temperature, (int, float)) or isinstance(temperature, bool):
                errors.append(f"{name}: invalid runtime temperature")

        baseline = model.get("baseline")
        if not isinstance(baseline, dict):
            errors.append(f"{name}: missing baseline")
        else:
            if not isinstance(baseline.get("raw_final_output"), str):
                errors.append(f"{name}: missing baseline final output")
            if not isinstance(baseline.get("thinking_present"), bool):
                errors.append(f"{name}: invalid baseline reasoning flag")
            if not _valid_score(baseline.get("score")):
                errors.append(f"{name}: invalid baseline score")

        scenarios = model.get("scenarios")
        if not isinstance(scenarios, list):
            errors.append(f"{name}: scenarios must be a list")
            continue
        ids = [s.get("id") for s in scenarios if isinstance(s, dict)]
        string_ids = [scenario_id for scenario_id in ids if isinstance(scenario_id, str)]
        if set(string_ids) != REQUIRED_SCENARIOS or len(string_ids) != len(REQUIRED_SCENARIOS) or len(string_ids) != len(ids):
            errors.append(f"{name}: scenario set is incomplete or duplicated")

        for scenario in scenarios:
            if not isinstance(scenario, dict):
                errors.append(f"{name}: scenario must be an object")
                continue
            scenario_id = scenario.get("id", "<unknown>")
            if scenario.get("mode") != EXPECTED_MODES.get(scenario_id):
                errors.append(f"{name}/{scenario_id}: invalid mode")
            if not isinstance(scenario.get("prompt"), str) or not scenario["prompt"].strip():
                errors.append(f"{name}/{scenario_id}: missing prompt")
            instruction = scenario.get("instruction_only")
            host = scenario.get("host_enforced")
            if not isinstance(instruction, dict) or not isinstance(instruction.get("raw_final_output"), str):
                errors.append(f"{name}/{scenario_id}: missing instruction-only final output")
            else:
                score = instruction.get("score")
                if not isinstance(instruction.get("thinking_present"), bool):
                    errors.append(f"{name}/{scenario_id}: invalid instruction-only reasoning flag")
                if not isinstance(instruction.get("done_reason"), str):
                    errors.append(f"{name}/{scenario_id}: invalid instruction-only done reason")
                if not _valid_score(score):
                    errors.append(f"{name}/{scenario_id}: invalid instruction-only score")
                else:
                    io_passed += int(score["passed"])
            if not isinstance(host, dict) or host.get("status") not in VALID_HOST_STATUS:
                errors.append(f"{name}/{scenario_id}: invalid host status")
                continue
            status = host["status"]
            released = host.get("released")
            attempts = host.get("attempts")
            provider_attempts = host.get("provider_attempts")
            if not isinstance(attempts, list) or not attempts:
                errors.append(f"{name}/{scenario_id}: missing attempt metadata")
                attempts = []
            if not isinstance(provider_attempts, list) or len(provider_attempts) != len(attempts):
                errors.append(f"{name}/{scenario_id}: provider attempt metadata mismatch")
                provider_attempts = []
            for index, attempt in enumerate(attempts, 1):
                if not isinstance(attempt, dict) or attempt.get("number") != index:
                    errors.append(f"{name}/{scenario_id}: invalid attempt numbering")
                    continue
                for field in ("nonempty", "semantic_ok", "reflowed"):
                    if not isinstance(attempt.get(field), bool):
                        errors.append(f"{name}/{scenario_id}: invalid attempt {field}")
            for provider_attempt in provider_attempts:
                if not isinstance(provider_attempt, dict) or not isinstance(provider_attempt.get("thinking_present"), bool):
                    errors.append(f"{name}/{scenario_id}: invalid provider reasoning flag")
                if not isinstance(provider_attempt, dict) or not isinstance(provider_attempt.get("done_reason"), str):
                    errors.append(f"{name}/{scenario_id}: invalid provider done reason")
            if status == "pass":
                score = host.get("score")
                output = host.get("raw_final_output")
                if released is not True or not isinstance(output, str) or not output.strip() or not _valid_score(score) or score.get("passed") is not True:
                    errors.append(f"{name}/{scenario_id}: invalid released pass")
                else:
                    host_passed += 1
            elif status == "blocked":
                if released is not False:
                    errors.append(f"{name}/{scenario_id}: blocked output was released")
                if not isinstance(host.get("failure_reason"), str) or not host["failure_reason"]:
                    errors.append(f"{name}/{scenario_id}: blocked output lacks failure reason")
                blocked += 1
            else:
                if released is not False:
                    errors.append(f"{name}/{scenario_id}: infrastructure error was released")
                if not isinstance(host.get("failure_reason"), str) or not host["failure_reason"]:
                    errors.append(f"{name}/{scenario_id}: infrastructure error lacks failure reason")
                infrastructure += 1
            scenarios_total += 1

    if len(protocol_hashes) != 1:
        errors.append("model records must share one protocol hash")

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
