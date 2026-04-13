---
type: source
title: How DeepSeek Changes the LLM Story
source_id: 01KJVHGZW34PWGWSDERWAG5QZ1
source_type: video
authors: []
published_at: '2025-02-04 00:00:00'
theme_ids:
- adaptive_computation
- ai_market_dynamics
- frontier_lab_competition
- model_architecture
- model_commoditization_and_open_source
- pretraining_and_scaling
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# How DeepSeek Changes the LLM Story

This source provides a comprehensive technical and strategic overview of DeepSeek's model lineage, arguing that DeepSeek-V3 represents a genuine infrastructural breakthrough in LLM pre-training efficiency while R1 disrupts OpenAI's monopoly on frontier reasoning models — together reshaping assumptions about compute requirements, open-source viability, and the future trajectory of AI scaling.

**Authors:** (not specified)
**Published:** 2025-02-04
**Type:** video

---

## Background and Context

DeepSeek's rise culminated in two back-to-back shocks to the AI establishment. First, NVIDIA lost approximately $600 billion in market valuation following DeepSeek's release — despite the fact that DeepSeek trained on NVIDIA chips. Second, [[entities/openai|OpenAI]]'s Sam Altman publicly acknowledged the company may be "on the wrong side of history" regarding open model weights — a dramatic reversal for a company that had resisted releases for years.

The source contextualizes these events against DeepSeek's 12-month publication history:

| Date | Paper | Significance |
|------|-------|--------------|
| Jan 2024 | DeepSeek LLM | First version; strong coding model |
| Jan 2024 | DeepSeek-Coder | Data curation for code |
| Jan 2024 | DeepSeekMoE | MoE architecture foundations |
| Jun 2024 | DeepSeek-V2 | MoE at production scale; adopted in real products |
| Dec 2024 | DeepSeek-V3 | Frontier-competitive pre-training for ~$6M |
| Jan 2025 | DeepSeek-R1 | Open-source reasoning matching o1 |

A key framing: **V3 is the infrastructure; R1 is the story that got people to look**. V3 was the real innovation — the [[themes/pretraining_and_scaling|pre-training]] advance that Anthropic's founder identified as what "should have made people take notice a month ago." R1 gained mass attention because it directly challenged o1's unique market position.

---

## DeepSeek-V3: Pre-Training Innovation

### What It Is

V3 is a 671B parameter sparse [[themes/model_architecture|mixture-of-experts]] model, where only 37B parameters are activated per token. Its performance is comparable to GPT-4o. Its full training run cost approximately **$6 million** — orders of magnitude less than the $50M–$100M+ figures circulating for comparable US frontier models.

> "This is a single expenditure that gives you back a model that is seemingly as good as GPT-4o."

Critically, the $6M figure is the cost of *this training run*, not the existence of the company or its compute cluster (which is on the order of billions of dollars).

### Architectural Innovations

V3's advances come not from any single breakthrough but from a combination of carefully integrated optimizations:

**Mixture of Experts architecture.** The model combines *shared experts* (dense, run on every token) with *routed experts* (sparse, only top-K activated per token). This maps naturally to [[themes/adaptive_computation|adaptive computation]] and data parallelism: individual experts can be placed on separate machines rather than replicating the full weight matrix across all nodes.

**Load balancing via learned bias terms.** Expert load imbalance is a critical failure mode in distributed MoE training. V3 addresses this by adding bias terms directly into the neural network architecture that adjust during training, tying routing decisions to physical network topology — a novel coupling of model architecture and distributed systems design.

**FP8 quantization.** Feed-forward matrix multiplications are performed in FP8, accumulated back to FP32, and stored in BF16. This leverages tensor cores on modern GPUs for dramatically higher throughput. The precision loss is extreme — the FP8 E4M3 format cannot represent the number 17, or many other floating-point values — but is tolerable for forward-pass multiplication when accumulated carefully.

**Export-control constraint as innovation driver.** Chinese export-restricted GPUs (H800/H20) have comparable computational throughput to H100s but are bottlenecked in *network bandwidth*. This may have forced DeepSeek to think harder about expert routing and communication efficiency than teams with unconstrained hardware would have.

### What V3 Does Not Change

Algorithmic innovations shift the [[themes/scaling_laws|scaling curve]] — a 2x compute multiplier moves the curve, but does not eliminate the fundamental requirement for more compute to achieve higher intelligence. The core argument for continued compute investment remains intact.

> "There is nothing in the DeepSeek paper which changes the general argument of needing more compute in the long run to gain more intelligence."

---

## DeepSeek-R1: Post-Training Innovation

### What It Is

R1 is a much simpler paper than V3 — one idea demonstrated deeply rather than a collection of small optimizations. It describes how to take a pre-trained model like V3 and teach it to produce legible chain-of-thought reasoning using a variant of **REINFORCE with symbolic verifiers**. The result matches o1-level performance on reasoning benchmarks and exposes the model's reasoning process to users.

### The Method

1. Provide a prompt explaining how the model can use reasoning to produce answers
2. The model generates a chain-of-thought followed by a final answer
3. A symbolic verifier (for math or code) scores the final answer
4. REINFORCE updates the model weights based on reward signal

Notably, complex methods that were speculated to be necessary — process reward models, Monte Carlo Tree Search — were *not* what worked. They were tried but abandoned due to reward hacking. Simple verifiers were critical.

### Cold-Start Problem

