# Changelog

All notable project changes are recorded here.

## [Unreleased]

### Planned

- broader real-model evaluation dataset;
- public standard-runner CI after the repository becomes public;
- additional community-tested host integrations.

## [0.3.0-rc1] - 2026-08-31

### Added

- cross-agent installation guide for Claude Code, Codex, Cursor, Gemini CLI fallback, and generic chat hosts;
- compatibility matrix and portability rules;
- OpenAI host metadata in `skills/6x6/agents/openai.yaml`;
- zero-dependency public-release structure gate.

### Changed

- improved distribution guidance so users can install the canonical skill without understanding repository internals;
- bumped canonical skill metadata to `0.3.0-rc1`.

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
