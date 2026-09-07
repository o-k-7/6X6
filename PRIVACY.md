# Privacy

6X6 is designed to work without collecting project telemetry.

## Instruction-only mode

The Skill, prompt, checker, and deterministic tests:

- do not send analytics or telemetry;
- do not create user accounts;
- do not use advertising identifiers;
- do not require a hosted database;
- do not automatically upload prompts, outputs, or files;
- do not require network access to run.

## Host-enforced mode

`tools/enforce.py` contains no provider client, credential storage, telemetry, or networking code. It accepts a callable supplied by the integrating host.

If that callable sends prompts or outputs to an external model provider, the host application is responsible for that transfer, authentication, retention settings, provider terms, privacy disclosures, and any applicable consent or data-handling obligations. 6X6 does not intercept, store, or control provider traffic on its own.

## AI providers and host applications

When you install or paste 6X6 into a third-party AI product, that product may process or retain prompts, outputs, metadata, or files under its own privacy policy and settings.

6X6 does not control those services.

## Evaluation data

Do not commit private conversations, secrets, personal data, confidential employer information, API keys, provider credentials, or unrelated proprietary content into evaluation fixtures or live-run evidence.

Use synthetic prompts and outputs that the project has the right to redistribute. Where provider terms restrict redistribution of raw outputs, keep the evidence outside the repository and record only non-restricted metadata/results needed for verification.

## Future changes

Any future telemetry, hosted service, crash reporting, account system, provider client, persistent storage, or networked feature must be documented here and reviewed for privacy, security, provenance, licensing, and cost before release.
