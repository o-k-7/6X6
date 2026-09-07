# Contributing to 6X6

Thanks for helping improve 6X6.

## Principles

Contributions should preserve these project goals:

- essential information first;
- lower-noise output;
- correctness and task completion before compression;
- model-agnostic protocol behavior;
- zero-cost local development;
- no required paid APIs or hosted services;
- evidence-backed compatibility claims.

## Development

Requirements:

- Python 3.10+
- no third-party Python packages

Run the complete deterministic test suite locally:

```bash
python -m unittest discover -s tests -v
python tools/check_6x6.py examples/sample-signal.txt
python tools/evaluate.py --cases evals/cases.json --outputs evals/sample_outputs.json
python tools/security_check.py
python tools/release_check.py
```

## Agent Skill changes

The canonical Agent Skill lives in `skills/6x6/` because the Agent Skills specification requires the skill `name` to match its parent directory.

When changing protocol behavior, keep these aligned:

- `skills/6x6/SKILL.md`;
- `skills/6x6/references/SPEC.md`;
- root `SPEC.md`;
- `6X6-PROMPT.txt`;
- `prompts/universal.md`;
- conformance/regression tests.

Local package tests do not count as an official Agent Skills reference-validator run. Record that validator only when it actually executes.

## Host-enforcement changes

Changes to `tools/enforce.py` must preserve these boundaries:

- the repository does not bundle provider credentials or a provider SDK;
- the host supplies model invocation;
- output is validated before release;
- retry is bounded;
- fail-closed behavior remains available;
- higher-priority provider/system policy is never bypassed;
- formatting compliance is never presented as proof of correctness.

Add regression tests for every enforcement behavior change.

## Behavioral evaluation

Keep deterministic fixtures separate from external-model evidence.

A claim about a named model requires the exact provider/model ID or version, date, runtime/host, prompt hash, activation mode, raw synthetic input/output where redistribution is permitted, retries, and scenario result. Missing, blocked, not-run, duplicate, or partial evidence must never become a pass.

Use comparable conditions for the 6X6 run and its concise-prompt baseline. Do not trigger billable inference for project testing without explicit authorization from the account owner.

## Pull requests

Keep changes focused. When changing normative behavior, update the specification, tests, and examples together.

A protocol change should explain:

1. the problem;
2. the proposed rule;
3. at least one passing example;
4. at least one edge case;
5. why correctness and task completion are preserved.

## Developer Certificate of Origin

6X6 uses the Developer Certificate of Origin process described in `DCO.md`.

Contributions intended for merge should be signed off:

```bash
git commit -s
```

Do not contribute code, prompts, model outputs, datasets, documentation, or other material you do not have the right to redistribute.

AI-assisted work is allowed, but the human contributor remains responsible for provenance, license compatibility, correctness, and the DCO representation. Do not submit generated material if you cannot reasonably establish the right to contribute it.

## Cost guardrail

Do not add dependencies on paid APIs, paid runners, hosted databases, or paid infrastructure to the required development or deterministic test path.

Optional integrations may be proposed, but the reference protocol and deterministic validation must remain usable without them.

## Security and privacy

Do not commit secrets, private conversations, confidential data, personal datasets, or provider credentials. Follow `SECURITY.md` for vulnerability reports and `PRIVACY.md` for data-handling expectations.
