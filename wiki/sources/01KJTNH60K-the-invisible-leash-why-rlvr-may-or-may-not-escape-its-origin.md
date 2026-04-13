---
type: source
title: 'The Invisible Leash: Why RLVR May or May Not Escape Its Origin'
source_id: 01KJTNH60KQN3MFCZCQVRWCQX3
source_type: paper
authors:
- Fang Wu
- Weihao Xuan
- Ximing Lu
- Mingjie Liu
- Yi Dong
- Zaid Harchaoui
- Yejin Choi
published_at: '2025-07-20 00:00:00'
theme_ids:
- mathematical_and_formal_reasoning
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
# The Invisible Leash: Why RLVR May or May Not Escape Its Origin

**Authors:** Fang Wu, Weihao Xuan, Ximing Lu, Mingjie Liu, Yi Dong, Zaid Harchaoui, Yejin Choi
**Published:** 2025-07-20 00:00:00
**Type:** paper

## Analysis

# The Invisible Leash: Why RLVR May or May Not Escape Its Origin
2025-07-20 00:00:00 · paper · Fang Wu, Weihao Xuan, Ximing Lu, Mingjie Liu, Yi Dong et al. (7 total)
https://arxiv.org/pdf/2507.14843

---

### Motivation & Prior Limitations
RLVR (Reinforcement Learning with Verifiable Rewards) has powered breakthrough reasoning models like DeepSeek-R1 and OpenAI-o1, but a fundamental question remained unresolved: whether RLVR genuinely expands a model's reasoning boundary or merely amplifies high-reward outputs the base model already knew, trading diversity for precision.
- Prior empirical studies examined RLVR only through before/after snapshots, leaving unexplored how RLVR reshapes the model's effective reasoning support throughout training.
  - A puzzling pattern had been noted: RLVR-trained models consistently outperform base models on single attempts (pass@1), but base models often perform better with multiple attempts (pass@k at large k), suggesting coverage loss.
  - Shao et al. (2025) found RLVR can benefit from noisy or spurious reward signals, raising doubt about whether gains reflect deeper reasoning improvements or sharper exploitation of existing heuristics.
- The debate was polarised: some studies interpreted pass@k patterns as evidence that RLVR performs conservative optimisation within existing base model capabilities, while others argued RLVR can substantially expand reasoning in domains where the base model is not already well-trained.
  - No systematic, multi-model, multi-domain empirical framework existed to characterise what RLVR does and does not change about solution accessibility.

---

### Proposed Approach
The paper introduces a formal framework of *empirical support* — the set of correct solutions a model can realistically discover under finite sampling — and uses it to diagnose exactly how RLVR reshapes solution accessibility, distinguishing four categories: Preservation, Expansion, Shrinkage, and Out of Support.
- The framework relaxes the theoretically strict definition of support by applying a threshold ε derived from sampling confidence bounds, capturing the practical distinction between completions with non-negligible probability and those so deep in the tail they are statistically invisible under finite on-policy rollouts.
  - This directly addresses the "softmax everywhere is positive" problem: all completions technically have non-zero probability, but many are unreachable in practice with finite rollouts.
- Four complementary metrics are derived: Support Retention Rate (SRR), Net Discovery Rate (NDR), Support Dynamic Score (SDS, the harmonic mean of SRR and NDR), and Net Support Change Rate (NSCR, capturing net expansion or shrinkage).
  - These metrics allow discrimination between four RLVR behaviours: support-constrained optimisation (high SRR, low NDR), genuine capability expansion (high SRR, high NDR), inefficient redistribution (low SRR, low NDR), and aggressive exploration (low SRR, high NDR).
- Experiments span seven RLVR models from 1.5B to 14B parameters (ProRL, Nemotron, Skywork, AceReason, Phi4-Reason, and a visual LLM Kangheng-OVR-7B), evaluated across math benchmarks (MATH500, Minerva, OlympiadBench, AIME 2024/2025, AMC 2023) and non-math benchmarks (SimpleQA, LiveBench, SciBench, Reasoning Gym), with sampling budgets up to k=16,384.

---

