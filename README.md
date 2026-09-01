# 6X6

**36 words first. Everything else on demand.**

6X6 is an open, model-agnostic progressive-disclosure protocol for AI assistants. It puts the useful part first, then expands only when you ask.

> Status: **v0.5.0 stable release**

## Try it in 30 seconds

No Terminal. No Python. No API key. No account. No subscription.

1. Open [`6X6-PROMPT.txt`](6X6-PROMPT.txt).
2. Copy all of it.
3. Paste it into your AI tool's Custom Instructions, Project Instructions, or the beginning of a chat.
4. Ask a normal question.

That is enough to use 6X6.

Need help? Open the beginner guide: **[`QUICKSTART.md`](QUICKSTART.md)**.

## Before → After

**Before**

> There are several ways to approach this. The right answer depends on your environment and priorities. I would first review the failing tests, inspect the authentication changes, determine whether the issue is isolated...

**With 6X6**

```text
Do not merge yet.
Two tests are still failing.
Fix the authentication regression first.
Run the full test suite.
Merge when everything passes.
```

Then ask `Expand line 3.` when you want the reasoning.

See [`examples/BEFORE_AFTER.md`](examples/BEFORE_AFTER.md) for the full example.

## Want your AI to install it?

If you use a coding agent, you do not need to know its skill-folder path.

1. Open [`INSTALL-WITH-AI.txt`](INSTALL-WITH-AI.txt).
2. Copy the instruction.
3. Paste it into your coding agent.

The agent can install the canonical `skills/6x6/` package using its normal supported skill location and verify it for you.

Manual installation for Claude Code, Codex, Cursor and other hosts is documented in [`docs/INSTALLATION.md`](docs/INSTALLATION.md). See [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md) for the support matrix.

## How it works

```text
Signal -> Expand -> Full
```

Signal targets **6 non-protected lines with up to 6 words per line**. Ask `expand`, `why`, `details`, `full`, or any normal follow-up for more.

Correctness and safety always override compression. Code, URLs, exact values, errors and safety-critical wording stay intact when shortening would damage them.

6X6 is not a medical or diagnostic tool and does not claim that 36 words is scientifically optimal. See [`LEGAL.md`](LEGAL.md).

## What gets installed?

The Skill itself is declarative Markdown plus host metadata:

```text
skills/6x6/
├── SKILL.md
├── agents/openai.yaml
└── references/SPEC.md
```

It does not start a server, create an account, install a runtime, collect analytics, or require a 6X6 cloud service.

The optional Python tools in this repository are maintainer/test utilities. Normal users do not need them.

## Developer validation

Python 3.10+ is enough. There are no required third-party Python packages.

```bash
python -m unittest discover -s tests -v
python tools/check_6x6.py examples/sample-signal.txt
python tools/evaluate.py --cases evals/cases.json --outputs evals/sample_outputs.json
python tools/security_check.py
python tools/release_check.py
```

Public CI runs the same validation on standard `ubuntu-latest` GitHub-hosted runners for pushes to `main` and pull requests.

If the optional Agent Skills reference validator is already installed:

```bash
skills-ref validate skills/6x6
```

## Security

6X6 is instruction-only. The reference tools read local project text and print validation results. They do not execute model output, call model APIs, open sockets, run shell commands, modify system configuration, install software, or send telemetry.

The repository includes a zero-dependency security gate for credential-like material and forbidden execution/network primitives. See [`SECURITY.md`](SECURITY.md).

## Evaluation

The offline evaluator measures structural 6X6 compliance and retention of predefined critical terms. It is a deterministic sanity check, not proof that every model preserves every important meaning.

Real-model claims require recorded model/version/prompt evidence before publication.

## Zero-cost principle

The required development, installation and test paths remain usable with **zero paid 6X6 infrastructure**: no required paid API, hosted database, deployment platform, third-party Python dependency, or paid CI requirement.

## Project policy

Release validation is documented in [`docs/RELEASE_CHECKLIST.md`](docs/RELEASE_CHECKLIST.md). The project maintains explicit legal, privacy, security, third-party, trademark and contribution-provenance policies.

See [`CONTRIBUTING.md`](CONTRIBUTING.md), [`DCO.md`](DCO.md), and the MIT [`LICENSE`](LICENSE).

---

**36 words first. Everything else on demand.**