Training reasoning from scratch produces incoherent outputs: models mix languages, generate nonsensical intermediate steps, and show poor legibility. The solution was cold-starting from human-curated chain-of-thought examples before applying RL — a meaningful but underemphasized caveat in the paper.

### Strict Domain Dependency

R1's methodology is **strictly limited to domains with explicit symbolic verifiers** — mathematics and code. Extending it to open-ended reasoning, robotics, or scientific discovery requires alternative reward signals that do not yet exist in reliable form.

---

## Limitations and Open Questions

| Limitation | Severity | Trajectory |
|-----------|----------|------------|
| Training code not published; distributed training implementation proprietary | Significant | Stable |
| Training data composition entirely undisclosed | Significant | Stable |
| R1 reasoning restricted to verifiable domains (math, code) | Significant | Improving |
| Cold-start failure without human chain-of-thought examples | Significant | Improving |
| Complex RL methods (process rewards, MCTS) fail due to reward hacking | Significant | Unclear |
| Network bandwidth bottleneck in MoE expert routing | Significant | Unclear |
| FP8 representational gaps (e.g., cannot represent 17 in E4M3) | Minor | Unclear |
| R1 not validated on real SWE benchmarks or production coding | Significant | Improving |
| R1 reasoning quality strictly bounded by pre-training quality of base model | Significant | Unclear |

The open-weights release is significant but incomplete: weights are public, but the training code, distributed infrastructure, and data pipeline that *produced* those weights remain proprietary. Competitive advantages are preserved through process, not model parameters.

There is also a **distillation threat**: access to frontier model outputs (including R1's) enables cheaper reproduction. R1-level reasoning capability could theoretically be obtained by distilling from OpenAI outputs at a fraction of the $6M cost.

---

## Bottlenecks

**RL scaling beyond isolated verifiers.** R1 appears to be a prototype, not a production-ready methodology. Scaling reasoning RL to full autonomous task environments — production software engineering, robotics, scientific discovery — requires verifiable objectives that do not yet exist. Horizon: **1–2 years**.

**MoE distributed training bandwidth.** Network bandwidth constraints in expert routing create a hard ceiling on MoE scaling. Inter-GPU InfiniBand bandwidth is lower than intra-GPU NVLink, limiting expert count and routing complexity beyond 671B parameters. Horizon: **1–2 years**.

**Pre-training data exhaustion.** The source references Ilya Sutskever's framing: "the 2010s were the age of scaling; now we're back in the age of wonder and discovery." The internet text wall is driving a paradigm shift from pre-training scaling to post-training (RL) scaling. Horizon: **3–5 years**.

**General-purpose autonomous improvement.** Autonomous self-improvement via RL is restricted to high-verification domains. Without verifiable objectives for open-ended reasoning and robotics, the path to general autonomy remains blocked. Horizon: **3–5 years**.

---

## Breakthroughs

**Frontier pre-training for ~$6M.** DeepSeek V3 demonstrated that frontier-competitive LLM training is achievable at a cost threshold that fundamentally changes competitive dynamics, open-source viability, and the [[themes/model_commoditization_and_open_source|commoditization]] of base models. Previously, training cost was treated as a moat; V3 shows it is a curve, not a cliff.

**Simple RL teaches legible reasoning.** DeepSeek R1 demonstrated that REINFORCE + symbolic verifiers is sufficient to teach frontier models to produce legible chain-of-thought reasoning matching o1 — without process reward models or MCTS. The complexity of the reasoning infrastructure was dramatically lower than the field assumed.

---

## Market and Strategic Implications

The combined effect on [[themes/ai_market_dynamics|AI market dynamics]] and [[themes/frontier_lab_competition|frontier lab competition]] is substantial:

- **Open weights pressure:** Sam Altman's acknowledgment that OpenAI may be "on the wrong side of history" on model weights suggests DeepSeek's release shifted the strategic calculus on openness.
- **o1's uniqueness eliminated:** R1 ended OpenAI's monopoly on publicly accessible frontier reasoning models.
- **Commoditization accelerating:** High-quality open-weight models are now competitive with closed frontier models on important tasks, pushing value toward fine-tuning, deployment infrastructure, and application layers rather than base model access.
- **Hardware narrative disrupted:** NVIDIA's market loss reflects investor uncertainty about whether frontier performance still requires the largest possible compute clusters — even though DeepSeek itself primarily used NVIDIA hardware.

The Anthropic founder's assessment is noted: V3 was the real innovation; R1 was the trigger. Together, they represent the clearest signal yet that [[themes/model_commoditization_and_open_source|open-source models]] can be genuinely competitive with closed frontier systems.

---

## Related Themes

- [[themes/adaptive_computation|Adaptive Computation]]
- [[themes/ai_market_dynamics|AI Market Dynamics]]
- [[themes/frontier_lab_competition|Frontier Lab Competition]]
- [[themes/model_architecture|Model Architecture]]
- [[themes/model_commoditization_and_open_source|Model Commoditization and Open Source]]
- [[themes/pretraining_and_scaling|Pre-Training and Scaling]]
- [[themes/scaling_laws|Scaling Laws]]

## Key Concepts

- [[entities/distillation|Distillation]]
- [[entities/infiniband|InfiniBand]]
- [[entities/monte-carlo-tree-search-mcts|Monte Carlo Tree Search (MCTS)]]
- [[entities/nvlink|NVLink]]
- [[entities/process-reward-model-prm|Process Reward Model (PRM)]]
- [[entities/scaling-laws|Scaling Laws]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/chain-of-thought-reasoning|chain-of-thought reasoning]]