### Results & Capabilities
RLVR predominantly acts as a support-constrained optimisation mechanism, not a genuine capability expander: across all 1.5B–14B models, solution preservation dominates, shrinkage consistently exceeds expansion, and genuine discovery is rare.
- All evaluated models achieve very high support retention (overall SRR ≈ 0.93–0.99), while genuine discovery is negligible (NDR ≤ 0.04 across all models and domains).
  - ProRL-1.5B-v2 loses 175 correct completions while gaining only 48 (shrinkage-to-expansion ratio ≈ 3.6:1); Nemotron-7B and Skywork-OR1-7B show similar ratios of 2:1 to 3:1.
  - Math benchmarks are especially imbalanced (SDS ≈ 0.00–0.01; NDR ≈ 0.00–0.01), while non-math domains are only marginally better (NDR ≤ 0.04).
- NSCR values are consistently slightly negative (−0.01 to −0.06), confirming RLVR systematically narrows the accessible solution set; this explains the pass@k crossover — e.g., base model pass@8192 on AIME2024 is 93.3% vs. ProRL-1.5B's 83.3%.
  - Tasks like leg_counting, family_relationships, and power_function (Reasoning Gym) illustrate cases where RLVR boosts pass@1 substantially but the pass@k curve flatlines well below the base model ceiling.
- An entropy divergence effect is identified: RLVR sometimes *increases* token-level entropy while simultaneously *decreasing* answer-level entropy — seemingly more uncertain token-by-token generation paths ultimately converge onto a smaller set of distinct final answers.
  - This indicates local uncertainty and global diversity can diverge, and that token-level entropy is a misleading proxy for solution diversity.
- Perplexity analysis against external reasoning traces (DeepSeek-R1 and Claude Sonnet 4) shows ProRL consistently assigns higher perplexity to external reasoning styles after RLVR training; on AIME2024, perplexity on Claude Sonnet 4 traces increases from 8.76 (base) to 14.91 (ProRL), indicating structural narrowing of compatible reasoning trajectories, not just format differences.
- Rare genuine expansion cases exist (e.g., graph_color_vertex20, arc_1d, boxnet in Reasoning Gym), but these are isolated exceptions; perplexity analysis on expansion cases suggests new successful trajectories originate from the base model's low-density tails rather than genuinely novel reasoning structures.
- SFT vs. RLVR comparison (fixing Qwen2.5-Math-7B and DeepMath-103K, varying only the training objective to SFT vs. DAPO) provides additional evidence that the precision-diversity trade-off is a property of the optimisation paradigm, not the data.

---

### Implications
The "invisible leash" finding challenges a central assu

## Key Claims

1. RLVR operates as a support-constrained optimization mechanism that restricts the discovery of entirely original solutions, remaining constrained by the base model's initial distribution.
2. RLVR creates an entropy-reward trade-off: while it reliably enhances precision, it may progressively narrow exploration and potentially overlook correct yet underrepresented solutions.
3. RLVR can benefit from noisy or spurious reward signals, calling into question whether observed gains reflect deeper reasoning improvements or merely sharper exploitation of existing heuristics.
4. The precision-diversity trade-off in RLVR is fundamental and not domain-specific, appearing across mathematics, logical reasoning, factual QA, and code generation.
5. RLVR achieves very high support retention rates (SRR ≈ 0.93–0.99) across all evaluated models and domains while genuine discovery rates remain rare (NDR ≤ 0.04).
6. Support shrinkage consistently exceeds expansion across all models and domains: ProRL-1.5B-v2 loses 175 completions while gaining only 48, a ratio of approximately 3.6:1.
7. RLVR training increases perplexity on diverse external reasoning traces: on AIME2024, perplexity on Claude Sonnet 4 traces increases from 8.76 (base model) to 14.91 (ProRL), indicating reduced ability
8. In shrinkage cases, the RLVR-trained ProRL model shows higher perplexity even when the base model succeeds, confirming that RLVR collapses probability mass away from viable solution pathways.
9. ProRL's rare expansion cases originate from the base model's low-density tails rather than genuinely novel reasoning structures.
10. On AIME2024, the base model achieves pass@8192 = 93.3% while ProRL-1.5B only achieves 83.3%, demonstrating that base models can dominate at high sampling budgets due to broader solution coverage.

