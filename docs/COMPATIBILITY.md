# Compatibility

6X6 is model-agnostic. The portable core is the Agent Skills `SKILL.md` package plus the universal prompt fallback.

| Host | Native Skill path | Status | Notes |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/6x6/` | Supported | Follows Agent Skills; supports project and personal skills. |
| Codex | `.agents/skills/6x6/` | Supported | Uses Agent Skills and supports explicit `$6x6` invocation. |
| Cursor | `.cursor/skills/6x6/` or `.agents/skills/6x6/` | Supported | Cursor discovers both native and shared Agent Skills locations. |
| ChatGPT / Codex skill UI | packaged skill | Compatible metadata included | `agents/openai.yaml` provides optional OpenAI host metadata. |
| Gemini CLI | host-version dependent | Fallback supported | Use `prompts/universal.md` via `GEMINI.md` when native skill discovery is unavailable or uncertain. |
| Other LLM/chat hosts | custom/system instructions | Supported fallback | Use `prompts/universal.md`. |

## What "supported" means

For 6X6, support means the host can load the instruction package without requiring paid 6X6 infrastructure. It does not guarantee every model will follow the format perfectly on every prompt.

Behavior quality must be measured separately with the evaluation harness.

## Portability rule

Host-specific metadata MUST NOT become required for core 6X6 behavior. The canonical behavior lives in `skills/6x6/SKILL.md` and `skills/6x6/references/SPEC.md`.

## Cost rule

No compatibility path may require a paid 6X6 service. A user's chosen AI product or model may have its own pricing, but 6X6 itself must not introduce a required paid dependency.
