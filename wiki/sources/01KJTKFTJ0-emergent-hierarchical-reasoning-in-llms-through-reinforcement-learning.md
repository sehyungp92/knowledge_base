---
type: source
title: Emergent Hierarchical Reasoning in LLMs through Reinforcement Learning
source_id: 01KJTKFTJ0PZGAG0B2C9DW78EZ
source_type: paper
authors:
- Haozhe Wang
- Qixin Xu
- Che Liu
- Junhong Wu
- Fangzhen Lin
- Wenhu Chen
published_at: '2025-09-03 00:00:00'
theme_ids:
- chain_of_thought
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Emergent Hierarchical Reasoning in LLMs through Reinforcement Learning

**Authors:** Haozhe Wang, Qixin Xu, Che Liu, Junhong Wu, Fangzhen Lin, Wenhu Chen
**Published:** 2025-09-03 00:00:00
**Type:** paper

## Analysis

# Emergent Hierarchical Reasoning in LLMs through Reinforcement Learning
2025-09-03 · paper · Haozhe Wang, Qixin Xu, Che Liu, Junhong Wu, Fangzhen Lin et al. (6 total)
https://arxiv.org/pdf/2509.03646

---

### Motivation & Prior Limitations
RL has proven empirically effective at improving LLM reasoning, but the underlying learning dynamics remain poorly understood, leaving algorithm design without principled guidance. Puzzling phenomena — "aha moments," "length-scaling," and complex token entropy trajectories — have been observed but treated as unrelated artifacts rather than symptoms of a unified underlying process.
- Prevailing RL algorithms like GRPO apply optimization pressure agnostically across all tokens, treating each token as equally important regardless of its functional role in the reasoning process.
  - This agnostic credit assignment dilutes the learning signal: it spreads optimization pressure uniformly over the vast majority of low-level execution tokens (arithmetic steps, variable substitutions, formula applications), which provide weak signal for advancing complex reasoning.
- Token-level entropy has been used as a proxy for exploration quality, but this metric is dominated by the many low-level execution tokens that naturally converge to low entropy as procedural skills consolidate.
  - Decreasing aggregate token entropy was misleading practitioners into believing exploration had declined, when in fact strategic-level exploration was continuing or even expanding.
- Prior work proposing "fork tokens" (high-entropy tokens as proxies for decision points) conflates entropy with strategic function: fewer than 10% of high-entropy tokens actually serve a planning function, meaning entropy alone is an unreliable signal for credit assignment.

---

### Proposed Approach
The paper makes two intertwined contributions: a mechanistic account of how RL shapes LLM reasoning as an emergent two-phase hierarchical process, and HICRA (Hierarchy-Aware Credit Assignment), an algorithm that exploits this structure to concentrate optimization on high-impact planning tokens.

**Mechanistic finding — emergent reasoning hierarchy:** RL training is shown to produce a consistent two-phase dynamic across eight text-only and vision-language models. In Phase 1, the model rapidly consolidates low-level procedural skills (arithmetic, formatting, formula application), evidenced by sharp drops in execution-token perplexity and token entropy. In Phase 2, once procedural reliability is established, the learning frontier shifts to exploring and mastering high-level strategic planning (deduction, branching, backtracing), evidenced by rising semantic diversity of planning tokens and correlated accuracy gains.
- This framing unifies previously unexplained phenomena: "aha moments" are the discovery and internalization of new high-level strategies; "length-scaling" arises because richer strategic deliberation naturally elongates reasoning traces; entropy dynamics reflect procedural convergence masking ongoing strategic exploration.

**Functional proxy — Strategic Grams (SGs):** To operationalize the planning/execution distinction, the paper introduces Strategic Grams — n-grams (n ∈ [3,5]) that function as reusable semantic scaffolding for logical moves (deduction, branching, backtracing). SGs are identified via a three-step data-driven pipeline: semantic clustering of n-grams from successful solutions, filtering by Cluster Document Frequency (top 20% cross-solution frequency), and union of high-frequency clusters. This avoids manual annotation and proprietary models, and a sensitivity analysis removing 30% of SGs confirms the dynamics are robust to the specific SG set.

