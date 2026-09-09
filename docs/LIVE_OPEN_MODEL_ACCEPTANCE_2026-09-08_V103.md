# Live open-model acceptance: v1.0.3 candidate, 2026-09-08

Independent local inference on parallel GitHub-hosted Linux runners using Ollama. These are open-weight family representatives, not proprietary hosted-product certification.

| Provider/family | Model | Instruction-only | Host-enforced |
|---|---|---:|---:|
| DeepSeek | `deepseek-r1:1.5b` | 0/8 | 0/8 |
| Google | `gemma3:1b` | 1/8 | 1/8 |
| HuggingFace | `smollm2:1.7b` | 3/8 | 6/8 |
| IBM | `granite3.3:2b` | 3/8 | 5/8 |
| Meta | `llama3.2:1b` | 2/8 | 3/8 |
| Microsoft | `phi4-mini:3.8b` | 2/8 | 5/8 |
| Mistral | `ministral-3:3b` | 2/8 | 5/8 |
| Qwen | `qwen2.5:0.5b` | 2/8 | 1/8 |

Models executed: **8/8**.
Instruction-only scenarios passed: **15/64**.
Host-enforced scenarios passed/released: **26/64**.

A host-enforced failure is fail-closed: an output that did not pass the configured structural and scenario-retention gates was not released. This does not override provider safety policy and is not universal factual-correctness proof.
