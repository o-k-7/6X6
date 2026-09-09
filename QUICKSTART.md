# 6X6 Quick Start

You do not need to install software, use Terminal, create a 6X6 account, or add a 6X6 API key.

## Normal ChatGPT, Claude, Gemini, or another chat app

1. Open `6X6-PROMPT.txt`.
2. Copy all of it.
3. Paste it into the strongest persistent instruction surface the app offers, such as Custom Instructions or Project Instructions.
4. Ask a normal question.

If the app only supports per-chat instructions, paste the prompt at the beginning of the conversation instead.

This is **instruction-only mode**. It requests 6X6 by default wherever the host keeps those instructions active, but the third-party host/model still controls instruction priority and can deviate.

## Coding agents

Open `INSTALL-WITH-AI.txt`, copy the instruction, and paste it into your coding agent.

The installer asks the agent to:

- install the canonical `skills/6x6/` package;
- add `6X6-PROMPT.txt` to a supported persistent instruction layer when available;
- verify what activation level was actually achieved.

If automatic installation is unsupported, use `docs/INSTALLATION.md`.

## Applications you control

If you control model invocation and want stronger enforcement, use the optional `tools/enforce.py` reference adapter. It injects 6X6, validates output, retries repair, and fails closed instead of releasing a structurally non-compliant Signal.

This **host-enforced mode** is stronger than a prompt alone, but it cannot override provider/system safety policy and its format check does not prove factual correctness.

## See the difference first

Open `examples/BEFORE_AFTER.md`.

```text
Signal, then Expand, then Full
```

You get the useful answer first. Details remain available when you ask. Full responses are not forced back into the strict Signal target.

## Test it

Ask:

```text
Explain why the sky appears blue.
```

Then ask:

```text
Expand line 2.
```

Then ask:

```text
Full explanation.
```

The first reply should be low-noise. The second should expand the requested point. The third should provide a complete useful answer rather than another forced six-line summary.

## Nothing runs in the background by default

Instruction-only 6X6 does not create an account, start a server, read files by itself, collect analytics, or require a 6X6 subscription.

The repository's optional Python validation/enforcement utilities have no bundled provider client or required third-party Python dependency. A host that connects the enforcement adapter to an external model remains responsible for that provider connection and any associated terms or costs.

Correctness, safety, task completion, exact content, and explicit user formats override compression.
