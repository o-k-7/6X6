# Live open-model acceptance — 2026-09-07

Independent local inference on parallel GitHub-hosted Linux runners using Ollama. This is open-weight family coverage, not certification of proprietary ChatGPT, Claude, Gemini, or other hosted products.

| Provider/family | Model | Instruction-only | Host-enforced | Status |
|---|---|---:|---:|---|
| DeepSeek | `deepseek-r1:1.5b` | 0/8 | 1/8 | executed |
| Google | `gemma3:1b` | 1/8 | 1/8 | executed |
| HuggingFace | `smollm2:1.7b` | 3/8 | 3/8 | executed |
| IBM | `granite3.3:2b` | 3/8 | 2/8 | executed |
| Meta | `llama3.2:1b` | 3/8 | 2/8 | executed |
| Microsoft | `phi4-mini:3.8b` | 2/8 | 5/8 | executed |
| Mistral | `ministral-3:3b` | 2/8 | 3/8 | executed |
| Qwen | `qwen2.5:0.5b` | 1/8 | 2/8 | executed |

Models executed: **8/8**.

Raw prompts, outputs, retry counts, scores, runtime metadata, and blocked cases are stored in `evidence/live-open-models-2026-09-07.json`.

A host-enforced pass means the adapter released only an output that passed this run’s structural and scenario-retention gates. It is not proof of universal factual correctness and cannot override higher-priority provider safety policy.
