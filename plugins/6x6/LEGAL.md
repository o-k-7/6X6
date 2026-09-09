# 6X6 legal policy

_Last reviewed: 2026-09-07._

This document records project policy and engineering controls. It is not legal advice or a legal opinion.

## Project license

6X6 source code and project documentation are released under the MIT License in `LICENSE`, except where a file explicitly states otherwise.

Contributors retain copyright in their contributions while licensing accepted contributions under the project's outbound license. See `DCO.md`.

## Purpose and claims

6X6 is a low-noise progressive-disclosure output protocol for AI systems. The project does not claim that six lines, six words per line, or 36 words is scientifically optimal for ADHD, accessibility, learning, cognition, or any medical condition.

6X6 is not a medical device, diagnostic tool, treatment, therapy, or substitute for professional medical or accessibility guidance.

The project does not claim universal model compliance. Instruction-only mode depends on host/model behavior. Host-enforced mode can control prompt injection, validation, retry, and output release inside an application that adopts it, but it cannot override higher-priority provider/system policy and cannot prove factual correctness from formatting alone.

## Third-party systems

6X6 can be used with third-party AI assistants, coding agents, model providers, and clients. Those products retain their own licenses, terms, privacy practices, safety policies, and usage costs. The 6X6 license grants no rights to third-party software, models, services, trademarks, or content.

The repository does not bundle provider SDKs, provider credentials, or paid model APIs. The optional host-enforcement reference accepts a host-supplied model callable and does not itself provide inference.

## Agent Skills compatibility

References to Agent Skills describe compatibility with public host/specification mechanisms. They do not imply ownership of, certification by, sponsorship by, or affiliation with any vendor or standards maintainer.

## Trademark and affiliation

6X6 is an independent open-source project. References to OpenAI, ChatGPT, Claude, Anthropic, Gemini, Google, GitHub, Cursor, Codex, Meta, Llama, Qwen, DeepSeek, Mistral, xAI, Grok, or other products are descriptive only unless explicitly stated otherwise.

No compatibility statement should be interpreted as endorsement, partnership, certification, or trademark clearance. See `TRADEMARKS.md`.

## Evaluation evidence

Deterministic fixtures and repository tests are engineering checks, not independent proof of external-model quality. A compatibility or benchmark claim about a named external model requires recorded evidence for that exact provider/model/host configuration. Missing, blocked, or partial runs must not be reported as passes.

Raw model outputs may be subject to provider terms or other rights. Only synthetic prompts and outputs that the project has the right to redistribute should be committed. Provider credentials, personal data, confidential conversations, and unrelated user content must not be included in evaluation evidence.

## AI-assisted contributions

Use of AI assistance does not change the contributor's responsibility for provenance, licensing, correctness, and the Developer Certificate of Origin. A contributor must have the right to submit the contribution and must not knowingly include copied third-party material whose license is incompatible with the project.

## Privacy

The reference checker, deterministic tests, and enforcement control logic include no project telemetry, analytics, advertising, hosted database, account system, or automatic network upload. A host that connects `tools/enforce.py` to an external model provider is responsible for the provider's data handling and must follow that provider's terms and privacy practices. See `PRIVACY.md`.

## Security

The reference tools do not execute model output. Host integrations must treat model output as untrusted. Security reports should follow `SECURITY.md`.

## Third-party materials

The project currently vendors no third-party runtime libraries. External specifications and product names are referenced for interoperability and documentation. See `THIRD_PARTY_NOTICES.md`.

## Future changes

Any future dependency, bundled dataset, copied code, hosted service, telemetry feature, provider integration, or paid infrastructure requires a fresh license, privacy, security, provenance, and cost review before release.
