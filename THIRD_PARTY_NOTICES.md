# Third-Party Notices

_Last reviewed: 2026-09-07._

6X6 currently has no required third-party runtime dependencies and does not vendor third-party source code, provider SDKs, model weights, datasets, or binaries.

## Specifications and interoperability references

The project references Agent Skills and host/product documentation for interoperability. Those specifications, products, and tools are maintained independently and retain their own terms.

The repository may mention OpenAI, Anthropic, Google, Meta, xAI, DeepSeek, Mistral, Alibaba/Qwen, GitHub, Cursor, and other AI or developer products in documentation or acceptance-test plans. Names and trademarks remain the property of their respective owners; descriptive references do not imply affiliation, endorsement, or certification.

## Optional external tools and model services

Contributors may choose to use external tools such as Git, Python, GitHub Actions, an Agent Skills reference validator, or third-party model services for optional live evaluation. Those tools and services are not bundled with 6X6 and retain their own licenses, terms, privacy policies, and pricing.

The host-enforcement reference adapter does not bundle or require a provider SDK. Integrators supply their own model callable and remain responsible for any third-party dependency they add around it.

## Contribution and evaluation rule

Do not add copied prompts, source code, benchmark datasets, raw model outputs, images, documentation, or other third-party material unless its provenance and redistribution rights are documented and compatible with this repository.

Synthetic repository fixtures are preferred. If external live outputs cannot legally or contractually be redistributed, do not commit them merely to satisfy an acceptance record.

If a future release vendors or requires third-party components, this file must be updated before release.
