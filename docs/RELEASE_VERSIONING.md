# Release versioning

6X6 uses semantic versioning for its distribution package. The normative protocol specification has its own version because documentation-only and packaging patches need not change protocol behavior.

- Package v1.0.0: first stable public release.
- Package v1.0.1: release hygiene and documentation patch.
- Protocol v1.0.0: unchanged normative behavior in both package releases.

The root `SPEC.md` and bundled `skills/6x6/references/SPEC.md` must agree on the protocol version. Package metadata and the latest README release status must agree on the package version.

Published tags are immutable release identities. Never rewrite a published tag to conceal a mistake. Correct release defects with a new patch release and transparent changelog entry.

Historical development commits and prerelease entries are retained. A stable release does not imply the absence of earlier development versions.
