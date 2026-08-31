# Changelog

All notable project changes are recorded here.

## [Unreleased]

### Planned

- broader real-model evaluation dataset;
- public standard-runner CI after the repository becomes public;
- additional community-tested host integrations.

## [0.5.0-rc1] - 2026-08-31

### Added

- `INSTALL-WITH-AI.txt` so a coding agent can perform its own supported Skill installation;
- immediate Before -> After example for first-time visitors;
- clearer two-path Quick Start for chat users and coding-agent users.

### Changed

- README now demonstrates the result before explaining implementation details;
- security scanner now uses Python AST inspection for imports and execution/network calls;
- security scanning covers extensionless UTF-8 project files up to a bounded size;
- canonical skill metadata bumped to `0.5.0-rc1`.

### Security

- added AST detection for process/network imports and dynamic execution;
- added bearer-token detection and extensionless-file secret scanning;
- expanded security regression coverage.

## [0.4.0-rc1] - 2026-08-31

### Added

- `QUICKSTART.md` for non-technical users;
- `6X6-PROMPT.txt` as a zero-install copy/paste entry point;
- zero-dependency repository security audit;
- security-audit regression tests.

### Changed

- README now leads with a 30-second no-Terminal path;
- release gate requires beginner-facing and security assets;
- security policy explicitly documents no-network, no-shell, no-telemetry behavior;
- canonical skill metadata bumped to `0.4.0-rc1`.

### Security

- scanned for common credential shapes;
- blocked shell execution, dynamic execution, and network-client primitives from reference Python source unless explicitly reviewed in a future change;
- documented that 6X6 never grants host permissions or treats generated output as trusted.

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
