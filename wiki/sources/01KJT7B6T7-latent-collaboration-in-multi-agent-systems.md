---
type: source
title: Latent Collaboration in Multi-Agent Systems
source_id: 01KJT7B6T7Y5V2MK758XQ06AY3
source_type: paper
authors:
- Jiaru Zou
- Xiyuan Yang
- Ruizhong Qiu
- Gaotang Li
- Katherine Tieu
- Pan Lu
- Ke Shen
- Hanghang Tong
- Yejin Choi
- Jingrui He
- James Zou
- Mengdi Wang
- Ling Yang
published_at: '2025-11-25 00:00:00'
theme_ids:
- agent_memory_systems
- agent_systems
- knowledge_and_memory
- latent_reasoning
- multi_agent_coordination
- reasoning_and_planning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Latent Collaboration in Multi-Agent Systems

**Authors:** Jiaru Zou, Xiyuan Yang, Ruizhong Qiu, Gaotang Li, Katherine Tieu, Pan Lu, Ke Shen, Hanghang Tong, Yejin Choi, Jingrui He, James Zou, Mengdi Wang, Ling Yang
**Published:** 2025-11-25 00:00:00
**Type:** paper

## Analysis

# Latent Collaboration in Multi-Agent Systems
2025-11-25 · paper · Jiaru Zou, Xiyuan Yang, Ruizhong Qiu, Gaotang Li, Katherine Tieu et al. (13 total)
https://arxiv.org/pdf/2511.20639

---

### Motivation & Prior Limitations
Text-based communication serves as the universal medium for LLM-based multi-agent systems (MAS), but this creates a fundamental bottleneck: forcing rich internal reasoning into discrete tokens imposes both expressiveness loss and compounded computational overhead at every agent boundary.
- Existing MAS frameworks such as ReAct, AutoGen, and CAMEL require each agent to decode its chain-of-thought to natural language, then re-encode that text as input for the next agent, introducing irreversible information compression at every handoff.
  - By Theorem 3.1, expressing the equivalent semantic content of m latent steps in text requires at least Ω(d_h·m / log|V|) tokens — for Qwen3-14B this means text is up to 471× less efficient per reasoning step.
- Prior work on latent-space reasoning (CoCoNut, RepE) and cross-model KV sharing (Cache-to-Cache) explored isolated components but not a unified framework: latent-reasoning methods were confined to single models, and cross-model latent transfer methods (Cache-to-Cache) only shared input-prompt KV caches and did not propagate newly generated reasoning content.
- No prior framework combined latent internal reasoning with latent cross-agent communication in an end-to-end, training-free setting.

---

### Proposed Approach
LatentMAS is a training-free, end-to-end framework that enables multi-agent systems to reason and communicate entirely within the continuous latent space, decoding to text only at the final output step.

- **Auto-regressive latent thought generation:** Instead of decoding tokens, each agent auto-regressively feeds the last-layer hidden state h_t back as the input embedding for the next step, producing m latent thought vectors H = [h_{t+1}, ..., h_{t+m}]. This is distinguished from standard CoT by never passing through the vocabulary projection.
  - An input-output alignment matrix W_a (computed once via ridge regression as the pseudo-inverse of W_out · W_in) maps each output hidden state back into the input embedding distribution, preventing out-of-distribution activations that would destabilize iterative latent generation. This is a lightweight d_h × d_h matrix reused across all steps.

- **Latent working memory transfer:** After completing m latent steps, each agent's full KV cache — capturing both the original input context and the newly generated latent thoughts — is extracted layer-wise and prepended to the subsequent agent's KV cache via layer-wise concatenation, before that agent begins its own latent generation.
  - This differs critically from Cache-to-Cache and similar methods, which only transfer input-prompt KV and do not transmit newly generated reasoning states. Theorem 3.3 proves this transfer is information-lossless: the receiving agent's outputs are equivalent to those it would produce if given the predecessor's full output as explicit input.

