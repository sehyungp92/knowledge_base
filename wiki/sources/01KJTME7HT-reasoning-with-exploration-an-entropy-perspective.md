---
type: source
title: 'Reasoning with Exploration: An Entropy Perspective'
source_id: 01KJTME7HTKC015QA0VJG19C8H
source_type: paper
authors:
- Daixuan Cheng
- Shaohan Huang
- Xuekai Zhu
- Bo Dai
- Wayne Xin Zhao
- Zhenliang Zhang
- Furu Wei
published_at: '2025-06-17 00:00:00'
theme_ids:
- chain_of_thought
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 16
tags: []
---
# Reasoning with Exploration: An Entropy Perspective

**Authors:** Daixuan Cheng, Shaohan Huang, Xuekai Zhu, Bo Dai, Wayne Xin Zhao, Zhenliang Zhang, Furu Wei
**Published:** 2025-06-17 00:00:00
**Type:** paper

## Analysis

# Reasoning with Exploration: An Entropy Perspective
2025-06-17 00:00:00 · paper · Daixuan Cheng, Shaohan Huang, Xuekai Zhu, Bo Dai, Wayne Xin Zhao et al. (7 total)
https://arxiv.org/pdf/2506.14758v3

---

### Motivation & Prior Limitations
Current RLVR methods for LLM reasoning over-optimize for exploitation, causing models to converge on narrow, over-optimized behaviors that plateau or regress on complex tasks.
- Standard accuracy-driven RL objectives (GRPO, PPO) reinforce correct outputs but provide no incentive to explore alternative reasoning strategies, leading to a systematic loss of exploratory capacity.
  - On benchmarks like AIME 2024/2025, RL-finetuned models consistently outperform base models on Pass@1 but are surpassed by base models on Pass@K at large K — demonstrating that conventional RL inadvertently constrains the model's solution diversity ceiling.
- Prior attempts to address exploration via token-frequency rewards for reasoning-like tokens (Chen et al., 2025) induce reward hacking — the model learns to repeat such tokens without performing genuine reasoning.
- Traditional maximum-entropy RL methods encourage higher-entropy policies uniformly by adding an entropy regularizer to the training objective, which destabilizes training (empirically showing a sudden entropy spike after step 1500) and produces inferior reasoning performance.

---

### Proposed Approach
The paper proposes entropy-based advantage shaping: augmenting the per-token advantage in standard RLVR algorithms (PPO, GRPO) with a clipped, gradient-detached entropy term, implemented as a single line of code.
- The approach is motivated by an empirical finding that high-entropy tokens correspond to three types of exploratory reasoning actions: (1) pivotal tokens (logical connectors like "first," "because," "however"), (2) reflective actions (self-verification, error correction), and (3) rare behaviors semantically distant from the base model's output distribution.
- The entropy term is defined as `ψ(Hₜ) = min(α · Hᵗᵈᵉᵗᵃᶜʰ, |Aₜ|/κ)` and added to the original advantage before computing the policy loss; clipping with threshold `|Aₜ|/κ` ensures the term never dominates or reverses the sign of the original advantage, preserving the original optimization direction.
- Crucially, the entropy term is detached from the computational graph (`∇θHᵗᵈᵉᵗᵃᶜʰ = 0`), making this fundamentally distinct from entropy regularization — it acts as a fixed scalar offset to advantage magnitude rather than introducing an additional gradient component that would alter the policy gradient flow.
- The method is self-regulating: when high entropy causes a stronger update on a token, the token's probability increases, sharpening the distribution, which lowers entropy and thus reduces the entropy-based advantage in subsequent steps — preventing over-encouragement without requiring explicit scheduling.

---

