# 6X6 Protocol Specification

Version: 1.0.0

6X6 is a progressive-disclosure output protocol for AI systems. Its purpose is to surface the most useful information first while preserving correctness.

## 1. Terminology

**Signal**: the first response layer containing the essential answer.

**Expand**: a focused explanation of one or more parts of Signal.

**Full**: a complete response when the user requests full detail.

**Protected content**: content whose integrity is more important than the 6x6 target, including code, commands, URLs, identifiers, exact values, safety-critical text, and user-required formats.

## 2. Normative requirements

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are used as requirement levels.

### 2.1 Signal

A compliant implementation:

- MUST put the direct answer, decision, or next action first.
- MUST preserve information required for correctness and safety.
- MUST NOT invent facts to make an answer shorter.
- MUST NOT omit a critical warning solely to satisfy the line or word target.
- SHOULD use no more than 6 non-protected visible content lines.
- SHOULD use no more than 6 natural-language words per non-protected line.
- SHOULD avoid filler, repeated conclusions, introductions, and unsolicited background.
- SHOULD stop after Signal unless expansion is required for correctness.

The limits are targets rather than destructive constraints. Correctness overrides compression.

### 2.2 Expansion

When the user requests more information, the implementation MUST expand only the requested scope when that scope can be determined.

Natural-language expansion requests MAY include:

- `expand`
- `details`
- `why`
- `explain line 3`
- `full`
- any ordinary follow-up question

### 2.3 Protected content

Protected content MAY exceed six words or six lines when shortening it would damage meaning or execution.

Protected content includes:

- code and shell commands;
- URLs and file paths;
- hashes, IDs, package names, and exact error messages;
- exact numbers, dates, and version strings;
- legal, medical, security, or safety-critical wording;
- tables or data structures that require stable formatting;
- formats explicitly required by the user.

Protected lines are excluded from mechanical line and word targets in conformance fixtures. An implementation SHOULD keep exceptions as small as possible and MUST NOT label ordinary prose as protected merely to bypass the target.

## 3. Information priority

When compression is required, rank candidate information in this order:

1. direct answer or decision;
2. required user action;
3. critical constraint or warning;
4. strongest supporting fact;
5. next useful option;
6. optional context.

Optional context SHOULD move to Expand or Full.

## 4. Word counting

For deterministic conformance tests, a word is a whitespace-separated token after trimming surrounding whitespace.

Blank lines are ignored. Explicitly protected physical lines are excluded from mechanical line and word targets.

This definition exists for testing only. Implementations SHOULD optimize for readability rather than gaming tokenization.

## 5. Modes

### Signal mode

Default. Return only the essential layer.

### Expand mode

Return focused detail about the user's requested point. Concision remains preferred, but the strict Signal target does not apply.

### Full mode

Return the complete useful answer. Normal quality and safety requirements apply.

## 6. Non-goals

6X6 is not:

- a claim that 36 words is scientifically optimal;
- a medical treatment or diagnostic tool;
- a replacement for accessibility standards;
- a summarizer that discards necessary information;
- a requirement to force code into six-word lines;
- a reason to ignore explicit user formatting requests.

## 7. Conformance levels

**Core compliant**: follows ordering, safety, and protected-content requirements.

**Signal compliant**: Core compliant and satisfies the 6-line target for non-protected Signal content.

**Strict 6X6 compliant**: Signal compliant and every non-protected Signal line contains at most 6 words.

## 8. Design principle

**36 words first. Everything else on demand.**
