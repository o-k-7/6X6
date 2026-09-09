# 6X6 Protocol Specification

Version: 1.0.0

6X6 is a progressive-disclosure output protocol for AI systems. Its purpose is to surface the most useful information first while preserving correctness, task completion, safety, and exact user-required content.

## 1. Terminology

**Signal**: the first response layer containing the essential answer or next action.

**Expand**: a focused explanation of one or more requested parts.

**Full**: a complete useful response when the user requests full detail.

**Protected content**: content whose integrity is more important than the 6x6 presentation target, including code, commands, URLs, identifiers, exact values, safety-critical text, and user-required formats.

**Instruction-only mode**: 6X6 is supplied as a Skill or prompt and compliance depends on host/model instruction following.

**Host-enforced mode**: a host controls prompt injection and output release, validates compliance, retries repairs, and may fail closed.

## 2. Normative requirements

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are used as requirement levels.

### 2.1 Signal

A compliant implementation:

- MUST put the direct answer, decision, or next action first.
- MUST preserve information required for correctness, safety, and successful completion of the user's requested task.
- MUST NOT replace requested work with a short summary merely to satisfy 6X6.
- MUST NOT claim an action, tool call, test, deployment, verification, or other external result succeeded without evidence.
- MUST NOT invent facts to make an answer shorter.
- MUST NOT omit a critical warning solely to satisfy the line or word target.
- SHOULD use no more than 6 non-protected visible content lines.
- SHOULD use no more than 6 natural-language words per non-protected line.
- SHOULD avoid filler, repeated conclusions, introductions, and unsolicited background.
- SHOULD stop after Signal for a simple completed request unless expansion is required for correctness or requested by the user.

The line and word limits are presentation targets rather than destructive constraints. Correctness, safety, task completion, and explicit user requirements override compression.

### 2.2 Expansion

When the user requests more information, the implementation MUST expand the requested scope when that scope can be determined.

Natural-language expansion requests MAY include:

- `expand`
- `details`
- `why`
- `explain line 3`
- `full`
- any ordinary follow-up question

Expand and Full are not subject to the strict Signal target. A user who explicitly requests a complete answer MUST NOT be forced through repeated six-line disclosures.

### 2.3 Protected content

Protected content MAY exceed six words or six lines when shortening it would damage meaning, correctness, safety, execution, or a required format.

Protected content includes:

- code and shell commands;
- URLs and file paths;
- hashes, IDs, package names, and exact error messages;
- exact numbers, dates, and version strings;
- legal, medical, security, or safety-critical wording;
- tables, JSON, machine-readable output, or data structures requiring stable formatting;
- quoted text or creative content when exact form matters;
- formats explicitly required by the user.

Protected lines are excluded from mechanical line and word targets in deterministic conformance fixtures. An implementation SHOULD keep exceptions as small as possible and MUST NOT label ordinary prose as protected merely to bypass the target.

Tool arguments, machine-readable output, and instructions intended for another system MUST NOT be altered merely to satisfy the 6X6 presentation target.

## 3. Information priority

When compression is required, rank candidate information in this order:

1. direct answer or decision;
2. required user action or completed action result;
3. critical constraint or warning;
4. strongest supporting fact;
5. next useful option;
6. optional context.

Optional context SHOULD move to Expand or Full.

## 4. Word counting

For deterministic conformance tests, a word is a whitespace-separated token after trimming surrounding whitespace.

Blank lines are ignored. Explicitly protected physical lines are excluded from mechanical line and word targets.

This definition exists for testing only. Implementations SHOULD optimize for readability rather than gaming tokenization.

## 5. Response modes

### Signal mode

Default for simple requests. Return the essential completed answer layer.

### Expand mode

Return focused detail about the user's requested point. Concision remains preferred, but the strict Signal target does not apply.

### Full mode

Return the complete useful answer. Normal quality, correctness, safety, and user-format requirements apply. The strict Signal target does not apply.

## 6. Enforcement modes

### Instruction-only

A Skill, custom instruction, project instruction, system/developer prompt, or conversation prompt requests 6X6 behavior. Installation alone MUST NOT be represented as proof that the host invokes the Skill on every turn.

### Host-enforced

A host MAY provide stronger enforcement by:

1. injecting the canonical 6X6 instruction for every relevant request;
2. validating output before release;
3. retrying with an explicit repair instruction after failure;
4. applying semantic/task-completion validation where available;
5. failing closed or explicitly reporting non-compliance when acceptable output cannot be established.

Host-enforced mode MUST NOT be described as capable of overriding higher-priority provider/system safety policy. Formatting validation MUST NOT be represented as proof of factual correctness.

## 7. Non-goals

6X6 is not:

- a claim that 36 words is scientifically optimal;
- a medical treatment or diagnostic tool;
- a replacement for accessibility standards;
- a summarizer that discards necessary information;
- a requirement to force code into six-word lines;
- a reason to ignore explicit user formatting requests;
- a universal guarantee that every model will obey every instruction.

## 8. Conformance levels

**Core compliant**: follows ordering, correctness, safety, task-completion, and protected-content requirements.

**Signal compliant**: Core compliant and satisfies the 6-line target for non-protected Signal content.

**Strict 6X6 compliant**: Signal compliant and every non-protected Signal line contains at most 6 words.

**Host-enforced compliant**: the host applies persistent injection, pre-release validation, bounded retry, and fail-closed or explicit non-compliance behavior. This level describes the host integration, not guaranteed model obedience.

## 9. Design principle

**36 words first. Everything else on demand.**
