# Installing 6X6

6X6 supports two installation modes.

- **Instruction-only**: install the Skill or persistent prompt. This is the simplest option, but the host/model can still deviate.
- **Host-enforced**: the host injects 6X6 in its strongest supported instruction layer, validates the returned Signal, retries repair, and can fail closed instead of releasing non-compliant output.

Neither mode can override higher-priority provider/system safety policies.

## Easiest: let your coding agent install it

Open `INSTALL-WITH-AI.txt`, copy the instruction, and paste it into your coding agent.

The instruction tells the agent to use the canonical package at `skills/6x6/`, avoid unrelated dependencies or services, and verify the installation afterward.

If the host cannot install Agent Skills, it should tell you and fall back to persistent instructions using `6X6-PROMPT.txt`.

## Skills CLI users

Users with a compatible Skills CLI can use that CLI's repository-install flow instead of copying folders manually. Follow the CLI's own confirmation and scope prompts; 6X6 does not require a separate runtime for instruction-only mode.

## Canonical package

```text
skills/6x6/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    └── SPEC.md
```

Manual installation means copying that entire `6x6` directory into a skill location supported by your host.

## Make 6X6 the default

Skill installation and default activation are separate concerns. If you want 6X6 active for every relevant request, place `6X6-PROMPT.txt` in the highest persistent instruction layer the host allows: project instructions, repository instructions, custom instructions, or a system/developer instruction controlled by your application.

Where a host supports both persistent instructions and Skills, use both:

1. persistent instructions establish 6X6 as the default;
2. the Skill provides canonical metadata and explicit invocation;
3. the host may invoke `$6x6` or equivalent when explicit selection is available.

Do not describe ordinary Skill installation as guaranteed always-on behavior unless the host actually guarantees that behavior.

## Claude Code

Project-scoped Skill:

```bash
mkdir -p .claude/skills
cp -R /path/to/6X6/skills/6x6 .claude/skills/6x6
```

Personal Skill:

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/6X6/skills/6x6 ~/.claude/skills/6x6
```

For project-default behavior, also place the canonical 6X6 instructions in the persistent project instruction mechanism supported by Claude Code.

Official reference: https://code.claude.com/docs/en/skills

## Codex

Project-scoped Skill:

```bash
mkdir -p .agents/skills
cp -R /path/to/6X6/skills/6x6 .agents/skills/6x6
```

Personal Skill:

```bash
mkdir -p ~/.agents/skills
cp -R /path/to/6X6/skills/6x6 ~/.agents/skills/6x6
```

Invoke explicitly with `$6x6` where supported, and use persistent project/user instructions when you want 6X6 to be the default rather than relying on automatic Skill selection.

Official reference: https://developers.openai.com/codex/build-skills

## Cursor

Project-scoped installation:

```bash
mkdir -p .cursor/skills
cp -R /path/to/6X6/skills/6x6 .cursor/skills/6x6
```

Cursor may also discover `.agents/skills/` where supported. Use Cursor's persistent project rules/instructions for default activation.

Official reference: https://cursor.com/docs/skills

## Gemini CLI

If the installed Gemini CLI build supports a compatible skill location, use its documented mechanism. Otherwise use the persistent prompt path:

1. copy `6X6-PROMPT.txt`;
2. place the instructions in the project's `GEMINI.md` or other supported persistent context;
3. refresh/restart the session if required by the host.

Official context reference: https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html

## ChatGPT, Claude, Gemini and other chat hosts

Copy `6X6-PROMPT.txt` into the strongest persistent instruction surface the product exposes, such as Custom Instructions or Project Instructions. If only per-chat instructions are available, paste it at the beginning of the conversation.

This is instruction-only mode. The model may still deviate because the chat host, not 6X6, controls the actual instruction hierarchy and output path.

## Host-enforced mode

Applications and agent hosts that control model invocation can use `tools/enforce.py` as a provider-neutral reference enforcement layer. It passes a structured `ModelRequest` to your integration so the canonical protocol and user content do not need to be collapsed into the same message.

```python
from tools.enforce import ModelRequest, enforce


def invoke_model(request: ModelRequest) -> str:
    # Map request.system_instruction to the strongest system/developer
    # instruction field your provider supports.
    # Map request.user_content to the user role.
    # On retries, also include request.repair_instruction and prior_output.
    ...

result = enforce(
    invoke_model,
    "Explain why the sky appears blue.",
    max_retries=2,
    fail_closed=True,
)
print(result.output)
```

The adapter:

1. supplies the canonical 6X6 system instruction on every attempt;
2. keeps the user request separately addressable by the host;
3. validates deterministic structure before releasing Signal responses;
4. retries with an explicit repair instruction;
5. optionally runs a host-provided semantic/task validator;
6. fails closed when acceptable output cannot be established.

`Expand` and `Full` deliberately bypass the strict Signal size checker. They still receive persistent 6X6 instructions and optional semantic validation, but are allowed to be complete responses as required by the protocol.

For providers exposing only a single text prompt, `ModelRequest.as_single_prompt()` offers a fallback rendering. That fallback cannot create a real instruction hierarchy; role-separated provider APIs are stronger and are preferred when available.

This is the strongest reference mode in the repository because a non-compliant Signal does not have to be released to the user. It still cannot force a provider/model to violate higher-priority policy, and deterministic formatting checks alone cannot prove factual correctness or task completion.

## Verify installation

Ask:

```text
Use 6X6. Explain why the sky appears blue.
```

Then ask:

```text
Expand line 2.
```

Then ask:

```text
Full explanation.
```

The first reply should be low-noise and concise. Expand should focus on the requested point. Full should remain complete rather than being squeezed back into the Signal target.

For host-enforced mode, deliberately return a non-compliant Signal fixture from your test model callable and verify that the adapter retries and eventually raises `EnforcementError` when fail-closed behavior is enabled. Also verify that a long Full response is released without Signal-size rejection.

## Uninstall

Instruction-only mode: delete the installed `6x6` Skill directory and remove any copied 6X6 prompt from persistent host instructions.

Host-enforced mode: remove the adapter from the invocation path and remove the persistent prompt injection configured by your application.

6X6 creates no account, subscription, database, background process, or remote state of its own.
