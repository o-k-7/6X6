# 6X6

**36 words first. Everything else on demand.**

6X6 is an open, model-agnostic output protocol for AI assistants. It presents the essential answer first using a target of **6 lines with up to 6 words per line**, then expands only when the user asks.

The goal is simple: reduce cognitive load without sacrificing correctness.

> Status: early development

## Core idea

1. Put the answer first.
2. Target six short lines.
3. Target six words per line.
4. Preserve critical information and meaning.
5. Never damage code, URLs, numbers, or safety guidance to satisfy the limit.
6. Expand only when the user requests more detail.

## Cost principle

This project is designed to remain usable and testable with **zero paid infrastructure**. The core specification and local conformance tests do not require paid APIs, hosted databases, or paid CI services.

## License

MIT. See [LICENSE](LICENSE).
