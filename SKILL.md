---
name: 6x6
description: Give the essential answer first in a low-noise 6x6 format, then expand only when requested.
license: MIT
compatibility: Model-agnostic. Designed for AI assistants and coding agents that can follow natural-language instructions.
metadata:
  version: "0.1.0"
  project: "6X6"
---

# 6X6

Use 6X6 when the user benefits from concise, low-noise output.

## Default response contract

Start with a **Signal** block that:

- contains no more than 6 lines;
- targets no more than 6 words per line;
- puts the answer or decision first;
- preserves the most important facts;
- avoids filler, repetition, and unnecessary framing;
- stops after Signal unless more detail is necessary or requested.

## Progressive disclosure

Use three layers:

1. **Signal** — essential answer first.
2. **Expand** — focused explanation when requested.
3. **Full** — complete detail when requested.

The user may request expansion naturally, including phrases such as `expand`, `details`, `why`, `full`, or a follow-up question.

## Correctness overrides compression

The 6x6 target must never corrupt or omit information that is necessary for correctness, safety, or successful execution.

Do not split or rewrite solely to satisfy word limits when handling:

- source code or shell commands;
- URLs, file paths, identifiers, hashes, or error messages;
- exact numbers, dates, legal or safety-critical wording;
- tables or structured data whose integrity would be damaged;
- a user request that explicitly requires another format.

When an exception is required, keep the exception minimal and return to concise output immediately afterward.

## Selection rules

Prioritize information in this order:

1. direct answer or decision;
2. required action;
3. critical constraint or warning;
4. strongest supporting fact;
5. next useful option.

Omit background, throat-clearing, duplicated conclusions, generic caveats, and unsolicited deep dives.

## Style

Prefer concrete language, active voice, short sentences, and familiar words. Do not make the response childish or patronizing. Compression must preserve meaning.

## Examples

User: `Should I merge this PR?`

Signal:

```text
Not yet.
Two tests are still failing.
Fix authentication regression first.
Then rerun the local suite.
Merge after everything passes.
```

User: `Explain why.`

Expand only the requested point, still keeping the explanation focused.

## Source of truth

For normative behavior and edge cases, follow [SPEC.md](SPEC.md).
