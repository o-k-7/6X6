# Compatibility

6X6 is model-agnostic by design: the protocol does not depend on one model vendor. Model behavior, host installation, persistent activation, and host-enforced compliance are separate claims and must be verified separately.

| Host / integration | Installation | Default activation | Enforcement |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/6x6/` | Use persistent project/user instructions when desired | Instruction-only unless the surrounding host adds validation/retry |
| Codex | `.agents/skills/6x6/` | Explicit `$6x6` plus persistent instructions where supported | Instruction-only unless wrapped by a host gate |
| Cursor | `.cursor/skills/6x6/` or compatible shared skill path | Use persistent project rules/instructions | Instruction-only unless wrapped by a host gate |
| Gemini CLI | Host-version dependent Skill support; `GEMINI.md` fallback | `GEMINI.md` or another supported persistent context | Instruction-only unless wrapped by a host gate |
| ChatGPT / Claude / Gemini chat | Custom/Project/system instructions where exposed | Depends on the product's persistent-instruction surface | Host-controlled; 6X6 cannot intercept output inside a third-party chat product |
| Application / agent host you control | Canonical prompt or Skill plus model client | Inject 6X6 on every relevant request | `tools/enforce.py` reference gate: validate, retry, semantic hook, fail closed |

## What compatibility means

A documented integration identifies a supported or documented installation mechanism. It is not proof that every version of that host invokes the Skill on every turn.

`Model-agnostic` means the core protocol is portable. It does not mean every model follows the format perfectly. Behavioral compatibility requires a recorded run for the exact provider, model ID/version, host/runtime, prompt hash, and scenario set.

## Activation levels

Use precise language when describing an installation:

- **installed** — the Skill/prompt exists in a host-supported location;
- **explicitly invoked** — the user/host selected 6X6 for the request;
- **persistent default** — the host places 6X6 in a persistent instruction layer;
- **host-enforced** — the host validates before release and retries/fails closed.

Do not call a Skill `always-on` solely because it is installed.

## Portability rule

Host-specific metadata MUST NOT become required for core 6X6 behavior. Canonical behavior lives in `skills/6x6/SKILL.md` and `skills/6x6/references/SPEC.md`. `6X6-PROMPT.txt` is the portable instruction fallback.

## Behavioral evidence

The deterministic repository tests verify protocol structure, fixtures, package consistency, security guardrails, and enforcement control flow. They do not certify any external model.

Cross-model results belong in recorded acceptance evidence and must never convert `blocked`, `not_run`, missing, or partial runs into a pass. See `docs/MODEL_ACCEPTANCE.md`.

## Cost rule

No compatibility path may require a paid 6X6 service. A user's chosen AI product/model may have its own pricing. Live acceptance must not silently incur provider charges; paid inference requires explicit authorization.