**Semantic Entropy as exploration compass:** The paper proposes semantic entropy — Shannon entropy over the frequency distribution of strategic grams — as a superior diagnostic for tracking strategic exploration, distinguishing it from token-level entropy (dominated by execution tokens) and Pass@K (saturates quickly). Semantic entropy directly captures diversity in high-level reasoning strategies.

**HICRA algorithm:** Built on the GRPO framework, HICRA modifies the advantage estimate for each token based on its membership in the SG set. For planning tokens, the advantage is amplified by a factor (1 + α · |Â|) where α = 0.2; for execution tokens, the standard GRPO advantage is unchanged. For positive-advantage (successful) trajectories, this amplifies reinforcement of planning tokens; for negative-advantage (failed) trajectories, it dampens their penalty. The resulting policy gradient update anisotropically stretches the target distribution toward the strategic subspace of the action space, fostering a virtuous feedback loop: increased incentive to explore strategies → faster discovery of effective plans → stronger reinforcement of those plans.
- Unlike entropy regularization (which indiscriminately boosts token-level entropy), HICRA focuses exploration specifically on the sparse planning subspace, avoiding non-productive verbosity on execution tokens.

---

### Results & Capabilities
HICRA consistently outperforms GRPO baselines across text-only and multimodal benchmarks and across both base and instruction-tuned model variants.
- On Qwen3-4B-Instruct, HICRA improves over GRPO by +5.4 on AIME24 (73.1 vs 68.5) and +5.1 on AIME25 (65.1 vs 60.0); on Qwen3-4B-Base, gains are +6.1 on AIME24 and +6.0 on Math500 (89.0 vs 83.0).
- On Qwen2.5-7B-Base, HICRA reaches 18.8/14.8 on AIME24/AIME25 vs GRPO's 16.3/11.4, matching ORZ while outperforming SimpleRL and entropy regularization across most benchmarks.
- On multimodal benchmarks, HICRA achieves notable gains over GRPO on MiMO-VL-Instruct: +7.0 on MathVista (80.7 vs 73.7) and +6.1 on MathVision (48.9 vs 42.8), demonstrating that the hierarchical reasoning structure extends to vision-language models.

HICRA achieves higher semantic entropy than GRPO throughout training, and this advantage directly correl

## Key Claims

1. RL training of LLMs exhibits a consistent two-phase learning dynamic: first, consolidation of low-level procedural skills, then exploration and mastery of high-level strategic planning.
2. The 'aha moment' phenomenon observed in RL-trained LLMs is the behavioral signature of a model discovering, mastering, and reinforcing a new high-level strategic reasoning strategy.
3. The 'length-scaling' effect in RL-trained LLMs is caused by increasingly sophisticated high-level strategies (planning, case analysis, self-reflection) that naturally produce longer reasoning traces.
4. GRPO applies optimization pressure agnostically across all tokens, diluting the learning signal and failing to concentrate optimization on high-impact planning tokens.
5. HICRA consistently outperforms GRPO baselines across both text-only LLMs and vision-language models on mathematical reasoning benchmarks.
6. The reduction in strategic (planning and strategy) errors during RL training is more pronounced than the reduction in procedural (calculation, fact-retrieval) errors.
7. Aggregate token-level entropy is dominated by low-level execution tokens and misleads practitioners into thinking exploration has declined, even when strategic exploration is increasing.
8. Semantic entropy of planning tokens is a more reliable diagnostic tool for tracking genuine exploration during RL training than aggregate token-level entropy.
9. Pre-training on human-written solutions encodes hierarchical reasoning structure as an inductive bias that RL subsequently rediscovers and operationalizes.
10. During the initial RL training phase, execution token perplexity and token-level entropy drop sharply, indicating rapid mastery of procedural skills.

