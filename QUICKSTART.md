# 6X6 Quick Start

You do not need to install software, use Terminal, create an account, or add an API key.

## Choose the easiest path

### I use normal ChatGPT, Claude, Gemini, or another chat app

1. Open `6X6-PROMPT.txt`.
2. Copy all of it.
3. Paste it into Custom Instructions, Project Instructions, or the beginning of a chat.
4. Ask a normal question.

You are done.

### I use a coding agent

Open `INSTALL-WITH-AI.txt`, copy the instruction, and paste it into your coding agent.

The agent should install the canonical `skills/6x6/` package in its normal user-level skills folder and verify it for you.

If automatic installation is unsupported, use the manual instructions in `docs/INSTALLATION.md`.

## See the difference first

Before installing anything, open `examples/BEFORE_AFTER.md`.

The core idea is:

```text
Signal -> Expand -> Full
```

You get the useful answer first. Details remain available when you ask.

## Test it

Ask:

```text
Explain why the sky appears blue.
```

Then ask:

```text
Expand line 2.
```

The first reply should stay short. The second should expand only the requested point when its scope is clear.

## Nothing runs in the background

6X6 is an instruction format. It does not create an account, start a server, read your files by itself, collect analytics, or require a subscription.

The repository's optional Python tools are for maintainers and validation only. Normal users do not need to run them.

Correctness and safety always override the 6x6 size target.
