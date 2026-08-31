# 6X6

**36 words first. Everything else on demand.**

6X6 is an open, model-agnostic progressive-disclosure protocol for AI assistants. It surfaces the essential answer first using a target of **6 non-protected lines with up to 6 words per line**, then expands only when the user asks.

The goal is simple: reduce output noise without sacrificing correctness.

> Status: **v0.2 release candidate**

## Why 6X6?

AI answers often bury the useful part under explanation. 6X6 reverses that order:

```text
Signal -> Expand -> Full
```

The first layer is intentionally small. Detail stays available instead of being forced into every response.

6X6 is not a claim that 36 words is scientifically optimal, and it is not a medical or diagnostic tool. See [`LEGAL.md`](LEGAL.md).

## Core rules

1. Put the answer first.
2. Target six short non-protected lines.
3. Target six words per non-protected line.
4. Preserve critical information and meaning.
5. Protect code, URLs, exact values, and safety-critical content when shortening would damage them.
6. Expand only when the user requests more detail.

Correctness always wins over compression.

## Install / use

### Option 1: Agent Skill

The canonical Agent Skill is:

```text
skills/6x6/
```

Install or copy that directory into the skills location supported by your AI agent or coding tool.

The package layout follows the public Agent Skills specification: the `name` is `6x6` and matches its parent directory.

If you already have the optional Agent Skills reference validator installed, you can validate it with:

```bash
skills-ref validate skills/6x6
```

The validator is optional. 6X6 itself has no third-party runtime dependency.

### Option 2: Any chat or model

Copy [`prompts/universal.md`](prompts/universal.md) into system instructions, custom instructions, project instructions, or the beginning of a chat.

No 6X6 API key, server, database, or hosted service is required.

## Local validation

Requires Python 3.10+ and no third-party Python packages.

Run all tests:

```bash
python -m unittest discover -s tests -v
```

Check a Signal block:

```bash
python tools/check_6x6.py examples/sample-signal.txt
```

The v0.2 reference suite contains **21 deterministic tests** covering formatting, protected-content behavior, Unicode text, parser edge cases, and the canonical Agent Skill package structure.

## Repository structure

```text
6X6/
├── skills/
│   └── 6x6/
│       ├── SKILL.md
│       └── references/
│           └── SPEC.md
├── SPEC.md
├── prompts/
│   └── universal.md
├── tools/
│   └── check_6x6.py
├── tests/
│   ├── test_compliance.py
│   └── test_skill_package.py
├── examples/
│   └── sample-signal.txt
├── docs/
│   └── RELEASE_CHECKLIST.md
├── LEGAL.md
├── PRIVACY.md
├── SECURITY.md
├── THIRD_PARTY_NOTICES.md
├── TRADEMARKS.md
├── DCO.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── LICENSE
```

## Zero-cost principle

The required development and test path must remain usable with **zero paid infrastructure**:

- no required paid model APIs;
- no hosted database;
- no paid deployment platform;
- no required third-party Python dependencies;
- no paid CI requirement.

While this repository is private, GitHub-hosted Actions are intentionally not enabled. If the project becomes public, only standard GitHub-hosted runners should be used for project CI under the zero-cost policy.

## Public-release policy

Before a public release, follow [`docs/RELEASE_CHECKLIST.md`](docs/RELEASE_CHECKLIST.md). The project also maintains explicit policies for legal claims, privacy, security, third-party material, trademarks, and inbound contribution provenance.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`DCO.md`](DCO.md). Protocol changes should include tests and preserve the zero-cost reference path.

## License

MIT. See [`LICENSE`](LICENSE).

---

**36 words first. Everything else on demand.**