## Capabilities

- HICRA (Hierarchy-Aware Credit Assignment) concentrates RL optimization pressure on high-level planning tokens by amplifying their advantage estimates (α=0.2), consistently outperforming GRPO baselines across diverse LLM and VLM architectures on mathematical reasoning benchmarks
- RL training spontaneously induces a consistent two-phase functional hierarchy in LLMs: initial procedural consolidation (sharp drop in execution token entropy and perplexity) followed by strategic exploration (increasing semantic diversity of planning tokens), validated across eight text-only and vi
- Semantic entropy (Shannon entropy over the frequency distribution of strategic n-grams) accurately tracks ongoing strategic exploration during RL training, remaining predictive of final validation accuracy even when aggregate token-level entropy collapses
- An automated three-step pipeline (semantic clustering of n-grams via sentence transformers → cluster document frequency analysis → top-20% filtering) identifies functional strategic planning units (Strategic Grams) from reasoning corpora without manual annotation or proprietary models, robust to 30%

## Limitations

- Standard RL algorithms for LLM reasoning (GRPO and all variants) apply optimization pressure agnostically across all generated tokens, diluting the learning signal on the sparse high-impact planning tokens that are the actual bottleneck for advanced reasoning
- Aggregate token-level entropy collapses during RL training due to dominance of procedural execution tokens, actively misleading researchers into concluding exploration has ceased when strategic exploration is actually increasing
- High-entropy 'fork tokens' are unreliable proxies for strategic planning function: fewer than 10% of high-entropy tokens serve a planning role, while the majority represent mere phrasing variability in procedural execution
- Entropy regularization applied uniformly to all tokens (a standard RL exploration technique) is counterproductive for reasoning: it promotes non-productive verbosity on procedural tokens while failing to improve accuracy, producing the lowest validation accuracy of all compared methods
- Outcome-based RL (RLVR/GRPO) cannot assign credit to correct strategic choices within failed reasoning trajectories — a solution with correct high-level strategy but a single arithmetic error yields zero learning signal on the strategy, starving the most important component of the learning signal
- HICRA and the hierarchical reasoning framework are validated exclusively on mathematical reasoning benchmarks (AIME, Math500, AMC, Olympiad, MathVista); applicability to code generation, agentic tool-use, and open-ended text domains remains entirely untested
- The two-phase procedural consolidation → strategic exploration dynamic may be absent or compressed in models with strong instruction-tuning, creating variable HICRA benefit depending on the starting model checkpoint
- HICRA produces mixed or negative results on Llama-3.1-8B (e.g., -0.6 on AIME24, -1.4 on Minerva vs GRPO), suggesting that the hierarchical credit assignment benefit is architecture- or training-regime-dependent rather than universal
- Pass@K on training data saturates rapidly during RL training, rendering it unusable for distinguishing ongoing exploration quality between methods after early training stages
- Experiments are limited to ~4–8B parameter models; whether the emergent two-phase hierarchy and HICRA's benefits generalise to frontier-scale models (70B+) remains unvalidated

## Bottlenecks

- Standard RL credit assignment for LLM reasoning is agnostic to token functional role, concentrating optimization pressure on the majority procedural tokens and starving the sparse high-impact strategic planning tokens that drive advanced reasoning
- Absence of process-level reward signals for intermediate strategic decisions prevents RL from learning from partially correct reasoning trajectories where the strategy was sound but execution failed, wasting valuable positive training signal

## Breakthroughs

- Discovery that RL training induces a consistent emergent two-phase reasoning hierarchy in LLMs — first consolidating procedural reliability, then exploring high-level strategic planning — providing a unified mechanistic explanation for 'aha moments', length-scaling, and entropy dynamics that were pr

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/entropy-regularization|Entropy Regularization]]
- [[entities/grpo|GRPO]]
- [[entities/passk|pass@k]]
