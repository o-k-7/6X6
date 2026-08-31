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

## Pull requests

Keep changes focused. When changing normative behavior, update `SPEC.md`, tests, and examples together.

A protocol change should explain:

1. the problem;
2. the proposed rule;
3. at least one passing example;
4. at least one edge case;
5. why correctness is preserved.

## Cost guardrail

Do not add dependencies on paid APIs, paid runners, hosted databases, or paid infrastructure to the required development or test path.

Optional integrations may be proposed later, but the reference implementation must remain fully usable without them.
