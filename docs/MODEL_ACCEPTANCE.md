# Cross-model acceptance

6X6 is model-agnostic by design, not universally certified. A model is verified only after its actual output has been recorded and evaluated. A passing local fixture is not evidence of model behavior.

## Acceptance tracks

The repository keeps two different forms of evidence:

1. Provider certification targets hosted products from OpenAI, Anthropic, Google, xAI, DeepSeek, Meta, Mistral, and Qwen. `tools/live_acceptance.py` requires ten scenarios for each provider. No complete provider-certification matrix has passed.
2. The open-model engineering lab uses small local representatives from eight model families. These runs diagnose prompt and enforcement behavior, but do not certify the vendors' hosted products.

Exact hosted model names are selected from official provider documentation when a run is authorized. They are recorded in the evidence instead of maintained as a time-sensitive list in this document.

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

Three eight-family open-model lab runs are recorded under `evidence/`. The final v1.0.3 candidate run completed all 64 scenarios: instruction-only passed 15, host-enforced output passed and was released in 23, and 41 outputs were blocked. No infrastructure error was counted in that run.

The final record is validated by `tools/validate_open_evidence.py`. It includes prompts, model identifiers and digests, runtime settings, final outputs, reasoning-presence flags without reasoning text, structural and retention checks, attempts, release decisions, and failure categories.

These results are diagnostic evidence, not an 8/8 pass. The branch makes no provider-wide or universal compatibility claim. A hosted-provider certification still requires genuine evidence from every provider and scenario accepted by `tools/live_acceptance.py`.
