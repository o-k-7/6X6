# Compatibility

6X6 is model-agnostic: its instructions are portable, but model behavior and host support must be verified separately.

| Host | Installation | Status | Notes |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/6x6/` | Documented integration | Project and personal skill locations. |
| Codex | `.agents/skills/6x6/` | Documented integration | Supports explicit `$6x6` invocation. |
| Cursor | `.cursor/skills/6x6/` or `.agents/skills/6x6/` | Documented integration | Native and shared skill locations. |
| OpenAI / Codex | packaged skill | Compatible metadata included | `agents/openai.yaml` is optional host metadata; availability depends on the product and version. |
| Gemini CLI | host-version dependent | Prompt fallback | Use `prompts/universal.md` via `GEMINI.md` when native skill discovery is unavailable or uncertain. |
| Other LLM/chat hosts | custom/system instructions | Prompt fallback | Use `prompts/universal.md` where the host permits custom instructions. |

## What compatibility means

A documented integration identifies an installation mechanism, not a guarantee of successful installation on every host version. The repository does not claim a completed live end-to-end test on every listed host or model. Host-specific availability, permissions and instruction precedence may differ.

Model-agnostic means the core does not depend on a particular model vendor. It does not mean every model follows the format perfectly. Behavioral quality requires recorded model/version/prompt evaluations.

## Portability rule

Host-specific metadata MUST NOT become required for core 6X6 behavior. The canonical behavior lives in `skills/6x6/SKILL.md` and `skills/6x6/references/SPEC.md`.

## Cost rule

No compatibility path may require a paid 6X6 service. A user's chosen AI product or model may have its own pricing, but 6X6 itself must not introduce a required paid dependency.
