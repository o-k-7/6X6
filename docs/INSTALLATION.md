# Installing 6X6

6X6 is an instruction-only Agent Skill. It requires no 6X6 API key, server, database, or paid dependency.

## Easiest: let your coding agent install it

Open `INSTALL-WITH-AI.txt`, copy the instruction, and paste it into your coding agent.

The instruction tells the agent to use the canonical package at `skills/6x6/`, avoid unrelated dependencies or services, and verify the installation afterward.

If the host cannot install Agent Skills, it should tell you and fall back to `6X6-PROMPT.txt`.

## One command for Skills CLI users

After the repository is public, users who already have a compatible Skills CLI can use its repository-install flow instead of copying folders manually. Follow that CLI's own confirmation and scope prompts; 6X6 does not require installing a separate runtime of its own.

## Canonical package

```text
skills/6x6/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    └── SPEC.md
```

Manual installation means copying that entire `6x6` directory into a skill location supported by your agent.

## Claude Code

Project-scoped installation:

```bash
mkdir -p .claude/skills
cp -R /path/to/6X6/skills/6x6 .claude/skills/6x6
```

Personal installation:

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/6X6/skills/6x6 ~/.claude/skills/6x6
```

Official reference: https://code.claude.com/docs/en/skills

## Codex

Project-scoped installation:

```bash
mkdir -p .agents/skills
cp -R /path/to/6X6/skills/6x6 .agents/skills/6x6
```

Personal installation:

```bash
mkdir -p ~/.agents/skills
cp -R /path/to/6X6/skills/6x6 ~/.agents/skills/6x6
```

Then invoke explicitly with `$6x6`, or let Codex select it from the skill description.

Official reference: https://developers.openai.com/codex/build-skills

## Cursor

Project-scoped installation:

```bash
mkdir -p .cursor/skills
cp -R /path/to/6X6/skills/6x6 .cursor/skills/6x6
```

Cursor may also discover `.agents/skills/`, allowing a shared project layout where supported.

Official reference: https://cursor.com/docs/skills

## Gemini CLI

If the installed Gemini CLI build supports a compatible skill location, use its documented mechanism. Otherwise use the safe prompt fallback:

1. copy `6X6-PROMPT.txt`;
2. place the instructions in the project's `GEMINI.md` or other supported persistent context;
3. refresh/restart the session if required by the host.

Official context reference: https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html

## Any chat or model

For ordinary ChatGPT, Claude, Gemini, or another chat host, no Skill installation is necessary.

Copy `6X6-PROMPT.txt` into Custom Instructions, Project Instructions, system instructions, or the beginning of a conversation.

## Verify installation

Ask:

```text
Use 6X6. Explain why the sky appears blue.
```

Then ask:

```text
Expand line 2.
```

The first reply should be low-noise and concise. The second should expand only the requested point when its scope is clear.

## Uninstall

Delete the installed `6x6` skill directory, or remove the copied prompt from your host instructions.

6X6 creates no background process, 6X6 account, subscription, database, or remote state.