## Capabilities

- RLVR training consistently improves single-attempt accuracy (pass@1) across diverse domains and model scales from 1.5B to 14B parameters, confirmed across math, logical reasoning, factual QA, and code generation
- Empirical support dynamics framework (SRR, NDR, SDS, NSCR metrics) enables systematic measurement of how RLVR reshapes a model's solution accessibility space relative to its base model, distinguishing preservation, expansion, shrinkage, and out-of-support regimes
- RLVR with entropy management techniques (GRPO + decoupled clipping + dynamic sampling + KL regularization + periodic reference resets) sustains long-horizon RL training without entropy collapse, enabling extended training runs on 1.5B models

## Limitations

- RLVR predominantly preserves rather than expands the base model's solution space — support shrinkage consistently outweighs expansion across all tested models, with ratios of 2:1 to 3.6:1 (e.g., ProRL-1.5B-v2 loses 175 completions while gaining only 48); even large 14B models exhibit net shrinkage
- RLVR-trained models perform worse than their untuned base models at high sampling budgets (large k) — the base model's broader solution coverage dominates when multiple attempts are allowed, reversing the apparent RLVR advantage
- RLVR's precision-diversity trade-off is fundamental and cross-domain — NDR remains near zero across mathematics (NDR ≤ 0.01), factual QA, logic, and code generation; the limitation is not a domain-specific artifact but an inherent property of the current RLVR recipe
- RLVR increases token-level entropy while simultaneously decreasing answer-level entropy — seemingly more uncertain generation paths converge onto a smaller set of distinct final answers, producing a decoupled divergence between local and global uncertainty measures
- RLVR substantially reduces a model's ability to assign probability to diverse external reasoning styles — perplexity on Claude Sonnet 4 reasoning traces increases from 8.76 to 14.91 after RLVR training on AIME2024, indicating structural incompatibility with valid alternative approaches
- In shrinkage cases, RLVR-trained models assign higher perplexity to the base model's own successful reasoning traces — confirming that mass collapses away from previously viable solution pathways that were not reinforced, even when those pathways were correct
- RLVR can be improved by noisy or spurious reward signals, undermining confidence that observed pass@1 gains reflect genuine reasoning improvements rather than sharpened exploitation of pre-existing heuristics
- RLVR's ability to expand reasoning capabilities is fundamentally bounded by the base model's initialization — weak base models cannot be rescued by RLVR; the method is essentially a precision-amplifier on existing capability, not a capability creator
- Standard pass@k metrics systematically overstate RLVR's contribution to reasoning capability expansion — pass@k primarily measures solution retrieval (precision at k) rather than whether the model can discover novel reasoning patterns
- SDS (Support Dynamic Score) values remain ≤ 0.07 across all 1.5B–14B models — indicating poor balance between solution preservation and discovery; RLVR improvements arise primarily from probability mass concentration rather than meaningful solution-space expansion

## Bottlenecks

- RLVR's on-policy sampling constraint creates an invisible leash — the algorithm can only train on solutions it can already sample from its current policy, making it mathematically incapable of seeding probability mass into underrepresented correct solution regions; genuine reasoning expansion beyond

## Breakthroughs

- Systematic empirical proof that RLVR is a support-constrained optimizer — the first comprehensive multi-model, multi-domain empirical demonstration that RLVR's precision-diversity trade-off is a fundamental structural property, not a domain artifact, resolving an active research debate

## Themes

- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]

## Key Concepts

- [[entities/cot-passk|CoT-Pass@k]]
- [[entities/grpo|GRPO]]
- [[entities/livebench|LiveBench]]
- [[entities/math500|MATH500]]
- [[entities/reasoning-gym|Reasoning Gym]]
- [[entities/reinforcement-learning-with-verifiable-rewards-rlvr|Reinforcement Learning with Verifiable Rewards (RLVR)]]
- [[entities/passk|pass@k]]
- [[entities/verl|veRL]]
