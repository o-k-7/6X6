# 6X6

**36 words first. Everything else on demand.**

6X6 is an open, model-agnostic progressive-disclosure protocol for AI assistants. It puts the useful part first, then expands only when you ask.

> Status: **v0.4 public-release candidate**

## Start in 30 seconds — no install

You do **not** need Terminal, Python, an API key, an account, or a subscription.

1. Open [`6X6-PROMPT.txt`](6X6-PROMPT.txt).
2. Copy all the text.
3. Paste it into your AI tool's Custom Instructions, Project Instructions, system prompt, or the beginning of a chat.
4. Ask a normal question.

For a beginner-friendly walkthrough, open [`QUICKSTART.md`](QUICKSTART.md).

## What changes?

Normal AI answers often bury the useful part under explanation. 6X6 uses progressive disclosure:

```text
Signal -> Expand -> Full
```

The first layer targets **6 non-protected lines with up to 6 words per line**. If you want more, ask `expand`, `why`, `details`, `full`, or a normal follow-up question.

Correctness and safety always override compression.

6X6 is not a claim that 36 words is scientifically optimal, and it is not a medical or diagnostic tool. See [`LEGAL.md`](LEGAL.md).

## Install as an Agent Skill

For Claude Code, Codex, Cursor and compatible hosts, the canonical Agent Skill is:

```text
skills/6x6/
```

See [`docs/INSTALLATION.md`](docs/INSTALLATION.md) for exact steps and [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md) for the support matrix.

No 6X6 server, database, telemetry service, package installation, or paid infrastructure is required.

## Core rules

1. Put the answer first.
2. Target six short non-protected lines.
3. Target six words per non-protected line.
4. Preserve critical information and meaning.
5. Protect code, URLs, exact values, and safety-critical content when shortening would damage them.
6. Expand only when more detail is requested.

## Local validation

Developers can run everything with Python 3.10+ and no third-party packages:

```bash
python -m unittest discover -s tests -v
python tools/check_6x6.py examples/sample-signal.txt
python tools/evaluate.py --cases evals/cases.json --outputs evals/sample_outputs.json
python tools/security_check.py
python tools/release_check.py
```

If the optional Agent Skills reference validator is already installed:

```bash
skills-ref validate skills/6x6
```

## Security model

6X6 is instruction-only. The reference tools read local text and print results. They do not execute model output, call model APIs, open sockets, run shell commands, write system configuration, install software, or collect telemetry.

The repository includes a zero-dependency security gate that scans for credential-like material and forbidden execution/network primitives before release. See [`SECURITY.md`](SECURITY.md).

## Evaluation

The offline evaluator measures mechanical 6X6 compliance and retention of predefined critical terms. It is a deterministic sanity check, not proof that every model preserves all important meaning.

Real-model claims must be backed by recorded model/version/prompt results before publication.

## Zero-cost principle

The required development and test path must remain usable with **zero paid infrastructure**: no required paid model APIs, hosted database, deployment platform, third-party Python dependency, or paid CI requirement.

While this repository is private, GitHub-hosted Actions remain disabled. If the project becomes public, only standard GitHub-hosted runners should be used for project CI under the zero-cost policy.

## Project policy

Before a public release, follow [`docs/RELEASE_CHECKLIST.md`](docs/RELEASE_CHECKLIST.md). The project maintains explicit policies for legal claims, privacy, security, third-party material, trademarks, and inbound contribution provenance.

See [`CONTRIBUTING.md`](CONTRIBUTING.md), [`DCO.md`](DCO.md), and the MIT [`LICENSE`](LICENSE).

---

**36 words first. Everything else on demand.**
