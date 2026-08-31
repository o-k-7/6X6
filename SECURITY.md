# Security Policy

## Supported versions

Until the first stable release, security fixes target the latest `main` branch and the latest tagged release, if one exists.

## Reporting a vulnerability

Please do not publish sensitive vulnerability details in a public issue.

When the repository is public and GitHub private vulnerability reporting is enabled, prefer the repository's private security reporting channel. If that channel is unavailable, open a non-sensitive issue asking the maintainer for a private reporting path without including exploit details.

For ordinary bugs that do not create a security risk, use a normal GitHub issue.

## Security model

The reference 6X6 checker:

- reads local UTF-8 text;
- performs deterministic formatting checks;
- does not execute model output;
- does not require network access;
- has no required third-party Python dependencies;
- stores no credentials;
- sends no project telemetry.

The Agent Skill itself is declarative Markdown. Host AI products retain their own security boundaries and permissions.

## Untrusted content

Treat prompts, model responses, copied commands, URLs, and third-party evaluation data as untrusted input. 6X6 formatting is not a security boundary and must never be used as evidence that generated commands or content are safe to execute.

## Dependency policy

Required runtime dependencies should remain zero unless a future capability clearly justifies one. Any new dependency requires license, provenance, maintenance, security, and cost review before release.

## Secrets

Never commit API keys, access tokens, credentials, private conversations, or confidential datasets. Test fixtures should be synthetic or appropriately licensed.
