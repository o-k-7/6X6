#!/usr/bin/env python3
"""Host-enforced 6X6 adapter.

This module does not call any provider API. A host supplies a callable that invokes
its model. The adapter injects the canonical protocol, validates the returned
Signal structure, retries with an explicit repair instruction, and fails closed
when compliance cannot be established.

The adapter cannot override provider/system safety policies. It enforces what the
host controls: prompt placement, output validation, retry, and release of output.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

try:
    from tools.check_6x6 import CheckResult, check_signal
except ModuleNotFoundError as exc:
    if exc.name != "tools":
        raise
    from check_6x6 import CheckResult, check_signal


class EnforcementError(RuntimeError):
    """Raised when fail-closed enforcement cannot obtain a compliant response."""


@dataclass(frozen=True)
class Attempt:
    number: int
    output: str
    structural: CheckResult
    semantic_ok: bool


@dataclass(frozen=True)
class EnforcementResult:
    output: str
    attempts: tuple[Attempt, ...]


ModelCallable = Callable[[str], str]
SemanticValidator = Callable[[str], bool]


def load_protocol(path: str | Path = "6X6-PROMPT.txt") -> str:
    protocol = Path(path).read_text(encoding="utf-8").strip()
    if not protocol:
        raise ValueError("6X6 protocol prompt is empty")
    return protocol


def _compose_initial(protocol: str, user_prompt: str) -> str:
    return (
        "<6x6_protocol>\n"
        f"{protocol}\n"
        "</6x6_protocol>\n\n"
        "The protocol above is a persistent host instruction for this request. "
        "Follow it unless a higher-priority provider/system policy conflicts.\n\n"
        "<user_request>\n"
        f"{user_prompt}\n"
        "</user_request>"
    )


def _compose_repair(protocol: str, user_prompt: str, prior_output: str) -> str:
    return (
        "<6x6_protocol>\n"
        f"{protocol}\n"
        "</6x6_protocol>\n\n"
        "Repair the prior answer. Preserve correctness, safety, requested scope, "
        "exact values and required formats. Return a compliant Signal unless the "
        "user explicitly requested Expand or Full. Do not describe the repair.\n\n"
        "<user_request>\n"
        f"{user_prompt}\n"
        "</user_request>\n\n"
        "<prior_output>\n"
        f"{prior_output}\n"
        "</prior_output>"
    )


def enforce(
    invoke: ModelCallable,
    user_prompt: str,
    *,
    protocol: str | None = None,
    max_retries: int = 2,
    protected_lines: set[int] | None = None,
    semantic_validator: SemanticValidator | None = None,
    fail_closed: bool = True,
) -> EnforcementResult:
    """Invoke a model behind a host-controlled 6X6 compliance gate.

    Structural validation is deterministic. Semantic validation is optional and
    host-defined because correctness/task-completion cannot be proven by line and
    word counts alone.
    """
    if max_retries < 0:
        raise ValueError("max_retries must be >= 0")
    if not user_prompt.strip():
        raise ValueError("user_prompt must not be empty")

    canonical = protocol.strip() if protocol is not None else load_protocol()
    if not canonical:
        raise ValueError("protocol must not be empty")

    attempts: list[Attempt] = []
    prompt = _compose_initial(canonical, user_prompt)

    for number in range(1, max_retries + 2):
        output = invoke(prompt)
        if not isinstance(output, str) or not output.strip():
            raise EnforcementError("model returned an empty or non-text response")

        structural = check_signal(output, protected_lines=protected_lines)
        semantic_ok = semantic_validator(output) if semantic_validator else True
        attempt = Attempt(number, output, structural, semantic_ok)
        attempts.append(attempt)

        if structural.compliant and semantic_ok:
            return EnforcementResult(output=output, attempts=tuple(attempts))

        if number <= max_retries:
            prompt = _compose_repair(canonical, user_prompt, output)

    message = (
        f"6X6 enforcement failed after {len(attempts)} attempt(s); "
        "host refused to release a non-compliant response"
    )
    if fail_closed:
        raise EnforcementError(message)
    return EnforcementResult(output=attempts[-1].output, attempts=tuple(attempts))
