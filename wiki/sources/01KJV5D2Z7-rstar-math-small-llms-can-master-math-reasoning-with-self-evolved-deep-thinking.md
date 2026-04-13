---
type: source
title: 'rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking'
source_id: 01KJV5D2Z7MBVHR0KNHYB9AWNN
source_type: paper
authors:
- Xinyu Guan
- Li Lyna Zhang
- Yifei Liu
- Ning Shang
- Youran Sun
- Yi Zhu
- Fan Yang
- Mao Yang
published_at: '2025-01-08 00:00:00'
theme_ids:
- mathematical_and_formal_reasoning
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- search_and_tree_reasoning
- synthetic_data_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking

> rStar-Math demonstrates that small language models (1.5B–7B parameters) can match or surpass OpenAI o1 on competition-level mathematics through a self-evolving MCTS-based System 2 reasoning pipeline — without any distillation from superior models. The system co-evolves a policy SLM and a Process Preference Model (PPM) across four rounds, using code-augmented chain-of-thought synthesis and pairwise reward training to progressively generate higher-quality reasoning data from scratch.

**Authors:** Xinyu Guan, Li Lyna Zhang, Yifei Liu, Ning Shang, Youran Sun, Yi Zhu, Fan Yang, Mao Yang
**Published:** 2025-01-08
**Type:** paper

---

## Motivation

Mathematical reasoning exposed a fundamental ceiling in the prevailing distillation-based data synthesis paradigm. OpenMathInstruct-2 achieved only a 3.9% improvement on MATH despite an 8× increase in dataset size — saturating returns that cannot cross the teacher model's capability boundary. Hard problems the teacher cannot solve are excluded entirely, and a correct final answer provides no guarantee that intermediate reasoning steps are valid.

The other half of the dependency is process reward models (PRMs), which supply step-level feedback essential for System 2 reasoning. Accurate step-by-step annotation requires intensive human labeling that is impractical to scale, and automated MCTS-based annotation approaches used Q-values directly as regression targets — inherently noisy labels that produced weak, imprecise reward models. The result was a co-dependency bottleneck: neither the policy model nor the reward model could improve without the other already being strong.

---

## Approach

rStar-Math resolves the co-dependency by bootstrapping both components iteratively across four self-evolution rounds, using only accessible hardware (4×40GB A100s) and no frontier model after Round 1.

### Code-Augmented CoT Synthesis

At each MCTS node, the policy SLM generates a natural-language reasoning step alongside executable Python code (with the NL step embedded as a comment). Only candidates whose Python code executes successfully are retained as valid tree nodes. This automatically filters hallucinated or erroneous intermediate steps before they can propagate — a structural improvement over pure NL approaches where step quality is invisible until the final answer.

### Process Preference Model (PPM)

Rather than regressing Q-values directly (as in prior PRM approaches), the PPM is trained on *preference pairs* derived from MCTS Q-values: positive steps paired against negative steps, optimized with a pairwise ranking loss (Bradley-Terry model). This sidesteps the precision problem — Q-values from extensive rollouts reliably distinguish correct from incorrect steps even when their magnitudes are noisy, making them sufficient for preference pair construction but not for direct score prediction. The PPM provides non-zero initial Q-values in later rounds, guiding MCTS search toward higher-quality steps from the outset.

### Four-Round Self-Evolution

| Round | Policy | Rollouts | Key change |
|-------|--------|----------|------------|
| 1 | 236B DeepSeek-Coder-V2 (bootstrap) | 8 | Terminal-guided Q-values; builds SLM-r1 SFT data |
| 2 | 7B SLM-r1 | 16 | First reliable PPM-r2 trained |
| 3 | 7B SLM-r2 + PPM-r2 | 16 | PPM-augmented MCTS reduces cold-start problem |
| 4 | 7B SLM-r3 + PPM-r3 | 64–128 | Extended to hard Olympiad problems; multiple tree seeds |

By Round 4, 90.25% of 747k math problems are covered with verified reasoning trajectories.

---

## Results

- **MATH-500:** Qwen2.5-Math-7B improves from 58.8% → **90.0%** (64 trajectories), surpassing o1-preview by 4.5% and matching o1-mini. Phi3-mini-3.8B (a general-purpose model) improves from 41.4% → 86.4%.
- **AIME 2024:** Solves an average of **8/15 problems (53.3%)**, placing in the top 20% of brightest high school math students. Exceeds o1-preview (44.6%) by 8.7%, though below o1-mini (56.7%).
- **Reward model scaling:** A 7B policy + 7B PPM outperforms a 72B policy + 72B ORM (Best-of-N) on all benchmarks except GSM8K at matched solution counts.
- **PPM dominance:** Across policy models of different sizes (1.5B, 3.8B, 7B), final reasoning accuracy converges when the same PPM is applied — PPM quality, not policy size, is the primary ceiling on System 2 performance once the policy crosses a capability threshold.
- **Emergent self-reflection:** Without any explicit self-reflection training data or prompting, the MCTS procedure spontaneously produces self-correction behaviour — the policy recognises low-quality reasoning paths and backtracks. This is consistent with prior findings that self-reflection is largely absent in open-source LLMs trained directly on NL CoT.

---

## Landscape Contributions

### Capabilities

