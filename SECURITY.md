# Security Policy

## Supported versions

Until the first stable release, security fixes target the latest `main` branch and the latest tagged release, if one exists.

## Reporting a vulnerability

Please do not publish sensitive vulnerability details in a public issue.

When the repository is public and GitHub private vulnerability reporting is enabled, prefer the repository's private security reporting channel. If that channel is unavailable, open a non-sensitive issue asking the maintainer for a private reporting path without including exploit details.

For ordinary bugs that do not create a security risk, use a normal GitHub issue.

## Security model

6X6 is instruction-only. The canonical Skill is Markdown/YAML and does not request host tools or permissions.

The reference Python tools:

- read local UTF-8 project files;
- perform deterministic checks;
- print results to standard output;
- do not execute model output;
- do not open network connections;
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

The zero-dependency gate scans repository text for common credential shapes and scans Python files for execution/network primitives that the reference implementation does not need. The release path must fail if such material appears unexpectedly.

This is a defense-in-depth check, not a claim that pattern matching can prove a repository is vulnerability-free.

## Untrusted content

Treat prompts, model responses, copied commands, URLs, and third-party evaluation data as untrusted input. 6X6 formatting is not a security boundary and must never be used as evidence that generated commands or content are safe to execute.

The Skill MUST NOT instruct a host to execute commands, browse the network, read unrelated user files, alter permissions, expose secrets, or bypass another tool's safety controls merely to produce a 6X6 response.

## Dependency policy

Required runtime dependencies should remain zero unless a future capability clearly justifies one. Any new dependency requires license, provenance, maintenance, security, and cost review before release.

## Secrets

Never commit API keys, access tokens, credentials, private conversations, or confidential datasets. Test fixtures should be synthetic or appropriately licensed.
