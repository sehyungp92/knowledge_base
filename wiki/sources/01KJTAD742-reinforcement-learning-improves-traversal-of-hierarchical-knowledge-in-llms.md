---
type: source
title: Reinforcement Learning Improves Traversal of Hierarchical Knowledge in LLMs
source_id: 01KJTAD742YENND9YCN9YEQMDK
source_type: paper
authors:
- Renfei Zhang
- Manasa Kaniselvan
- Niloofar Mireshghallah
published_at: '2025-11-08 00:00:00'
theme_ids:
- interpretability
- knowledge_and_memory
- mechanistic_interpretability
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Reinforcement Learning Improves Traversal of Hierarchical Knowledge in LLMs

**Authors:** Renfei Zhang, Manasa Kaniselvan, Niloofar Mireshghallah
**Published:** 2025-11-08 00:00:00
**Type:** paper

## Analysis

# Reinforcement Learning Improves Traversal of Hierarchical Knowledge in LLMs
2025-11-08 · paper · Renfei Zhang, Manasa Kaniselvan, Niloofar Mireshghallah
https://arxiv.org/pdf/2511.05933

---

### Motivation & Prior Limitations
The prevailing narrative holds that RL and RLHF post-training methods impose an "alignment tax" — sacrificing factual memorization to optimize for other objectives — and prior work documents systematic degradation on knowledge-intensive benchmarks as alignment pressure increases.
- Existing studies of factual degradation focus exclusively on unstructured, direct-recall tasks, leaving open whether the same pattern holds for retrieval that requires navigating hierarchical, taxonomic structures encoded in model parameters.
  - Lin et al. (2024) showed RLHF degrades factual benchmarks as reward strength increases; Ghosh et al. (2024) found instruction tuning adjusts style rather than knowledge; Phan et al. (2025) found reasoning-focused RL leads to increased hallucinations despite improved benchmark scores.
- No prior work distinguished between two fundamentally different retrieval regimes: flat direct recall versus hierarchical traversal, meaning the assumed universality of the alignment tax was untested.

---

### Proposed Approach
The paper challenges the alignment-tax narrative through three complementary experiments designed to disentangle knowledge acquisition from knowledge navigation, arguing that RL improves procedural traversal skills over existing parametric knowledge rather than adding new factual content.
- **Structured prompting (RQ1):** The authors craft prompts that explicitly instruct instruction-tuned models to perform hierarchical traversal — first recalling the structural breakdown of the relevant code or concept, then systematically eliminating options — to test whether the knowledge exists in SFT models but simply needs navigation scaffolding to surface.
  - This is motivated by evidence that prompt optimization can match RL gains (Agrawal et al., 2025; Khattab et al., 2023), providing a parameter-free test of the knowledge-vs-navigation hypothesis.
- **Complexity-stratified path evaluation (RQ2):** The authors extend the IPC patent classification dataset into Memory-Light (<3 ancestor traversals) and Memory-Heavy (≥5 ancestor traversals) splits and introduce a **Path Matching Score** — the harmonic mean of an F1 score over ancestor node identification and a Common Subsequence Score measuring structural path integrity — to measure traversal quality beyond final-answer accuracy.
- **Layer-wise representational analysis (RQ3):** Contrastive query-answer probes are constructed from MedConceptsQA across five medical vocabularies (500 total probes); hidden states at the final token position are extracted at each layer for interrogative queries (e.g., "What is code 57.95?") and declarative factual statements (e.g., "Code 57.95 refers to urinary catheter replacement"), and cosine similarity is computed inter-model (base vs. specialized) and intra-model (query vs. answer) across the Qwen2.5-32B family (base, instruct, distilled, reasoning).

---

### Results & Capabilities
RL-enhanced reasoning models (DeepSeek-R1, QwQ-32B) outperform their instruction-tuned counterparts by up to 24 percentage points on MedConceptsQA, directly contradicting the claim that RL uniformly degrades structured knowledge recall.
- DeepSeek-R1 achieves 0.778 majority-vote accuracy on MedConceptsQA (QA prompt) versus DeepSeek-V3's 0.541, a 23.7pp gap; structured prompting reduces this to 7.5pp (a 68% gap reduction), demonstrating that the knowledge exists in SFT models but requires navigational scaffolding to access.

Structured prompting fully closes or reverses the gap for some model families, but cannot replicate RL's advantage on complex deep-retrieval tasks.
- On Memory-Heavy IPC tasks (≥5 traversals), DeepSeek-R1 and DeepSeek-V3 achieve identical final-answer accuracy (67.7%), but R1's Path Matching Score is 0.597 versus V3's 0.503 — a 9pp gap that widens from the 5pp gap on Memory-Light tasks — showing R1 correctly navigates intermediate hierarchical steps even when V3 reaches the right answer by other means.
- On MedConceptsQA, structured prompting caused V3 responses to migrate from "All Incorrect" and "Majority Incorrect" categories toward "All Correct," while R1's distribution remained static, indicating R1 already operates near ceiling and that V3's gains come from improved reasoning consistency rather than new knowledge.

Layer-wise activation analysis reveals RL transforms query processing while leaving factual representations intact.
- Declarative answer representations maintain cosine similarity of 0.85–0.92 between base and RL models across most layers; interrogative query representations diverge to 0.65–0.73 in middle layers — a striking asymmetry confirming that RL modifies how models process questions, not where or how factual knowledge is stored.
- Distilled models (e.g., DeepSeek-R1-Distill-Qwen-32B) show the greatest overall representational divergence from the base model yet achieve only intermediate performance, with structured prompting yielding minimal gains; this suggests distillation transfers surface behavioral patterns without instilling robust hierarchical navigation mechanisms.

