# 6X6 public release checklist

Use this checklist before making the repository public or tagging a release.

## Product

- [ ] `SPEC.md` version matches the release.
- [ ] Canonical skill exists at `skills/6x6/SKILL.md`.
- [ ] Bundled skill reference matches the normative protocol behavior.
- [ ] Universal prompt matches the same behavior.
- [ ] Examples do not contradict the specification.

## Validation

- [ ] `python -m unittest discover -s tests -v` passes locally.
- [ ] `python tools/check_6x6.py examples/sample-signal.txt` passes.
- [ ] Canonical `skills/6x6` package passes Agent Skills reference validation.
- [ ] Unicode / non-English text is covered by tests.
- [ ] Protected-content exceptions are covered by regression tests.
- [ ] No test requires a paid API or hosted service.

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
- [ ] Test fixtures are synthetic or redistributable.
- [ ] No telemetry, analytics, or automatic upload has been introduced without documentation.

## Cost guardrail

- [ ] Required development path costs $0.
- [ ] Required test path costs $0.
- [ ] No required paid API, hosted database, deployment platform, or paid runner.
- [ ] While private, GitHub Actions remain disabled.
- [ ] If public CI is enabled, only standard GitHub-hosted runners are used.

## Repository hygiene

- [ ] README install instructions point to the canonical skill directory.
- [ ] Status/version text is current.
- [ ] Contribution path and security reporting path are documented.
- [ ] `.gitignore` excludes common local secrets and caches.
- [ ] Branch / PR used for release hardening is reviewed before merge.

## Public switch

Only after every required item above passes:

1. make the repository public;
2. enable standard-runner CI if desired;
3. run the public CI once;
4. verify the public README and skill paths from a clean browser session;
5. tag the release only after those checks pass.
