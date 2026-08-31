# 6X6

**36 words first. Everything else on demand.**

6X6 is an open, model-agnostic output protocol for AI assistants. It presents the essential answer first using a target of **6 lines with up to 6 words per line**, then expands only when the user asks.

The goal is simple: reduce cognitive load without sacrificing correctness.

> Status: v0.1 protocol bootstrap

## Why 6X6?

AI answers often bury the useful part under explanation. 6X6 reverses that order:

```text
Signal -> Expand -> Full
```

The first layer is intentionally small. Detail stays available instead of being forced into every response.

## Core rules

1. Put the answer first.
2. Target six short lines.
3. Target six words per line.
4. Preserve critical information and meaning.
5. Never damage code, URLs, numbers, or safety guidance to satisfy the limit.
6. Expand only when the user requests more detail.

The line and word limits are targets, not destructive constraints. Correctness always wins.

## Install / use

### Option 1: Agent Skill

Use [`SKILL.md`](SKILL.md) with an AI agent that supports Agent Skills or compatible instruction files. The canonical behavior is defined in [`SPEC.md`](SPEC.md).

### Option 2: Any chat or model

Copy the text from [`prompts/universal.md`](prompts/universal.md) into the model's system instructions, custom instructions, project instructions, or the start of a chat.

No API key is required.

## Local validation

Requires Python 3.10+ and no third-party packages.

Run all tests:

```bash
python -m unittest discover -s tests -v
```

Check a Signal block:

```bash
python tools/check_6x6.py examples/sample-signal.txt
```

Current reference suite: **8 deterministic tests** covering line limits, word limits, blank lines, and protected-content exceptions.

## Repository structure

```text
6X6/
├── SKILL.md
├── SPEC.md
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── prompts/
│   └── universal.md
├── tools/
│   └── check_6x6.py
├── tests/
│   └── test_compliance.py
└── examples/
    └── sample-signal.txt
```

## Zero-cost principle

The required development and test path must remain usable with **zero paid infrastructure**:

- no required paid model APIs;
- no hosted database;
- no paid deployment platform;
- no required third-party Python dependencies;
- no paid CI requirement.

While this repository is private, GitHub-hosted Actions are intentionally not enabled. Private repositories consume account Actions minutes and can become billable after the included quota. If the project becomes public, a standard GitHub-hosted runner can be added without Actions-minute charges under GitHub's public-repository policy.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Protocol changes should include tests and preserve the zero-cost reference path.

## License

MIT. See [`LICENSE`](LICENSE).

---

**36 words first. Everything else on demand.**