---

### Implications
RL post-training should be understood as installing improved **cognitive scaffolding** — procedural access patterns over parametric knowledge — rather than as a knowledge injection or knowledge destruction mechanism, which reframes how alignment tax findings should be interpreted across different retrieval regimes.
- This suggests a more efficient training paradigm: pretraining handles knowledge acquisition; post-training (RL) optimizes organizational and navigational access over that knowledge, potentially reducing the need for expensive re-pretraining when new navigation behaviors are desired.

The finding that structured prompting recovers most of

## Key Claims

1. RL-enhanced models consistently outperform base and SFT counterparts on pure knowledge recall tasks that require traversal of hierarchical, structured knowledge such as medical codes.
2. The performance gains of RL-enhanced models on hierarchical knowledge tasks stem from improved procedural navigation skills, not from newly acquired factual data.
3. Structured prompting that explicitly guides SFT models through hierarchical traversal reduces the performance gap between DeepSeek-V3 and DeepSeek-R1 on MedConceptsQA from 24 percentage points to 7 pe
4. RL-enhanced models retain superior ability to recall correct procedural paths on deep-retrieval tasks even when structured prompting improves final-answer accuracy of SFT models.
5. Factual (declarative) representations maintain high cosine similarity of 0.85–0.92 between SFT and RL models across most layers, while query (interrogative) representations diverge substantially, drop
6. RL primarily transforms how models process queries and traverse knowledge hierarchies, leaving factual knowledge representations substantially intact.
7. The conventional wisdom that RL sacrifices memorization for reasoning is incomplete; RL-enhanced models outperform base models by 24 percentage points on hierarchical knowledge retrieval tasks.
8. Existing work on alignment tax has primarily studied direct factual recall over unstructured knowledge, leaving a gap regarding hierarchical parametric knowledge retrieval.
9. As retrieval depth increases from fewer than 3 hops to more than 5 hops, the performance gap between reasoning and instruct models on path recall accuracy widens from 5 percentage points to 9 percenta
10. Distilled models capture only surface-level improvements without acquiring robust hierarchical navigation capabilities, achieving intermediate performance on complex retrieval tasks.

## Capabilities

- RL-enhanced reasoning models systematically traverse hierarchical knowledge taxonomies (medical codes, patent classifications) via multi-step procedural navigation, outperforming SFT counterparts by up to 24 percentage points on structured recall benchmarks — gains attributed to navigation mechanism
- Hand-crafted structured prompting that explicitly instructs models to recall hierarchical structural breakdowns and perform stepwise elimination recovers up to 68% of the RL-SFT performance gap on hierarchical knowledge retrieval, without any parameter updates
- Layer-wise cosine similarity analysis of final-token hidden states can mechanistically distinguish whether post-training modifies query processing versus factual knowledge encoding — detecting RL's effect on model internals at the representational level

## Limitations

- Distilled models (e.g., DeepSeek-R1 distillations into Qwen2.5-32B, Llama3.3-70B) fail to acquire robust hierarchical navigation capabilities — they capture only surface-level output patterns and remain far below teacher performance even with structured prompting (e.g., +0.182 gap for Llama3.3-70B o
- A 7pp residual performance gap persists between RL-enhanced models and optimally-prompted SFT models even after hand-crafted hierarchical structured prompting, indicating RL training produces navigation capabilities that prompting alone cannot fully replicate
- Structured prompting that closes the RL-SFT gap requires hand-crafted, domain-specific hierarchical prompt templates — generic CoT and standard QA prompting provide marginal benefit, and no general method exists for automatically deriving effective hierarchical prompts
- On memory-heavy deep-retrieval tasks (5+ hierarchical hops), RL-enhanced models achieve higher path quality scores than SFT models but converge to the same final-answer accuracy (67.7% for both R1 and V3), revealing a ceiling where better navigation does not translate to better outcomes
- The alignment tax — RL/SFT degrading direct factual recall on flat unstructured knowledge tasks — remains real and unaddressed by this work; the hierarchical navigation gains do not generalize to direct recall improvements
- RL training optimized for narrow verifiable rewards causes regression in general capabilities and increased hallucinations — the same training that improves structured knowledge traversal simultaneously degrades broader model reliability
- The hierarchical navigation findings are demonstrated only on two structured knowledge domains (ICD medical codes, IPC patent codes) with three model families; generalization to mathematical proofs, code debugging, multi-hop QA, or flat hierarchies is entirely unverified
- Even optimally-prompted RL models (DeepSeek-R1) achieve only 77-83% on medical code QA — structured hierarchical knowledge retrieval from parameters remains far from reliable for high-stakes clinical deployment

## Bottlenecks

- Distillation from RL-trained reasoning models fails to transfer hierarchical navigation mechanisms — current distillation recipes optimize for output matching and cannot reproduce the internal query-processing transformations that RL instills, blocking efficient capability scaling via knowledge dist
- No RL training objective explicitly targets hierarchical knowledge navigation — current RL methods (GRPO, PPO, RLHF) produce navigation as an emergent side effect rather than a direct optimization target, making it impossible to systematically design or control the navigation capability

## Breakthroughs

- Layer-wise representational analysis establishes that RL primarily transforms query processing mechanisms (cosine similarity drops to 0.65-0.73 in middle layers) while leaving factual knowledge representations largely intact (similarity 0.85-0.92), directly refuting the blanket 'alignment tax' narra

## Themes

- [[themes/interpretability|interpretability]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/mechanistic_interpretability|mechanistic_interpretability]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]

## Key Concepts

- [[entities/quiet-star|Quiet-STaR]]
- [[entities/qwq-32b|QwQ-32B]]
