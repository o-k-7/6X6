# Privacy

6X6 is designed to work without collecting project telemetry.

## Reference implementation

The repository's reference checker and deterministic tests:

- do not send analytics or telemetry;
- do not create user accounts;
- do not use advertising identifiers;
- do not require a hosted database;
- do not automatically upload prompts, outputs, or files;
- do not require network access to run.

## AI providers and host applications

6X6 is an output protocol and Agent Skill. When you install or paste it into a third-party AI product, that product may process or retain prompts, outputs, metadata, or files under its own privacy policy and settings.

6X6 does not control those services.

## Local evaluation data

Contributors should not commit private conversations, secrets, personal data, confidential employer information, API keys, or proprietary model outputs into evaluation fixtures.

Use synthetic or appropriately licensed test data whenever possible.

## Future changes

Any future telemetry, hosted service, crash reporting, account system, or networked feature must be opt-in where appropriate, documented here, and reviewed before release.
