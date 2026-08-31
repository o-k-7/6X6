# 6X6 public release checklist

Use this checklist before making the repository public or tagging a release.

## Product

- [ ] Canonical skill exists at `skills/6x6/SKILL.md`.
- [ ] Bundled skill reference matches the normative protocol behavior.
- [ ] Universal prompt matches the same behavior.
- [ ] `6X6-PROMPT.txt` matches the universal prompt block.
- [ ] Examples do not contradict the specification.
- [ ] Installation guide and compatibility matrix are current.
- [ ] A non-technical user can start from `QUICKSTART.md` without Terminal.

## Validation

- [ ] `python -m unittest discover -s tests -v` passes locally.
- [ ] `python tools/check_6x6.py examples/sample-signal.txt` passes.
- [ ] `python tools/security_check.py` passes.
- [ ] `python tools/release_check.py` passes.
- [ ] `python tools/evaluate.py --cases evals/cases.json --outputs evals/sample_outputs.json` passes.
- [ ] Canonical `skills/6x6` package passes Agent Skills reference validation when `skills-ref` is available.
- [ ] Unicode / non-English text is covered by tests.
- [ ] Protected-content exceptions are covered by regression tests.
- [ ] No test requires a paid API or hosted service.

## Distribution

- [ ] 30-second no-install path is visible near the top of README.
- [ ] Claude Code installation path is documented.
- [ ] Codex installation path is documented.
- [ ] Cursor installation path is documented.
- [ ] Generic prompt fallback is documented.
- [ ] Host-specific metadata is optional and does not change core behavior.
- [ ] Uninstall leaves no remote 6X6 state behind.

## Legal and provenance

- [ ] `LICENSE` is present and correct.
- [ ] `LEGAL.md` reviewed for current claims.
- [ ] `PRIVACY.md` matches actual behavior.
- [ ] `SECURITY.md` matches actual attack surface.
- [ ] `THIRD_PARTY_NOTICES.md` matches bundled material and dependencies.
- [ ] `TRADEMARKS.md` contains no unsupported affiliation claims.
- [ ] `DCO.md` and contribution instructions agree.
- [ ] No copied prompt, benchmark data, code, logo, model output, or documentation lacks clear redistribution rights.
- [ ] No medical or scientific efficacy claim is made without evidence.

## Privacy and secrets

- [ ] Repository contains no API keys, tokens, passwords, private URLs, confidential conversations, or personal datasets.
- [ ] `python tools/security_check.py` finds no credential-like material.
- [ ] Reference Python contains no unreviewed shell execution, dynamic execution, or network-client primitive.
- [ ] Test fixtures are synthetic or redistributable.
- [ ] No telemetry, analytics, tracking pixel, or automatic upload has been introduced without documentation.

## Cost guardrail

- [ ] Required development path costs $0.
- [ ] Required test path costs $0.
- [ ] No required paid API, hosted database, deployment platform, or paid runner.
- [ ] While private, GitHub Actions remain disabled.
- [ ] If public CI is enabled, only standard GitHub-hosted runners are used.

## Repository hygiene

- [ ] README points to the canonical skill directory.
- [ ] Status/version text is current.
- [ ] `CHANGELOG.md` includes the canonical skill metadata version.
- [ ] Contribution path and security reporting path are documented.
- [ ] `.gitignore` excludes common local secrets and caches.
- [ ] No ambiguous root-level `SKILL.md` exists.
- [ ] Branch / PR used for release hardening is reviewed before merge.

## Public switch

Only after every required item above passes:

1. make the repository public;
2. enable standard-runner CI only if desired;
3. run the public CI once if enabled;
4. verify the public README, quick start, prompt file, and skill paths from a clean browser session;
5. tag the release only after those checks pass.
