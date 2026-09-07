# Cross-model acceptance

6X6 is model-agnostic by design, not universally certified. A model is verified only after its actual output has been recorded and evaluated. A passing local fixture is not evidence of model behavior.

## Current acceptance targets

The target matrix was refreshed from vendor/model-owner documentation on 2026-09-07. These are test targets, not pass claims.

| Provider | Exact target | Selection note |
| --- | --- | --- |
| OpenAI | `gpt-5.6-sol` | Current flagship GPT-5.6 model |
| Anthropic | `claude-opus-5` | Active Opus generation |
| Google | `gemini-3.8-flash` | Current GA Gemini 3.8 Flash |
| xAI | `grok-4.6` | Current frontier Grok model |
| DeepSeek | `deepseek-v4-pro` / version `DeepSeek-V4-Pro-0813` | Current GA V4 Pro |
| Meta | `meta-llama/Llama-4-Maverick-17B-128E-Instruct` | Meta-published Llama 4 Maverick instruct weights; runtime host must be recorded |
| Mistral | `mistral-medium-3-5` | Fixed GA Mistral Medium 3.5 generation; avoid floating alias for evidence |
| Qwen / Alibaba Cloud | `qwen3.8-max-0902` | Current dated Qwen3.8-Max snapshot |

Model names and availability change. Re-check official documentation immediately before a future run instead of assuming this table remains current.

## Required scenarios

The machine-readable gate in `tools/live_acceptance.py` requires all eight providers and these behavioral areas:

1. English Signal.
2. Hebrew Signal.
3. Expand.
4. Full without forced Signal truncation.
5. Code, commands, URLs, numbers, and exact formats.
6. Safety/correctness override of compression.
7. Long context.
8. Multi-turn behavior.
9. Task completion rather than summary substitution.
10. Comparable baseline using a simple `be concise` instruction.

Skill invocation and persistent-default behavior should be tested separately when the host supports both.

## Evidence and scoring

Each live record must identify provider, exact model ID/version, host/runtime, date, prompt hash, activation mode, actual synthetic input/output, retry count, and result. Store raw outputs only where redistribution is permitted.

Use `not_run`, `blocked`, `pass`, or `fail`. `tools/live_acceptance.py` intentionally treats anything except a complete pass matrix as certification failure. Missing providers, missing scenarios, duplicate records, blocked access, and not-run cases cannot become a pass.

Report these dimensions separately during review:

- Signal structure;
- factual/correctness review;
- critical information retention;
- task completion;
- safety behavior;
- Expand/Full quality;
- exact-format preservation;
- retry count and final enforcement outcome;
- baseline comparison.

A strict-format failure does not automatically mean an answer is unsafe. A short answer does not automatically mean it is correct.

## Instruction-only versus host-enforced runs

Instruction-only testing measures whether the model/host follows the Skill or persistent prompt voluntarily.

Host-enforced testing measures the complete integration: canonical instruction injection, pre-release validation, bounded repair retry, optional semantic validation, and fail-closed/reporting behavior. A host-enforced pass does not mean the underlying model followed the first instruction attempt; retries must be recorded.

Neither mode can override higher-priority provider/system safety policy.

## Execution and cost

The deterministic repository suite and evidence validator require no paid model API. Live inference must not be silently started on a billable account, and provider credentials must never be committed to the repository.

A provider with no authorized zero-cost execution path remains `blocked`/`not_run`; it is not substituted with a fixture or with another model.

## Current evidence

As of 2026-09-07, this repository audit has not executed a complete independent eight-provider live matrix. The current ChatGPT conversation is not counted as an OpenAI acceptance run, because self-observation is not an independent provider execution under the recorded harness.

The engineering changes in this branch therefore make no 8/8, provider-wide, or universal compatibility claim. A future live certification must pass `tools/live_acceptance.py` with genuine evidence from all required providers and scenarios.
