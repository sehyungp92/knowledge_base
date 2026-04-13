---
type: entity
title: pass@k metric
entity_type: metric
theme_ids:
- agent_systems
- ai_market_dynamics
- chain_of_thought
- code_and_software_ai
- code_generation
- frontier_lab_competition
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.002419569583804271
staleness: 0.0
status: active
tags: []
---
# pass@k metric

The pass@k metric measures whether at least one of k independently generated attempts at a task succeeds. Introduced as a less stringent alternative to pass^k (which requires *all* k trials to succeed), it has become the dominant lens through which inference-time compute scaling is studied — revealing that correctness coverage across repeated sampling grows far more steeply with sample count than mainstream evaluation practice suggests, and that this growth can close — or invert — capability gaps between model tiers.

**Type:** metric
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/chain_of_thought|Chain of Thought]], [[themes/code_and_software_ai|Code and Software AI]], [[themes/code_generation|Code Generation]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/scaling_laws|Scaling Laws]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]

---

## Overview

pass@k is formally defined as the probability that at least one of k sampled completions solves a given problem. It is typically estimated using the unbiased formula introduced by Chen et al., which corrects for the sampling variance that arises when empirically measuring coverage over a fixed number of generated candidates — an important methodological detail when comparing results across very different values of k.

The metric sits in deliberate contrast to pass^k (pass-to-the-k), which measures consistency across all k trials. Where pass^k penalises unreliable models that can solve problems only occasionally, pass@k rewards any model that *can* solve a problem given enough attempts. This distinction has significant practical implications: pass@k is the right metric when a verifier exists (a test suite, a formal checker, a reward model) to identify the correct sample, while pass^k is appropriate when the model must be trusted to self-consistently produce correct outputs without external verification.

---

## Key Findings

### Coverage scales dramatically — and non-linearly — with sample count

The most striking empirical finding around pass@k concerns how rapidly coverage expands as k grows. On MATH, Large Language Monkeys: Scaling Inference Compute with Repeated Sampling reports that Llama-3-8B-Instruct improves from 82.9% coverage at 100 samples to 98.44% at 10,000. Even Pythia-160M — a model too small to be considered practically competitive — climbs from 0.27% at pass@1 to 57% at pass@10k. The effect is even more dramatic for harder domains: Gemma-2B's coverage on CodeContests increases by over 300x, from 0.02% to 7.1% across the same range.

Critically, these gains dwarf what selection strategies can extract from a fixed pool. On MATH, majority voting and reward-model-based selection improve coverage only from 40.50% to 41.41% over the same 100→10,000 sample range — roughly 1 percentage point against roughly 16 points for raw pass@k. This gap reveals a fundamental asymmetry: the hard ceiling of coverage is determined by how many correct solutions exist in the sample, not by how well you select among them. Generating more samples expands that ceiling; selection only approaches it.

### Repeated sampling inverts capability hierarchies

The practical consequence of steep pass@k scaling is that weaker, cheaper models with high sample counts can outperform stronger models at single-attempt inference. On SWE-bench Lite, DeepSeek-Coder-V2-Instruct's solve rate increases from 15.9% at pass@1 to 56% with 250 samples — exceeding the single-sample state-of-the-art of 43% at the time. Five samples from DeepSeek solve more issues than a single sample from GPT-4o or Claude 3.5 Sonnet, at over 3x lower total cost. This reframes the question of model selection in production: the economically rational strategy is not always the most capable model at one shot, but the most capable-per-dollar model at the coverage-sufficient sample count.

### The metric's relevance extends to agent task reliability

The `pass^k` variant — requiring *all* k trials to succeed — appears prominently in agentic evaluations where reliability under repeated deployment matters more than any single success. On the τ-Bench benchmark, the `think` tool with an optimised prompt achieves pass^1 of 0.570 on the airline domain (54% relative improvement over the 0.370 baseline) but pass^5 of 0.340, versus 0.100 for both the unprompted `think` tool and baseline. This spread between pass@1 and pass^5 is diagnostically important: a model can look strong at single-attempt metrics while being practically unusable in repeated autonomous deployments. The "think" tool paper uses both metrics in tandem precisely to surface this failure mode.

---

## Limitations and Open Questions

**The verifier bottleneck.** pass@k's practical value is entirely conditional on having a reliable verifier. On SWE-bench Lite, 11.3% of problems have flaky test suites that produce inconsistent results on identical candidate solutions — directly corrupting pass@k estimates. For domains without formal verifiers (open-ended reasoning, long-form writing, strategic advice), pass@k is largely inapplicable, and the field lacks consensus on what replaces it.

**Coverage does not equal deployability.** A 98% pass@10k on MATH does not mean any deployed system achieves 98% accuracy — it means a correct solution exists somewhere in 10,000 samples. The marginal cost of identifying that solution, and the latency of generating 10,000 completions, are orthogonal problems. The metric measures theoretical ceiling, not practical throughput.

**Selection quality matters at scale.** As k grows large, the selection problem becomes the binding constraint. If reward models or verifiers cannot reliably identify the correct sample among thousands, the coverage gains are largely theoretical. The gap between pass@k and what is actually achievable with realistic selectors grows as coverage approaches saturation.

**Diminishing returns at the frontier.** The dramatic scaling curves observed in Large Language Monkeys are most pronounced for models and tasks where pass@1 is already low. For frontier models on benchmarks where pass@1 exceeds 70–80%, the marginal coverage gains from repeated sampling compress, and the cost-efficiency argument weakens.

---

## Relationships

pass@k is the primary measurement instrument in the inference-time compute scaling literature, linking directly to themes of [[themes/test_time_compute_scaling|test-time compute scaling]] and [[themes/scaling_laws|scaling laws]] extended beyond training. It intersects with [[themes/reinforcement_learning|reinforcement learning]] through its use in training pipelines where many rollouts are generated and filtered. Its implications for [[themes/ai_market_dynamics|AI market dynamics]] are significant: the finding that cheaper models with more samples can match expensive frontier models at lower cost challenges prevailing assumptions about where value accrues in the inference stack.

Key sources: Large Language Monkeys: Scaling Inference Compute with Repeated Sampling, The "think" tool: Enabling Claude to stop and think.

## Sources
