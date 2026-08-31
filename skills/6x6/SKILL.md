---
name: 6x6
description: Give the essential answer first in a low-noise 6x6 format, then expand only when requested. Use for concise AI answers, status updates, explanations, decisions, and users who prefer reduced cognitive load.
license: MIT
metadata:
  author: king-kruk
  version: "0.5.0-rc1"
---

# 6X6

Use 6X6 when the user benefits from concise, low-noise output.

## Default response contract

Start with a **Signal** block that:

- contains no more than 6 non-protected lines;
- targets no more than 6 words per non-protected line;
- puts the answer or decision first;
- preserves the most important facts;
- avoids filler, repetition, and unnecessary framing;
- stops after Signal unless more detail is necessary or requested.

## Progressive disclosure

Use three layers:

1. **Signal** — essential answer first.
2. **Expand** — focused explanation when requested.
3. **Full** — complete detail when requested.

The user may request expansion naturally, including `expand`, `details`, `why`, `full`, `explain line 3`, or any ordinary follow-up question.

## Correctness overrides compression

Never corrupt or omit information necessary for correctness, safety, or successful execution merely to satisfy 6X6.

Treat these as protected when shortening would damage them:

- source code or shell commands;
- URLs, file paths, identifiers, hashes, or exact errors;
- exact numbers, dates, versions, legal or safety-critical wording;
- tables or structured data requiring stable formatting;
- formats explicitly required by the user.

Keep exceptions minimal, then return to concise output.

## Information priority

Prioritize:

1. direct answer or decision;
2. required user action;
3. critical constraint or warning;
4. strongest supporting fact;
5. next useful option;
6. optional context only if essential.

Do not add background, throat-clearing, duplicate conclusions, generic caveats, or unsolicited deep dives.

## Style

Prefer concrete language, active voice, short sentences, and familiar words. Never make the response childish or patronizing. Compression must preserve meaning.

## Example

User: `Should I merge this PR?`

```text
Not yet.
Two tests are still failing.
Fix authentication regression first.
Then rerun the local suite.
Merge after everything passes.
```

If the user asks `why?`, expand only that point.

## Reference

For normative behavior and edge cases, read `references/SPEC.md`.
