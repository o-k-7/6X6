#!/usr/bin/env python3
"""Host-enforced 6X6 adapter.

The adapter is provider-neutral. A host supplies a callable that receives a
structured model request so the canonical 6X6 protocol can be placed in the
strongest system/developer instruction layer the provider exposes while user
content stays in the user role.

For Signal responses the adapter validates structure before release, retries with
an explicit repair instruction, and can fail closed. Expand and Full deliberately
skip the strict Signal size gate because the protocol does not constrain those
modes to 6x6 presentation targets.

The adapter cannot override provider/system safety policies. It enforces only what
the integrating host controls: instruction placement, output validation, retry,
and release of output.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal

try:
    from tools.check_6x6 import CheckResult, check_signal
except ModuleNotFoundError as exc:
    if exc.name != "tools":
        raise
    from check_6x6 import CheckResult, check_signal


ResponseMode = Literal["auto", "signal", "expand", "full"]
ResolvedMode = Literal["signal", "expand", "full"]


class EnforcementError(RuntimeError):
    """Raised when fail-closed enforcement cannot obtain an acceptable response."""


@dataclass(frozen=True)
class ModelRequest:
    """Provider-neutral request for a host-controlled model invocation.

    Integrations SHOULD map ``system_instruction`` to the strongest supported
    system/developer instruction field and ``user_content`` to the user role.
    ``repair_instruction`` and ``prior_output`` are supplied only for retries.
    """

    system_instruction: str
    user_content: str
    response_mode: ResolvedMode
    attempt: int
    repair_instruction: str | None = None
    prior_output: str | None = None

    def as_single_prompt(self) -> str:
        """Fallback rendering for hosts that expose only one text prompt.

        A single text prompt cannot create real instruction hierarchy, so hosts
        that support role-separated messages should use the structured fields
        directly instead of this fallback.
        """
        parts = [
            "<6x6_system_instruction>",
            self.system_instruction,
            "</6x6_system_instruction>",
            "",
            "<user_request>",
            self.user_content,
            "</user_request>",
        ]
        if self.repair_instruction:
            parts.extend(["", "<repair_instruction>", self.repair_instruction, "</repair_instruction>"])
        if self.prior_output is not None:
            parts.extend(["", "<prior_output>", self.prior_output, "</prior_output>"])
        return "\n".join(parts)


@dataclass(frozen=True)
class Attempt:
    number: int
    output: str
    response_mode: ResolvedMode
    structural: CheckResult | None
    semantic_ok: bool


@dataclass(frozen=True)
class EnforcementResult:
    output: str
    response_mode: ResolvedMode
    attempts: tuple[Attempt, ...]


ModelCallable = Callable[[ModelRequest], str]
SemanticValidator = Callable[[str], bool]


_FULL_RE = re.compile(r"(?:^|\b)(?:full|full explanation|complete|complete answer|in full)(?:\b|$)", re.IGNORECASE)
_EXPAND_RE = re.compile(r"(?:^|\b)(?:expand|details|detail|explain|why)(?:\b|$)", re.IGNORECASE)


def load_protocol(path: str | Path = "6X6-PROMPT.txt") -> str:
    protocol = Path(path).read_text(encoding="utf-8").strip()
    if not protocol:
        raise ValueError("6X6 protocol prompt is empty")
    return protocol


def resolve_mode(user_prompt: str, mode: ResponseMode) -> ResolvedMode:
    if mode not in {"auto", "signal", "expand", "full"}:
        raise ValueError("response_mode must be auto, signal, expand, or full")
    if mode != "auto":
        return mode

    text = user_prompt.strip()
    if _FULL_RE.search(text):
        return "full"
    if _EXPAND_RE.search(text):
        return "expand"
    return "signal"


def _repair_instruction(mode: ResolvedMode, structural: CheckResult | None, semantic_ok: bool) -> str:
    if mode == "signal":
        reason = "Signal structure failed" if structural is not None and not structural.compliant else "semantic validation failed"
        return (
            f"Repair the prior answer because {reason}. Preserve correctness, safety, task completion, "
            "requested scope, exact values, code, URLs, commands, and required formats. Return a compliant "
            "6X6 Signal. Do not describe the repair process."
        )
    return (
        "Repair the prior answer because semantic validation failed. Preserve correctness, safety, task "
        f"completion, requested scope, exact values, code, URLs, commands, and required formats. Return a {mode} "
        "response; do not force it into the Signal 6x6 size target. Do not describe the repair process."
    )


def enforce(
    invoke: ModelCallable,
    user_prompt: str,
    *,
    protocol: str | None = None,
    response_mode: ResponseMode = "auto",
    max_retries: int = 2,
    protected_lines: set[int] | None = None,
    semantic_validator: SemanticValidator | None = None,
    fail_closed: bool = True,
) -> EnforcementResult:
    """Invoke a model behind a host-controlled 6X6 compliance gate.

    Signal mode receives deterministic structure validation plus optional semantic
    validation. Expand/Full intentionally skip the strict Signal structure gate and
    rely on non-empty output plus the optional semantic validator.
    """
    if max_retries < 0:
        raise ValueError("max_retries must be >= 0")
    if not isinstance(user_prompt, str) or not user_prompt.strip():
        raise ValueError("user_prompt must not be empty")

    canonical = protocol.strip() if protocol is not None else load_protocol()
    if not canonical:
        raise ValueError("protocol must not be empty")

    mode = resolve_mode(user_prompt, response_mode)
    attempts: list[Attempt] = []
    repair: str | None = None
    prior_output: str | None = None

    for number in range(1, max_retries + 2):
        request = ModelRequest(
            system_instruction=canonical,
            user_content=user_prompt,
            response_mode=mode,
            attempt=number,
            repair_instruction=repair,
            prior_output=prior_output,
        )
        output = invoke(request)
        if not isinstance(output, str) or not output.strip():
            raise EnforcementError("model returned an empty or non-text response")

        structural = check_signal(output, protected_lines=protected_lines) if mode == "signal" else None
        semantic_ok = semantic_validator(output) if semantic_validator else True
        attempt = Attempt(number, output, mode, structural, semantic_ok)
        attempts.append(attempt)

        structure_ok = structural.compliant if structural is not None else True
        if structure_ok and semantic_ok:
            return EnforcementResult(output=output, response_mode=mode, attempts=tuple(attempts))

        if number <= max_retries:
            repair = _repair_instruction(mode, structural, semantic_ok)
            prior_output = output

    message = (
        f"6X6 enforcement failed after {len(attempts)} attempt(s); "
        "host refused to release an unacceptable response"
    )
    if fail_closed:
        raise EnforcementError(message)
    return EnforcementResult(output=attempts[-1].output, response_mode=mode, attempts=tuple(attempts))
