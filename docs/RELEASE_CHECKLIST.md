# 6X6 release checklist

Use this checklist before tagging a release from the public repository.

## Product

- [ ] Canonical Skill exists at `skills/6x6/SKILL.md`.
- [ ] Bundled Skill reference matches normative protocol behavior.
- [ ] Universal prompt and `6X6-PROMPT.txt` match.
- [ ] Task completion is never replaced by compression.
- [ ] Signal, Expand, and Full behavior matches `SPEC.md`.
- [ ] Host-enforced behavior matches `tools/enforce.py` and documentation.
- [ ] Examples do not contradict the specification.
- [ ] Installation and compatibility documentation are current.
- [ ] A non-technical user can start from `QUICKSTART.md` without Terminal.

## Deterministic validation

- [ ] `python -m unittest discover -s tests -v` passes.
- [ ] `python tools/check_6x6.py examples/sample-signal.txt` passes.
- [ ] `python tools/security_check.py` passes.
- [ ] `python tools/release_check.py` passes.
- [ ] `python tools/evaluate.py --cases evals/cases.json --outputs evals/sample_outputs.json` passes.
- [ ] Partial evaluation fixtures cannot report a full pass.
- [ ] Host-enforcement retry and fail-closed behavior have regression tests.
- [ ] Unicode / non-English text is covered.
- [ ] Protected-content exceptions are covered.
- [ ] No deterministic test requires a paid API or hosted service.

## External behavioral acceptance

- [ ] External-model evidence is clearly separated from deterministic tests.
- [ ] Each claimed model records provider, exact model ID/version, date, runtime/host, prompt hash, instruction placement, raw synthetic input/output, retries, and result.
- [ ] Signal, Expand, Full, Hebrew, English, code, commands, URLs, numbers, structured formats, safety/correctness overrides, long context, multi-turn, and task completion are covered for every claimed model.
- [ ] Baseline (`be concise`) and 6X6 runs use comparable conditions.
- [ ] `blocked`, `not_run`, missing, duplicate, or partial evidence cannot become a pass.
- [ ] No provider-wide or universal claim is published from incomplete evidence.
- [ ] No paid inference was started without explicit authorization.

A release may ship deterministic improvements without claiming external-model certification. Any release note that claims verified compatibility with named external models requires the corresponding live evidence to exist and pass.

## Agent Skills validation

- [ ] Canonical `skills/6x6` package passes the official Agent Skills reference validator when that validator is actually available for the release environment.
- [ ] If it was not run, documentation says `not verified`; local structural tests are not described as equivalent.

## Distribution

- [ ] 30-second no-install path is visible near README top.
- [ ] `INSTALL-WITH-AI.txt` offers agent-assisted installation.
- [ ] Agent-assisted installation forbids unrelated dependencies/services.
- [ ] Claude Code, Codex, Cursor, Gemini, and generic prompt paths are documented.
- [ ] Skill installation and persistent-default activation are distinguished.
- [ ] Host-enforced mode is documented separately from instruction-only mode.
- [ ] Uninstall removes 6X6-created local configuration and leaves no 6X6 remote state.

## Legal and provenance

- [ ] `LICENSE` is present and correct.
- [ ] `LEGAL.md` reviewed for current claims.
- [ ] `PRIVACY.md` matches actual behavior.
- [ ] `SECURITY.md` matches actual attack surface.
- [ ] `THIRD_PARTY_NOTICES.md` matches bundled material and dependencies.
- [ ] `TRADEMARKS.md` contains no unsupported affiliation claims.
- [ ] `DCO.md` and contribution instructions agree.
- [ ] AI-assisted contributions remain subject to provenance and DCO obligations.
- [ ] No copied prompt, benchmark data, code, logo, model output, or documentation lacks redistribution rights.
- [ ] No medical, scientific, accessibility, endorsement, or universal-compliance claim is made without evidence.

## Privacy and secrets

- [ ] Repository contains no API keys, tokens, passwords, private URLs, confidential conversations, personal datasets, or provider credentials.
- [ ] `python tools/security_check.py` finds no credential-like material.
- [ ] Security scan includes extensionless UTF-8 files.
- [ ] Reference Python contains no unreviewed shell execution, dynamic execution, or direct provider/network client.
- [ ] Test fixtures are synthetic or redistributable.
- [ ] No telemetry, analytics, tracking, or automatic upload has been introduced without review.

## Cost guardrail

- [ ] Required installation and deterministic validation cost $0 in 6X6 infrastructure.
- [ ] No required paid API, hosted database, deployment platform, or paid runner.
- [ ] Public CI uses standard GitHub-hosted runners only.
- [ ] Live provider tests state their cost/access assumptions and are opt-in.

## Repository hygiene

- [ ] README points to the canonical Skill directory.
- [ ] Status/version text is current.
- [ ] `CHANGELOG.md` and Skill metadata agree on package version.
- [ ] Contribution and security reporting paths are documented.
- [ ] `.gitignore` excludes common local secrets and caches.
- [ ] No ambiguous root-level `SKILL.md` exists.
- [ ] Release-hardening PR diff is reviewed before merge.
- [ ] Temporary merged branches are deleted.
- [ ] Published tags/releases are preserved unless there is an explicit integrity reason to revoke them; history is not rewritten for cosmetic cleanup.

## Tagging

Only after the required checks for the intended claims pass:

1. merge the reviewed change to `main`;
2. verify CI on the merged commit;
3. verify README, Quick Start, installer, examples, and canonical Skill from `main`;
4. create the release tag at that exact verified commit;
5. verify the public release points to the intended commit;
6. delete temporary branches that are no longer needed.
