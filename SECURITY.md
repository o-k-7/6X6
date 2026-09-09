# Security Policy

## Supported versions

Security fixes target the latest `main` branch and the latest supported tagged release.

## Reporting a vulnerability

Please do not publish sensitive vulnerability details in a public issue.

When GitHub private vulnerability reporting is available, prefer the repository's private security reporting channel. If that channel is unavailable, open a non-sensitive issue asking the maintainer for a private reporting path without including exploit details.

For ordinary bugs that do not create a security risk, use a normal GitHub issue.

## Security model

6X6 has two modes:

1. **Instruction-only mode**: Markdown/YAML instructions with no 6X6 runtime, network service, or additional host permission.
2. **Host-enforced mode**: an optional local adapter (`tools/enforce.py`) that injects the canonical protocol into a host-controlled model invocation, validates returned Signal structure, retries repairs, and can fail closed instead of releasing a non-compliant response.

The enforcement adapter does not include provider credentials, networking code, shell execution, telemetry, or a bundled model client. The host supplies the model callable and remains responsible for authentication, provider policy, safety, data handling, and any inference cost.

Host-enforced mode cannot override a provider/system safety policy. Its security boundary is deliberately narrow: it controls instruction placement, validation, retry, and whether an answer is released.

The reference Python tools:

- read local UTF-8 project files where required;
- perform deterministic checks;
- print validation results;
- do not execute model output;
- do not open network connections themselves;
- do not run shell commands;
- do not modify system configuration;
- do not install software;
- have no required third-party dependencies;
- store no credentials;
- send no project telemetry.

Host AI products retain their own security boundaries and permissions. Installing 6X6 does not grant the Skill additional permissions.

## Automated repository audit

Run:

```bash
python tools/security_check.py
```

The zero-dependency gate scans repository text for common credential shapes and scans Python files for unexpected execution/network primitives. The release path must fail if such material appears unexpectedly.

This is a bounded defense-in-depth check, not a comprehensive security audit and not proof that the repository is vulnerability-free.

## Untrusted content

Treat prompts, model responses, copied commands, URLs, and third-party evaluation data as untrusted input. 6X6 formatting is not a security boundary and must never be used as evidence that generated commands or content are safe to execute.

The Skill MUST NOT instruct a host to execute commands, browse the network, read unrelated user files, alter permissions, expose secrets, or bypass another tool's safety controls merely to produce a 6X6 response.

## Dependency policy

Required runtime dependencies remain zero. Any future dependency requires license, provenance, maintenance, security, privacy, and cost review before release.

## Secrets and evaluation data

Never commit API keys, access tokens, credentials, private conversations, personal data, or confidential datasets. Behavioral evaluation fixtures must be synthetic or appropriately licensed, and live-run records must not contain provider secrets or unrelated user content.
