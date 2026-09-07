# Cross-model acceptance

6X6 is model-agnostic by design, not universally certified. A model is verified only after its actual output has been recorded and evaluated. A passing local fixture is not evidence of model behavior.

## Candidate coverage

Test current generally available models from OpenAI, Anthropic, Google, xAI, DeepSeek, Meta, Mistral, and Qwen. Record the exact model identifier, provider, host, date, instruction placement, sampling settings, and actual response. Do not substitute a different model or infer results from another provider. Model names and availability change; use current official documentation before execution.

## Required scenarios

1. Direct factual answer within the six-by-six target.
2. Hebrew answer and natural-language expansion.
3. Explicit full-detail request without forced truncation.
4. Exact code, commands, JSON, and user-requested formats.
5. Multi-step tool task: complete work before summarizing.
6. Safety-critical answer: preserve necessary warnings.
7. Uncertainty: do not invent facts or claim verification.
8. Conflicting lower-priority instructions: preserve instruction hierarchy.
9. Long input: retain critical facts and requested scope.
10. Skill invocation versus persistent instructions: test separately.

## Evidence and scoring

Store only synthetic, non-sensitive prompts and outputs with redistribution rights. Each run must identify the exact model and host, prompt version or commit SHA, timestamp, actual input/output, and whether tools were available. Use `not_run`, `blocked`, `pass`, or `fail`; never turn missing evidence into a pass. Report structural compliance separately from factual correctness, task completion, safety, and expansion quality. A strict-format failure does not automatically mean the answer is unsafe; a short answer does not automatically mean it is correct.

A release claim of verified compatibility requires actual runs of every required scenario on that exact model/host configuration, review of failures, and regression testing after fixes. Do not claim a universal pass from a single conversation or from self-generated examples.

## Execution and cost

The reference test suite remains offline and requires no paid API. Live provider testing is optional and must be explicitly authorized within a known cost budget. Do not request or store user API keys in the repository, enable paid services, or silently use an account with billable inference. Where access is unavailable, mark the provider blocked and preserve the untested status.

## Current evidence

As of 2026-09-07, no complete cross-provider live acceptance matrix has been established by this audit. The current chat can inspect the repository and exercise its own response behavior, but that is not an independent API run or proof of compatibility with every OpenAI model. All provider-wide certification claims remain unverified pending recorded execution.