### Results & Capabilities
The method consistently improves Pass@1 accuracy across AIME 2025/2024, AMC 2023, and MATH500 when applied to both GRPO and PPO on Qwen2.5-Base-7B and Qwen2.5-Math-Base-7B.
- On AIME 2025 Pass@256, PPO with entropy advantage reaches 56.7% vs. 43.3% for PPO alone (+13.4 pp); GRPO with entropy advantage reaches 53.3% vs. 50.0% for GRPO alone (+3.3 pp) and notably exceeds the base model's Pass@256 ceiling of 50.0%, demonstrating the method can push beyond base model limits on held-out benchmarks.
- Pass@1 gains are consistent but smaller: +3.8 pp on AIME 2025 with PPO, +1.3 pp on AIME 2025 with GRPO on Qwen2.5-Math, confirming the method's primary value is in expanding reasoning diversity rather than merely lifting greedy accuracy.
- The method increases response length and pivotal token/reflective action counts throughout training without increasing n-gram repetition rate, demonstrating that longer outputs reflect genuine reasoning depth rather than degenerate verbosity.
- Entropy-based advantage shaping outperforms entropy regularization on both Pass@1 and Pass@K metrics (e.g., AIME 2025 Pass@256: 53.3% vs. 50.0%; AIME 2024 Pass@256: 56.7% vs. 50.0%) while maintaining stable training dynamics.

---

### Implications
The entropy-as-exploration-signal finding provides a mechanistic, token-level explanation for why certain reasoning behaviors (reflection, logical pivots, novel solutions) emerge and how RL training can explicitly target them, connecting classical RL exploration theory to LLM inference dynamics.
- The Pass@K plateau observed in conventionally RL-trained models — where base models eventually surpass fine-tuned ones at large K — suggests that standard RLVR systematically narrows the model's hypothesis space, which has important implications for how test-time compute scaling interacts with training-time RL: training choices directly determine the ceiling that test-time sampling can reach.
- The one-line implementation compatible with any RLVR pipeline (veRL, PPO, GRPO) lowers the barrier to adoption significantly, suggesting this could become a standard component of RL training recipes for reasoning models.
- The finding that Llama-series LLMs abandoned intermediate reasoning chains within a few RL training iterations (absent pre-training on reasoning traces) implies that base model architecture and pre-training data are a prerequisite constraint for RL-driven reasoning improvements — exploration methods alone cannot substitute for foundational reasoning capability.

---

### Remaining Limitations & Next Steps
The method is validated only on mathematical reasoning benchmarks (AIME, AMC, MATH500); generalization to code reasoning, scientific reasoning, or open-ended tasks is not demonstrated in the main evaluation.
- The paper evaluates on two Qwen2.5 model families (7B scale) and explicitly notes that Llama-series models were dropped because they collapsed during RL training; it is unclear whether the entropy-exploration correlation holds at different model scales or for non-math-specialized base models.

## Key Claims

1. Rare or under-explored behaviors that emerge during RL training coincide with elevated token entropy, revealing a strong correlation between semantic novelty and predictive uncertainty.
2. Entropy-based advantage shaping can be implemented as a single line of code added to existing RLVR training pipelines.
3. The entropy-based advantage term is clipped to prevent it from dominating or reversing the sign of the original advantage, preserving the original optimization direction.
4. The entropy term in the advantage shaping method is gradient-detached, meaning it adjusts the magnitude of updates without altering the gradient flow of the original RL algorithm.
5. The entropy-based advantage is self-regulating: as model confidence increases, entropy decreases, naturally reducing the entropy-based shaping term and preventing over-encouragement of exploration.
6. Rewarding reasoning-like token frequency leads to reward hacking, whereas entropy-based advantage shaping avoids this due to the intrinsic tension between entropy and confidence.
7. Entropy-based advantage shaping is fundamentally distinct from and orthogonal to entropy regularization because it does not introduce an additional entropy gradient component.
8. Llama LLMs abandon intermediate reasoning chains within just a few RL training iterations, suggesting they require pre-training on reasoning traces prior to RL training.
9. Entropy-based advantage shaping consistently outperforms RL baselines on both Pass@1 and Pass@K across AIME 2025/2024, AMC 2023, and MATH500 benchmarks with both GRPO and PPO algorithms.
10. On AIME 2025, entropy-based advantage with PPO achieves Pass@256 of 56.7% compared to 43.3% for PPO baseline and 50.0% for the base model, breaking through the base model's performance ceiling.

