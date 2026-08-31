# Contributing to 6X6

Thanks for helping improve 6X6.

## Principles

Contributions should preserve these project goals:

- essential information first;
- lower-noise output;
- correctness before compression;
- model-agnostic behavior;
- zero-cost local development;
- no required paid APIs or hosted services.

## Development

Requirements:

- Python 3.10+
- no third-party Python packages

Run the complete test suite locally:

```bash
python -m unittest discover -s tests -v
```

Check a Signal manually:

```bash
python tools/check_6x6.py examples/sample-signal.txt
```

## Agent Skill changes

The canonical Agent Skill lives in `skills/6x6/` because the Agent Skills specification requires the skill `name` to match its parent directory.

When changing skill behavior, keep these aligned:

- `skills/6x6/SKILL.md`;
- `skills/6x6/references/SPEC.md`;
- root `SPEC.md`;
- `prompts/universal.md`;
- conformance tests.

## Pull requests

Keep changes focused. When changing normative behavior, update the specification, tests, and examples together.

A protocol change should explain:

1. the problem;
2. the proposed rule;
3. at least one passing example;
4. at least one edge case;
5. why correctness is preserved.

## Developer Certificate of Origin

6X6 uses the Developer Certificate of Origin process described in `DCO.md`.

Contributions intended for merge should be signed off:

```bash
git commit -s
```

Do not contribute code, prompts, model outputs, datasets, documentation, or other material you do not have the right to redistribute.

## Cost guardrail

Do not add dependencies on paid APIs, paid runners, hosted databases, or paid infrastructure to the required development or test path.

Optional integrations may be proposed later, but the reference implementation must remain fully usable without them.

## Security and privacy

Do not commit secrets, private conversations, confidential data, or personal datasets. Follow `SECURITY.md` for vulnerability reports and `PRIVACY.md` for data-handling expectations.
