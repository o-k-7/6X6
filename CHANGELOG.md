# Changelog

Notable stable-line changes are recorded here. Earlier pre-release development history remains available in Git and is intentionally not rewritten.

## [Unreleased]

### Added

- optional zero-dependency host-enforcement adapter with persistent protocol injection, output validation, bounded repair retries, semantic-validation hook, and fail-closed behavior;
- regression coverage for enforcement and incomplete evaluation evidence;
- strict eight-provider live-acceptance evidence validator that rejects missing, blocked, not-run, duplicate, or partial results.

### Changed

- protocol, Skill, prompt, installation, compatibility, security, privacy, legal, contribution, and release documentation now prioritize task completion and distinguish instruction-only, persistent-default, and host-enforced behavior;
- Expand and Full are explicitly outside the strict Signal presentation target;
- evaluator now requires complete evidence for a full pass;
- agent-assisted installation requests both the canonical Skill and persistent host instructions where supported;
- GitHub Actions majors updated after compatibility CI checks.

### Claims

- no universal model-compliance claim is made;
- deterministic tests are explicitly separated from external-model behavioral acceptance;
- external-model compatibility claims require actual recorded runs for the exact provider/model/host configuration.

## [1.0.1] - 2026-09-07

Patch release for public distribution consistency. No protocol behavior changes.

### Fixed

- release snapshot includes specification alignment completed after the original v1 release;
- compatibility wording distinguishes documented integrations from verified live model behavior;
- release notes and validation scope clarify the limits of automated checks.

## [1.0.0] - 2026-09-01

First stable public release of 6X6.

### Added

- canonical Agent Skill package and bundled protocol reference;
- 30-second copy/paste prompt path and non-technical Quick Start;
- agent-assisted and manual installation guidance;
- deterministic checker, evaluation harness, security gate, release gate, and regression tests;
- public zero-cost GitHub Actions validation;
- legal, privacy, security, third-party, trademark, DCO, contribution, and conduct policies.

### Protocol

- Signal → Expand → Full progressive disclosure;
- six-line / six-word Signal presentation targets for non-protected prose;
- correctness and protected content override compression;
- code, commands, URLs, exact values, errors, safety-critical wording, and required formats remain intact when shortening would damage them.