## Capabilities

- Entropy-based advantage shaping (one-line modification to PPO/GRPO) improves exploratory reasoning in LLMs, achieving superior Pass@K at large K values and consistent Pass@1 gains across math reasoning benchmarks
- Token-level entropy reliably identifies three classes of exploratory reasoning actions — pivotal logical connectors, reflective self-verification sentences, and rare emergent solution strategies — all exhibiting statistically significantly higher entropy than ordinary tokens
- RL-trained LLMs can generate substantially longer, more exploratory reasoning chains (3023 vs 725 tokens in case study) without proportional increase in repetition rate, enabling systematic case analysis and adaptive backtracking

## Limitations

- Conventional accuracy-driven RLVR fine-tuning inadvertently caps exploratory capacity: base models can outperform their RL-finetuned counterparts in Pass@K when K is sufficiently large, meaning RL training trades output distribution diversity for average accuracy
- Purely accuracy-driven RLVR training leads to performance plateaus and regression as LLMs converge on narrow over-optimised behaviours and lose incentive to explore alternative reasoning strategies
- Models without pre-existing reasoning behaviours (e.g. Llama-series LLMs) cannot benefit from RLVR training and abandon intermediate reasoning chains within a few training iterations, requiring prior exposure to reasoning traces
- Without the 'clip-higher' asymmetric clipping technique, standard RL training causes catastrophic entropy collapse in LLMs (entropy ~0.03), eliminating exploration capacity and rendering entropy-based methods ineffective
- Entropy regularisation (adding entropy loss to the training objective) causes unstable optimisation with sudden entropy spikes after step ~1500, and is outperformed by advantage-based shaping on both stability and final accuracy
- Rewarding frequency of reasoning-like tokens in RL training causes reward hacking — models repetitively generate such tokens to maximise reward without performing genuine reasoning
- Entropy-based advantage shaping can decrease Pass@K for already domain-adapted models on some benchmarks (Qwen2.5-Math + GRPO on AIME24 Pass@256 drops from 83.3 to 80.0), suggesting the method may trade off diversity for accuracy in models with strong domain priors
- All evaluations are conducted on mathematical reasoning benchmarks (AIME, AMC, MATH500) using 7B parameter models only; generalisability to other domains (general language, code at scale, science) and larger model sizes is not demonstrated
- The entropy scaling coefficient α must be tuned per algorithm (0.4 for GRPO, 0.1 for PPO), implying sensitivity to RL algorithm choice and non-trivial generalisation overhead when adopting the technique in new settings
- Response length is capped at 8K tokens during evaluation, imposing a hard ceiling on reasoning depth and potentially masking performance differences on problems requiring extended solution chains beyond this budget

## Bottlenecks

- Standard accuracy-driven RLVR training systematically collapses output distribution diversity, creating a fundamental tension between Pass@1 optimisation and Pass@K exploratory capacity — fine-tuning improves average accuracy while eroding ability to discover rare but correct solutions at large samp
- Entropy collapse in standard RL training (dropping to ~0.03 without clip-higher mitigation) creates an implicit ceiling on LLM exploration during fine-tuning, requiring non-standard workarounds not present in vanilla RLVR implementations

## Breakthroughs

- Entropy-based advantage shaping: a one-line modification to PPO/GRPO that amplifies high-entropy token updates during training, self-regulates as confidence increases via entropy-confidence tension, and preserves original policy gradient flow — enabling trained models to exceed base model explorator
- First systematic empirical analysis demonstrating that token-level entropy in LLMs correlates specifically with three distinct categories of exploratory reasoning behaviour — pivotal logical connectors, reflective self-verification actions, and rare emergent solution strategies — establishing entrop

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]

## Key Concepts

- [[entities/entropy-collapse|Entropy Collapse]]
- [[entities/entropy-regularization|Entropy Regularization]]
- [[entities/grpo|GRPO]]
- [[entities/math500|MATH500]]
- [[entities/ppo|PPO]]
- [[entities/rlvr|RLVR]]
- [[entities/passk|pass@k]]
- [[entities/verl|verl]]
