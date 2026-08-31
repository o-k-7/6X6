# Installing 6X6

6X6 is an instruction-only Agent Skill. It requires no API key, package manager, service, database, or paid dependency.

The canonical distributable folder is:

```text
skills/6x6/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    └── SPEC.md
```

Copy that entire `6x6` directory into a skill location supported by your agent.

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

Claude Code follows the Agent Skills standard and discovers skills from `.claude/skills/` and `~/.claude/skills/`.

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

Cursor also discovers `.agents/skills/`, so the Codex-compatible project layout can be shared by both tools.

Official reference: https://cursor.com/docs/skills

## Gemini CLI

Gemini CLI supports skill-style packages in its `.gemini/skills/` ecosystem. If the installed Gemini CLI version does not discover the Agent Skill automatically, use the universal prompt fallback below rather than relying on undocumented behavior.

Project fallback:

1. copy the contents of `prompts/universal.md`;
2. add them to the project's `GEMINI.md`;
3. run `/memory refresh` if the session is already open.

Official context reference: https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html

## Any chat or model

If a host does not support Agent Skills, copy the instruction block from:

```text
prompts/universal.md
```

into the host's custom instructions, system prompt, project instructions, or the beginning of a conversation.

## Verify installation

Ask:

```text
Use 6X6. Explain why the sky appears blue.
```

The first response layer should lead with the answer, remain low-noise, and target at most six non-protected lines with at most six words per non-protected line.

Then ask:

```text
Expand line 2.
```

Only the requested point should expand when its scope is clear.

## Uninstall

Delete the installed `6x6` skill directory. No background process, account, subscription, database, or remote state is created by 6X6.