| Capability | Maturity |
|-----------|----------|
| SLMs (1.5B–7B) matching o1 on competition math via MCTS + PPM, without distillation | demo |
| Iterative self-evolution of policy and reward model via MCTS rollouts, progressively covering harder problems | research_only |
| PPM via pairwise ranking loss on MCTS Q-value pairs — reliable step-level reward without precise annotation | research_only |
| Code-augmented CoT synthesis with automatic verification via Python execution | research_only |
| Emergent self-reflection as a by-product of MCTS deep thinking | research_only |
| PPM quality as dominant determinant of System 2 ceiling (superseding policy model scale) | demo |

### Limitations

**Significant:**
- **No visual/geometric reasoning.** 8 of 15 unsolved AIME 2024 problems were geometry-based requiring visual understanding — a hard capability boundary with no architectural path provided.
- **Bootstrap dependency on frontier models.** Round 1 requires a 236B parameter model; truly from-scratch self-improvement remains undemonstrated.
- **MCTS inference cost.** 16–64 trajectories per problem on 4×A100s is prohibitive for production API deployment. No latency or cost-per-query analysis is provided.
- **Saturation at 64 trajectories.** On MATH, AIME, and Olympiad Bench, performance plateaus — further compute investment yields no gain on the hardest problems.
- **Generalisability undemonstrated.** All results are math-only. Claims of a "general methodology for improving LLM reasoning" are unsupported by any non-math experiment.
- **Emergent self-reflection not systematically studied.** Only illustrative examples are provided; the phenomenon is not quantified or reliably elicited.
- **Formal theorem proving blocked by datasets.** Extension to Lean/Coq-style proofs is cited as future work but acknowledged as currently infeasible.
- **Noisy training labels.** Of 20 sampled unsolved problems from 747k training data, 19 had incorrectly labeled answers — a significant silent data quality hazard.

**Blocking:**
- **Precise per-step reward scoring remains unsolved.** Q-values can discriminate correct from incorrect but cannot rank fine-grained quality among correct steps. Even expert humans struggle to do this reliably.
- **GPT-4 distillation ceiling.** 8× dataset scaling yields 3.9% MATH improvement — the teacher capability boundary is hard and worsening as benchmarks advance.

### Bottlenecks Addressed / Surfaced

**Partially resolved:**
- *Process reward signal at scale without human labeling* — PPM via pairwise preference training is a meaningful step forward, but fine-grained step ranking remains open (horizon: 1–2 years).

**Remains blocking:**
- *Fully autonomous capability bootstrap* — self-evolution still requires a 236B external teacher for round 1 (horizon: 1–2 years).
- *Production deployment of MCTS reasoning* — 64-trajectory inference is too costly for real-time API use (horizon: 1–2 years).

### Breakthroughs

- **SLMs matching o1 without distillation** (major): Demonstrates that frontier math reasoning capability is achievable at 7B scale via MCTS test-time search, fundamentally challenging the assumption that large model size or teacher distillation is necessary.
- **PPM via preference pairs** (notable): Resolves the noisy Q-value annotation problem by shifting from regression to ranking, making reliable step-level reward models trainable from automated MCTS data alone.
- **Emergent self-reflection from MCTS** (notable): Self-corrective behaviour arises without explicit training signal, suggesting that System 2 search structure may be sufficient to elicit metacognitive behaviours previously thought to require deliberate training.

---

## Open Questions

1. **Can self-evolution bootstrap work without a 236B teacher?** The Round 1 dependency is the weakest link in the "no superior model" claim. What is the minimum external resource required?
2. **Does PPM quality transfer across domains?** The reward model architecture is domain-agnostic, but whether preference pairs from MCTS Q-values are meaningful outside mathematics is entirely unknown.
3. **Is emergent self-reflection MCTS-specific?** Could the same behaviour be obtained via other structured search methods, or is it a property of Q-value backpropagation specifically?
4. **What is the saturation cause at 64 trajectories?** Is it PPM quality, policy diversity, or benchmark difficulty ceiling? The paper does not isolate these.
5. **How does rStar-Math compare to RLVR approaches** (e.g., GRPO, DAPO) that achieve similar benchmark scores with less inference overhead?

---

## Themes

- [[themes/mathematical_and_formal_reasoning|Mathematical & Formal Reasoning]]
- [[themes/post_training_methods|Post-Training Methods]]
- [[themes/reasoning_and_planning|Reasoning & Planning]]
- [[themes/reinforcement_learning|Reinforcement Learning]]
- [[themes/reward_modeling|Reward Modeling]]
- [[themes/search_and_tree_reasoning|Search & Tree Reasoning]]
- [[themes/synthetic_data_generation|Synthetic Data Generation]]

## Key Concepts

- [[entities/best-of-n-sampling|Best-of-N Sampling]]
- [[entities/bradley-terry-model|Bradley-Terry model]]
- [[entities/metamath|MetaMath]]
- [[entities/monte-carlo-tree-search-mcts|Monte Carlo Tree Search (MCTS)]]
- [[entities/numinamath|NuminaMATH]]
- [[entities/outcome-reward-model-orm|Outcome Reward Model (ORM)]]
- [[entities/process-reward-model-prm|Process Reward Model (PRM)]]
- [[entities/qwen25-math-7b|Qwen2.5-Math-7B]]
- [[entities/rejection-sampling|Rejection Sampling]]
- [[entities/system-1-thinking|System 1 thinking]]
- [[entities/system-2-reasoning|System 2 Reasoning]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
