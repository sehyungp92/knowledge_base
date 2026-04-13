---
type: source
title: Untitled Article
source_id: 01KKTE8FZZ18ZR8N3QDY457BC5
source_type: article
authors: []
published_at: None
theme_ids:
- agent_systems
- ai_market_dynamics
- code_and_software_ai
- code_generation
- frontier_lab_competition
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
Now I have what I need. Let me generate the wiki page following the source page template and format established by the Movie Gen example.

```markdown
---
type: source
title: 'GLM-4.5: Reasoning, Coding, and Agentic Abilities'
source_id: 01KKTE8FZZ
source_type: article
authors:
- Zhipu AI
published_at: null
theme_ids:
- agent_systems
- ai_market_dynamics
- code_and_software_ai
- code_generation
- frontier_lab_competition
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 15
tags: []
---
# GLM-4.5: Reasoning, Coding, and Agentic Abilities

Zhipu AI's GLM-4.5 is a 355B MoE model (32B active parameters) that positions itself as a unified frontier model competitive with Claude 4 Sonnet and GPT-4.1 across agentic, reasoning, and coding benchmarks — ranking 3rd overall across 12 benchmarks against the full field of frontier labs. Its core architectural thesis is that increasing layer depth while reducing width outperforms the conventional wider-MoE approach for reasoning quality, and that a single model capable across all three capability domains is the right bet for the agentic application era. The release includes open weights, a custom RL infrastructure (`slime`), and explicit integration support for Claude Code and other agent frameworks — directly targeting the emerging ecosystem of agent orchestration tools rather than competing only as a base model.

**Authors:** Zhipu AI
**Published:** None
**Type:** Article
**Source:** https://z.ai/blog/glm-4.5
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/code_and_software_ai|Code & Software AI]], [[themes/code_generation|Code Generation]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/software_engineering_agents|Software Engineering Agents]]

---

## Architecture

### Deeper-Narrower MoE

GLM-4.5 uses 355B total / 32B active parameters; GLM-4.5-Air uses 106B total / 12B active. The defining design choice explicitly diverges from DeepSeek-V3 and Kimi K2: **reduce width (hidden dimension, number of routed experts), increase depth (number of layers)**. The empirical claim is that deeper models exhibit better reasoning capacity, and this decision shaped the entire architectural direction.

**Routing and attention:**
- **Loss-free balance routing with sigmoid gates** instead of common softmax-based routing
- **Grouped-Query Attention (GQA)** with partial RoPE
- **96 attention heads for a 5120 hidden dimension** — 2.5× more than conventional models at this scale
  - This increased head count does *not* improve training loss but **consistently enhances performance on reasoning benchmarks** (MMLU, BBH); the mechanism is acknowledged as unexplained

**Training stabilization and efficiency:**
- **Muon optimizer** instead of AdamW: accelerates convergence and tolerates larger batch sizes
- **QK-Norm** for attention logit stabilization
- **Multi-Token Prediction (MTP) layer** on both GLM-4.5 and GLM-4.5-Air to support speculative decoding during inference — latency reduction without quality loss

---

## Training Pipeline

### Pre-training

Two-stage pre-training: 15T tokens of general corpus, followed by 7T tokens of code and reasoning-specific corpus — a two-phase approach prioritizing code and reasoning specialization on top of general world knowledge, now common among post-DeepSeek-R1 frontier models. Additional domain-specific instruction data stages follow before RL.

### RL Curriculum

RL training targets **only two verifiable task types**: information-seeking QA (search-based) and software engineering tasks.

- **Search QA:** Pairs synthesized via human-in-the-loop extraction with selective obfuscation of web content — a scalable method for creating verifiable retrieval tasks with ground-truth answers.
- **Coding tasks:** Driven by execution-based feedback on real-world SWE tasks — ground truth is whether code runs correctly, not model-judged quality.

The key empirical finding: RL on these two narrow verifiable task categories **transfers to adjacent agentic abilities** not explicitly trained on, confirming a generalization hypothesis about the structure of agentic capability. Progressive difficulty curriculum was tested and found inferior to single-stage training over the full 64K context.

### `slime` Infrastructure

The custom RL infrastructure is open-sourced. Core innovation: **decoupled rollout/training engines** operating independently on separate hardware with async data generation.

- **FP8 rollouts + BF16 training** for mixed-precision throughput
- **Addresses the long-tail latency problem**: agentic RL rollouts (tool calls, web browsing, code compilation) have highly variable completion times; conventional synchronous training idles GPUs waiting for the slowest rollout in each batch

---

## Capabilities

| Capability | Maturity | Key Evidence |
|---|---|---|
| Unified reasoning/coding/agentic model (355B/32B MoE), ranked 3rd across 12 benchmarks | narrow_production | GLM-4.5 vs. full field of OpenAI, Anthropic, Google, xAI, Alibaba, Moonshot |
| Highest tool-calling success rate at 90.6% across 52 agentic coding tasks | narrow_production | Beats Claude 4 Sonnet (89.5%), Kimi K2 (86.2%), Qwen3-Coder (77.1%) |
| τ-bench agentic reliability matching Claude 4 Sonnet (Retail 79.7, Airline 60.4) | narrow_production | Competitive with the leading agentic benchmark standard |
| BFCL v3 Full function calling at 77.8 — highest among all compared models | narrow_production | o3: 72.4, Claude 4 Opus: 74.4, Claude 4 Sonnet: 75.2, Gemini 2.5 Pro: 61.2 |
| BrowseComp 26.4% — beats Claude 4 Opus (18.8%), approaches o4-mini-high (28.3%) | narrow_production | Most frontier models collapse on this task (GPT-4.1: 4.1%, Gemini 2.5 Pro: 7.6%) |
| SWE-Terminal-Bench 37.5% — beats o3 (30.2%), GPT-4.1 (30.3%), Claude 4 Sonnet (35.5%) | narrow_production | Claude 4 Opus leads at 43.2% |
| AIME24 91.0% (Avg@32) and MATH 500 98.2% | narrow_production | Competitive with o3 (90.3%), ahead of Gemini 2.5 Pro (88.7%) |
| Hybrid thinking/non-thinking mode in a single deployment | narrow_production | No model switching required; instant mode for simple queries |
| Decoupled async agentic RL infrastructure (`slime`) with FP8/BF16 mixed precision | demo | Open-sourced; solves GPU underutilization during long-horizon RL |
| Deeper-narrower MoE with 2.5× attention heads improving reasoning despite no loss improvement | research_only | 96 heads for 5120 hidden dim; mechanism unexplained |

---

## Limitations

### Capability Ceilings

**Specialization trade-offs persist across the entire field.** Despite GLM-4.5's unified ambition, no model simultaneously achieves top performance across reasoning, coding, and agentic tasks. GLM-4.5 itself trails Claude 4 Sonnet on SWE-bench Verified (64.2% vs. 70.4%) while leading on Terminal-Bench (37.5% vs. 35.5%) — benchmark choice significantly changes the capability ordering.

**HLE performance cliff.** 14.4% on Humanity's Last Exam (text subset only), a 6–10 point gap behind Gemini 2.5 Pro (21.1%), o3 (20.0%), and Grok 4 (23.9%). Genuinely novel cross-domain reasoning remains out of reach. Note: multimodal HLE questions were excluded, overstating actual capability.

**GPQA gap.** 79.1% on graduate-level science QA — 5–9 points behind Grok 4 (87.7%) and Gemini 2.5 Pro (84.4%), indicating persistent weakness in expert scientific reasoning not addressed by the current RL curriculum.

**SciCode ceiling.** 41.7% on scientific coding — the entire frontier field clusters in 37–46% regardless of overall capability tier (o3: 41.0%, Claude 4 Opus: 39.8%, Grok 4: 45.7%). Deep scientific domain knowledge required for research-grade code is a structural limitation of current training.

### Evaluation Inflation

**Avg@32 / Avg@8 reporting.** AIME24 results are reported as the average over 32 samples; GPQA over 8 samples. Single-sample pass@1 performance is substantially lower — the reported frontier numbers require 8–32× inference compute overhead and should not be compared directly to pass@1 results from other models.

**BrowseComp absolute failure rate.** 26.4% accuracy means ~74% of complex web research tasks remain unsolved. Leading this benchmark signals the field is collectively unreliable at production-scale web research.

**SWE-bench operates under constrained conditions.** Results use a 100-iteration budget and force history truncation to stay within the 128K context limit — signaling that real-world long-horizon agentic coding tasks routinely exceed current context capacity.

### Architectural Mysteries

**Attention head count mechanism unknown.** 2.5× more attention heads improve reasoning benchmarks but not training loss — a fundamental disconnect between the training objective and downstream capability that currently has no mechanistic explanation. This complicates architectural transferability.

### RL Coverage Gap

**Verifiability ceiling.** RL reward signals exist only for narrow categories with objective correctness (math, code execution). Domains requiring open-ended assessment — writing, planning, negotiation, design — cannot benefit from RLVR, limiting RL-driven improvement to indirect transfer.

---

## Open Bottlenecks

| Bottleneck | Horizon | Blocking |
|---|---|---|
| Long-tail latency in agentic RL rollouts causing GPU underutilization | months | Efficient large-scale RL training for long-horizon agentic tasks; `slime` is Zhipu AI's proposed solution |
| Verifiability ceiling: automated RL reward signals only for narrow objective-correctness domains | 1–2 years | Applying RL-driven improvement to writing, planning, negotiation, design, and other open-ended agentic domains |
| Unified multi-domain frontier excellence: no model simultaneously tops reasoning, coding, and agentic tasks | 1–2 years | Deploying a single frontier model at peak quality across all AI use cases; architecture/training trade-offs enforce a persistent capability ceiling |

---

## Key Contributions

**Decoupled async RL infrastructure (`slime`)** is the most transferable technical artifact. The insight — separate rollout engines (which interact with slow external environments) from training engines (which are GPU-bound) — is architectural rather than model-specific. It directly addresses the scaling bottleneck that makes agentic RL with tool use impractical at large batch sizes.

**Deeper-narrower MoE as an alternative scaling axis.** The conventional wisdom borrowed from language model scaling (wider hidden dimensions = more capability) appears challenged by GLM-4.5's finding that more layers with fewer experts and smaller hidden dimensions outperforms at fixed parameter count for reasoning tasks. If this holds across architectures, it has implications for how compute should be allocated in next-generation MoE designs.

**RL generalization from narrow verifiable tasks to broad agentic ability.** The finding that RL on just two task types (search QA, SWE coding) generalizes to adjacent agentic abilities reinforces a structural claim: agentic capability may not require exhaustive task-specific training, but rather transfer from tasks with strong verifiable signals. This shapes the practical roadmap for other labs.

**Agent-ecosystem integration as competitive strategy.** GLM-4.5's explicit support for Claude Code, Roo Code, and CodeGeex as deployment targets — rather than competing only as a base model API — represents a distinct go-to-market approach from most frontier models. It frames capability competition as a substitution game within established developer workflows.

---

## Broader Significance

GLM-4.5's main significance in the competitive landscape is demonstrating that a non-hyperscaler Chinese lab can achieve frontier agentic and coding parity — not just mathematical or language benchmark parity — with the leading Western frontier models. The TAU-bench Retail/Airline match with Claude 4 Sonnet and the BFCL v3 lead are qualitatively different from MMLU-style matches because they involve extended tool use in multi-turn environments rather than static multiple-choice.

The open-weight release alongside `slime` strengthens the case that the gap between frontier closed-weight and open-weight capability is compressing specifically in the agentic domain — an area where most open releases (Qwen3-Coder, DeepSeek R1) still trail meaningfully on τ-bench and BFCL.

The HLE result (14.4%) is a useful counterweight to the benchmark-leading narrative: genuine cross-domain novelty at the frontier of human knowledge remains the persistent gap, regardless of how well models perform on structured agentic benchmarks. The correlation between τ-bench performance and HLE performance appears weak — agentic reliability is a different dimension of capability than fundamental reasoning reach.
```

## Key Concepts

- [[entities/hle-humanitys-last-exam|HLE (Humanity's Last Exam)]]
- [[entities/multi-token-prediction-mtp|Multi-Token Prediction (MTP)]]
- [[entities/muon-optimizer|Muon Optimizer]]
- [[entities/qk-norm|QK-Norm]]