- **Architecture-agnostic design:** LatentMAS is evaluated in both sequential (planner→critic→refiner→solver) and hierarchical (domain-expert agents + summarizer) MAS configurations, demonstrating that the latent collaboration mechanism is independent of the orchestration topology.

- **Complexity advantage:** Theorem 3.4 shows LatentMAS has time complexity O((d²_h·m + d_h·m² + d_h·t·m)·L) per agent, versus O((d³_h·m/log|V| + d³_h·m²/log²|V| + d²_h·t·m/log|V|)·L + d²_h·|V|·m/log|V|) for text-based MAS at equivalent expressiveness — a reduction proportional to d_h/log|V|.

---

### Results & Capabilities
LatentMAS consistently outperforms both single-model baselines and text-based MAS across all 9 benchmarks, at all three model scales (4B, 8B, 14B Qwen3), while dramatically reducing compute.

- **Accuracy:** LatentMAS improves over the single-model baseline by an average of 14.6% (sequential) and 13.3% (hierarchical), and over text-based MAS by 2.8% (sequential) and 4.6% (hierarchical). On AIME24, Qwen3-14B improves from 63.3% (single) to 73.3% (LatentMAS hierarchical).
  - On reasoning-intensive tasks (AIME24/25, GPQA-Diamond), LatentMAS achieves comparable or higher accuracy using fewer than 50 latent steps, whereas text-based MAS requires 20K+ output tokens for full CoT trajectories.

- **Token efficiency:** LatentMAS reduces output token usage by 70.8%–83.7% versus text-based MAS, and also achieves 15.0%–60.3% lower token usage than single-agent baselines, because distributing the question across agents reduces the token burden on the final decoding agent.

- **Inference speed:** LatentMAS delivers 4×–4.3× faster end-to-end inference on average versus text-based MAS; this holds even when TextMAS baselines are accelerated with vLLM prefix caching and tensor-parallel inference, where LatentMAS still achieves 2.6×–7× speedup.

- **Latent thought semantics:** Embedding-space visualization on 300 MedQA questions shows that LatentMAS's last-layer latent thought embeddings occupy the same region as TextMAS token embeddings (semantic consistency), while covering a substantially larger region (greater expressiveness). Applying W_a improves downstream accuracy by 2.3%–5.3% over unaligned latent generation.

- **Optimal latent depth:** Performance peaks at 40–80 latent steps across ARC-C, ARC-E, and GSM8K on Qwen3-14B; beyond 80–160 steps, accuracy plateaus or slightly declines, suggesting diminishing returns from excessive latent generation.

---

### Implications
LatentMAS reframes the multi-agent communication bottleneck as an architecture problem rather than a prompting or training problem, suggesting that the standard text-as-lingua-franca assumption in MAS design is a contingent choice rather than a fundamental constraint.

- The training-free nature of the approach, combined with its model-scale generality (4B to 14B) and architecture-agnosticism, implies it

## Key Claims

1. LatentMAS is a training-free framework that enables pure latent collaboration among LLM agents through continuous latent space communication
2. Existing LLM-based multi-agent systems depend on text-based mediation for both reasoning and communication between agents
3. LatentMAS achieves up to 14.6% higher accuracy than baselines across 9 benchmarks without any additional training
4. LatentMAS reduces output token usage by 70.8%-83.7% compared to text-based MAS
5. LatentMAS provides 4x-4.3x faster end-to-end inference than text-based MAS
6. Natural language serves as the lingua franca in existing LLM-based MAS, carrying agents' internal thoughts and enabling cross-agent communication
7. In LatentMAS, reasoning unfolds by auto-regressively appending last-layer hidden representations as next-step input embeddings, replacing standard token decoding entirely
8. Directly inserting last-layer hidden states as shallow-layer input embeddings can cause out-of-distribution activations because hidden states differ statistically from learned token embeddings
9. The alignment matrix Wa is computed once per run and reused across all inference steps, making its computational overhead negligible
10. Under the Linear Representation Hypothesis, expressing m latent thoughts losslessly via text requires at least Ω(dh·m / log|V|) tokens, making latent generation O(dh/log|V|) times more efficient

