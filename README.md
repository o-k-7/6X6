# 6X6

**36 words first. Everything else on demand.**

[![CI](https://github.com/o-k-7/6X6/actions/workflows/ci.yml/badge.svg)](https://github.com/o-k-7/6X6/actions/workflows/ci.yml)

6X6 is an open, model-agnostic progressive-disclosure protocol for AI assistants. It puts the useful part first, then expands when you ask, without sacrificing correctness, task completion, safety, code, exact values, URLs, or required formats.

> Status: **v1.0.2 stable release** · [Latest release](https://github.com/o-k-7/6X6/releases/latest)

## Try it in 30 seconds

No Terminal, Python, or 6X6 account required. Your chosen AI host may have its own account, subscription, or usage costs.

1. Open [`6X6-PROMPT.txt`](6X6-PROMPT.txt).
2. Copy all of it.
3. Paste it into your AI tool's strongest persistent instruction surface: Custom Instructions, Project Instructions, system/developer instructions, or equivalent.
4. Ask a normal question.

That is enough to try instruction-only 6X6.

Need help? Open the beginner guide: **[`QUICKSTART.md`](QUICKSTART.md)**.

## Install as a plugin

6X6 now includes installable packages for ChatGPT/Codex and Claude Code.

- ChatGPT and Codex: use the package in `plugins/6x6/`. Public directory availability depends on OpenAI review.
- Claude Code: add this repository with `/plugin marketplace add o-k-7/6X6`, then run `/plugin install 6x6@ok7-plugins`.

See [`docs/PLUGIN_INSTALLATION.md`](docs/PLUGIN_INSTALLATION.md) for installation and verification details. Installing the plugin makes the Skill available; it does not guarantee automatic use on every response.

## Before and after

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

See [`examples/BEFORE_AFTER.md`](examples/BEFORE_AFTER.md) for the full illustrative example.

## Signal, Expand, Full

Signal targets **6 non-protected lines with up to 6 words per line**. Those are presentation targets, not destructive limits.

Ask `expand`, `why`, `details`, `full`, or any ordinary follow-up for more. **Expand and Full are not constrained by the strict Signal target.** If you ask for a complete answer, 6X6 should complete it rather than forcing repeated six-line turns.

Correctness, safety, task completion, and explicit user requirements override compression. Code, commands, URLs, exact values, errors, structured data, tool arguments, and safety-critical wording stay intact when shortening would damage them.

## Make 6X6 the default

Installing a Skill and making it the default are different things.

For the strongest instruction-only setup, use both:

1. the canonical Skill in the host's supported skill directory; and
2. `6X6-PROMPT.txt` in the strongest persistent instruction layer the host exposes.

This makes 6X6 the requested default, but a third-party host/model can still deviate or apply higher-priority policies. 6X6 does not claim otherwise.

Manual installation for Claude Code, Codex, Cursor, Gemini CLI, and other hosts is documented in [`docs/INSTALLATION.md`](docs/INSTALLATION.md). See [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md) for the exact meaning of installed, explicitly invoked, persistent-default, and host-enforced modes.

## Host-enforced mode

If you control the application or agent host, 6X6 can be stronger than a prompt alone.

`tools/enforce.py` is a zero-dependency reference adapter that:

- injects the canonical 6X6 instructions for every request;
- validates returned Signal structure before release;
- retries with an explicit repair instruction;
- supports a host-provided semantic/task validator;
- can fail closed instead of releasing non-compliant output.

```python
from tools.enforce import enforce

result = enforce(
    invoke_model,
    "Explain why the sky appears blue.",
    max_retries=2,
    fail_closed=True,
)
print(result.output)
```

The host supplies `invoke_model`; 6X6 does not bundle provider credentials, SDKs, networking, or a paid inference service. Host-enforced mode cannot override provider/system safety policy, and formatting checks alone cannot prove factual correctness.

## Want your AI to install it?

If you use a coding agent:

1. open [`INSTALL-WITH-AI.txt`](INSTALL-WITH-AI.txt);
2. copy the instruction;
3. paste it into your coding agent.

The agent can install the canonical `skills/6x6/` package using its normal supported skill location and verify it. Review requested file changes and permissions before approving them.

## What gets installed?

The Skill itself is declarative Markdown plus optional host metadata:

```text
skills/6x6/
├── SKILL.md
├── agents/openai.yaml
└── references/SPEC.md
```

Instruction-only installation does not start a server, create an account, install a runtime, collect analytics, or require a 6X6 cloud service.

The optional Python tools are maintainer/integration utilities. Normal chat users do not need them.

## Developer validation

Python 3.10+ is enough. There are no required third-party Python packages.

```bash
python -m unittest discover -s tests -v
python tools/check_6x6.py examples/sample-signal.txt
python tools/evaluate.py --cases evals/cases.json --outputs evals/sample_outputs.json
python tools/security_check.py
python tools/release_check.py
```

Public CI runs deterministic validation on standard `ubuntu-latest` GitHub-hosted runners for pushes to `main` and pull requests.

If the optional Agent Skills reference validator is already installed:

```bash
skills-ref validate skills/6x6
```

The official reference validator is not bundled and is not replaced by local structural tests. A reference-validator pass should only be claimed after that validator actually ran.

## Evaluation

The offline evaluator is deterministic and zero-cost. It now fails strict evaluation when required cases are missing and never converts `blocked`, `not_run`, duplicate, unknown, or partial evidence into a pass.

It still is **not a real-model benchmark**. Structural compliance and critical-term retention are engineering signals, not proof of factual correctness or universal compatibility.

Cross-model acceptance requires recorded evidence for the exact provider, model ID/version, runtime, instruction placement, prompt hash, raw input/output, retries, and scenario set. See [`docs/MODEL_ACCEPTANCE.md`](docs/MODEL_ACCEPTANCE.md).

## Security and privacy

The repository's reference Python code has no required third-party dependency, telemetry, bundled credential, or provider SDK. `tools/enforce.py` accepts a host-supplied callable; any network/provider access belongs to that host integration.

`python tools/security_check.py` is a bounded static gate for credential-like material and unexpected execution/network primitives. It is not a comprehensive security audit. See [`SECURITY.md`](SECURITY.md) and [`PRIVACY.md`](PRIVACY.md).

## Legal and claims

6X6 is not a medical or diagnostic tool and does not claim that 36 words is scientifically optimal. It does not claim guaranteed compliance across every model or host.

The project is independently maintained and references third-party product names descriptively for interoperability. See [`LEGAL.md`](LEGAL.md), [`TRADEMARKS.md`](TRADEMARKS.md), and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Zero-cost principle

Required 6X6 installation and deterministic validation use **zero paid 6X6 infrastructure**: no required paid API, hosted database, deployment platform, third-party Python dependency, or paid CI runner.

Live external-model acceptance may involve provider-specific accounts or costs. The project must not silently create such costs or claim a live pass when access was unavailable.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md), [`DCO.md`](DCO.md), and the MIT [`LICENSE`](LICENSE).

**36 words first. Everything else on demand.**
