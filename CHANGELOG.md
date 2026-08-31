# Changelog

All notable project changes are recorded here.

## [Unreleased]

### Planned

- broader model-output evaluation dataset;
- public standard-runner CI after the repository becomes public;
- additional installation examples for supported agent hosts.

## [0.2.0-rc1] - 2026-08-31

### Added

- canonical Agent Skill package at `skills/6x6/`;
- bundled protocol reference for progressive loading;
- legal, privacy, security, trademark, third-party, and DCO policies;
- public-release checklist;
- zero-cost offline evaluation harness;
- initial multilingual evaluation fixtures;
- Agent Skill package conformance tests;
- public-safe `.gitignore`.

### Changed

- clarified that 6X6 limits apply to non-protected content;
- aligned the universal prompt, specification, and checker;
- expanded deterministic test coverage from 8 to 27 tests;
- prepared README and contribution guidance for public release.

### Fixed

- protected content can now exceed both mechanical line and word targets when integrity requires it;
- removed the ambiguous root `SKILL.md` layout that could violate the Agent Skills name/directory rule;
- corrected a multilingual test fixture word count.

## [0.1.0] - 2026-08-31

### Added

- initial 6X6 protocol specification;
- universal prompt;
- deterministic 6X6 checker;
- initial test suite;
- MIT license and basic contribution documentation.