## Capabilities

- Multi-agent LLM systems can collaborate entirely within continuous latent space without any text decoding between agents, using KV-cache sharing for lossless cross-agent memory transfer — achieving up to 14.6% higher accuracy, 83.7% fewer tokens, and 4.3x faster inference than text-based MAS, all wi
- LLMs can perform auto-regressive latent chain-of-thought reasoning by feeding last-layer hidden states back as input embeddings, generating continuous thought representations that are theoretically 235–471x more information-dense than token-level reasoning for models of 4B–14B scale
- KV-cache contents from one LLM can be directly prepended into a successive LLM's KV-cache to achieve lossless information transfer between agents without re-encoding, provably equivalent to passing explicit text outputs while eliminating decoding overhead
- Latent multi-agent reasoning achieves 2.6x–7x speedup over vLLM-optimized text-based MAS, requiring fewer than 50 latent steps to match or exceed tasks that require 20K+ output tokens in text-based chain-of-thought approaches

## Limitations

- Latent collaboration requires all agents to share the same underlying transformer architecture — KV-cache prepending assumes layer-wise structural compatibility, making heterogeneous multi-model collaboration (e.g., mixing GPT and Llama families) architecturally impossible under the current design
- Latent thought generation causes out-of-distribution activations when last-layer hidden states are fed back as input embeddings — the required linear alignment operator is an approximation via pseudo-inverse ridge regression, not an exact transformation, and introduces a small residual error
- Performance plateaus or degrades beyond 40–80 latent steps — excessive latent thought generation introduces redundant or harmful information, implying a hard practical ceiling on the depth of latent reasoning without training-based selection
- LatentMAS has not been evaluated on tool-use, computer-use, or open-ended agentic tasks — all benchmarks are closed-form reasoning tasks, leaving its utility for real-world autonomous agents unverified and likely incompatible with intermediate text-output requirements
- KV-cache memory footprint grows linearly with the number of agents and latent steps — the paper provides no analysis of memory overhead at scale, but concatenating full layer-wise KV caches across N agents accumulates proportionally to N × (input_length + latent_steps) × L_layers
- The framework is validated only on models of 4B–14B parameters; performance on frontier-scale models (70B+) is untested, and the training-free linear alignment operator's effectiveness at larger hidden dimensions is not established
- Post-training optimization of latent inter-agent communication protocols is entirely unexplored — agents use generic hidden representations for cross-agent signaling rather than representations trained for collaboration, leaving a known performance gap acknowledged as future work
- Latent thought expressiveness advantage scales linearly with model hidden dimension — smaller models benefit proportionally less, limiting the applicability of latent MAS to edge or small-model deployments where the efficiency case is weakest

## Bottlenecks

- Latent multi-agent collaboration is architecturally restricted to homogeneous model families — no mechanism exists for cross-architecture latent communication, blocking the broader vision of heterogeneous multi-provider agent systems collaborating in latent space
- Absence of post-training optimization for latent inter-agent communication — agents cannot learn coordinated representational conventions, capping latent MAS performance below its theoretical ceiling and leaving the approach incompetitive with trained latent collaboration methods on tasks requiring 

## Breakthroughs

- Training-free multi-agent collaboration entirely within transformer latent space: LatentMAS enables multiple LLMs to reason and communicate through KV-cache sharing and auto-regressive hidden-state generation, eliminating text as the inter-agent medium with no additional training required

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/agent_systems|agent_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/latent_reasoning|latent_reasoning]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]

## Key Concepts

- [[entities/arc-easy|ARC-Easy]]
- [[entities/gsm8k|GSM8K]]
- [[entities/kv-cache|KV Cache]]
- [[entities/qwen3|Qwen3]]
