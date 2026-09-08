# Live open-model acceptance: v1.0.3 final candidate

Run: [34261230323](https://github.com/o-k-7/6X6/actions/runs/34261230323)
Tested commit: `9d52858aede22d50d96d28befee6233584130d80`

This run used local Ollama inference on eight parallel GitHub-hosted Linux runners. It separated final content from model reasoning, never recorded reasoning text, used a 2,048-token output budget for DeepSeek R1, recorded model digests exposed by Ollama, and classified provider failures separately from blocked output.

| Family | Model | Instruction-only | Host-enforced | Blocked | Infrastructure errors |
|---|---|---:|---:|---:|---:|
| DeepSeek | `deepseek-r1:1.5b` | 1/8 | 3/8 | 5 | 0 |
| Google | `gemma3:1b` | 0/8 | 2/8 | 6 | 0 |
| HuggingFace | `smollm2:1.7b` | 3/8 | 5/8 | 3 | 0 |
| IBM | `granite3.3:2b` | 3/8 | 3/8 | 5 | 0 |
| Meta | `llama3.2:1b` | 3/8 | 2/8 | 6 | 0 |
| Microsoft | `phi4-mini:3.8b` | 2/8 | 4/8 | 4 | 0 |
| Mistral | `ministral-3:3b` | 2/8 | 3/8 | 5 | 0 |
| Qwen | `qwen2.5:0.5b` | 1/8 | 1/8 | 7 | 0 |

Totals: instruction-only **15/64**; host-enforced released passes **23/64**; blocked **41/64**; infrastructure errors **0/64**.

Blocked output is not counted as a pass. Workflow success means the experiment completed, not that the candidate passed acceptance. The results do not justify an eight-model compatibility claim or a v1.0.3 release.

The DeepSeek baseline produced non-empty final content with the larger budget, and host enforcement passed 3/8 scenarios. This supports the diagnosis that the earlier all-empty result was at least partly a harness/output-budget issue; it does not prove protocol compatibility.

Full raw final outputs, prompts, model/runtime metadata, reasoning-presence booleans, attempts, structural and retention checks, release decisions, and failure classifications are stored in `evidence/live-open-models-2026-09-08-v103-final.json`.
