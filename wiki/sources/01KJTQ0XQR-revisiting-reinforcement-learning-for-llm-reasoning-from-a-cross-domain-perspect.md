---
type: source
title: Revisiting Reinforcement Learning for LLM Reasoning from A Cross-Domain Perspective
source_id: 01KJTQ0XQRB50VSN951C5WB06K
source_type: paper
authors:
- Zhoujun Cheng
- Shibo Hao
- Tianyang Liu
- Fan Zhou
- Yutao Xie
- Feng Yao
- Yuexin Bian
- Yonghao Zhuang
- Nilabjo Dey
- Yuheng Zha
- Yi Gu
- Kun Zhou
- Yuqi Wang
- Yuan Li
- Richard Fan
- Jianshu She
- Chengqian Gao
- Abulhair Saparov
- Haonan Li
- Taylor W. Killian
- Mikhail Yurochkin
- Zhengzhong Liu
- Eric P. Xing
- Zhiting Hu
published_at: '2025-06-17 00:00:00'
theme_ids:
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Revisiting Reinforcement Learning for LLM Reasoning from A Cross-Domain Perspective

> This paper provides the first systematic cross-domain investigation of reinforcement learning for LLM reasoning, revealing that the dominant "elicitation vs. acquisition" debate is domain-dependent rather than a universal property of RL. The authors introduce GURU, a 92K-example multi-domain RL corpus spanning Math, Code, Science, Logic, Simulation, and Tabular reasoning, and use it to show that domains underrepresented in pretraining require in-domain RL data to improve, that uniform domain mixing matches single-domain specialists, and that many widely-held beliefs about RL behavior (longer outputs, uniform Pass@k patterns) do not generalize across domains.

**Authors:** Zhoujun Cheng, Shibo Hao, Tianyang Liu, Fan Zhou, Yutao Xie, Feng Yao, Yuexin Bian, Yonghao Zhuang, Nilabjo Dey, Yuheng Zha, Yi Gu, Kun Zhou, Yuqi Wang, Yuan Li, Richard Fan, Jianshu She, Chengqian Gao, Abulhair Saparov, Haonan Li, Taylor W. Killian, Mikhail Yurochkin, Zhengzhong Liu, Eric P. Xing, Zhiting Hu
**Published:** 2025-06-17
**Type:** paper

---

## Motivation

The [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] field has developed almost entirely within the math and code domains, which offer easily verifiable answers and abundant benchmark data. This concentration introduced a structural blind spot: conclusions drawn from these domains were treated as universal truths about RL's mechanisms, when they may simply reflect the unusual properties of math as a domain (dense pretraining coverage, deterministic answer verification, clean difficulty gradients).

Three prior assumptions were particularly at risk:

1. **RL primarily elicits latent knowledge**, not acquiring genuinely new skills.
2. **RL drives models to produce longer responses** as a general phenomenon.
3. **Pass@k behavior is approximately uniform across tasks**, with RL gains narrowing at large k.

Each of these was established almost entirely on math benchmarks. The paper tests all three across six domains and finds that none holds universally.

A secondary motivation is data infrastructure: even within well-studied domains, publicly available RL datasets contain severe redundancy (conservative substring deduplication eliminates 27.2% of Math samples across major datasets like OR1, Open-Reasoner, and NovaSky). And outside math/code, there was no systematic effort to construct verifiable RL training data at scale.

---

## The GURU Corpus

GURU is a 92K-example dataset built through a five-stage domain-specific pipeline applied to each of six reasoning domains.

**Domains and reward types:**

| Domain | Examples | Reward type |
|---|---|---|
| Math | ~varied | Rule-based matching |
| Code | ~varied | Execution-based verification |
| Science | ~3.6K usable / 232K raw | Model-based (1.5B verifier) |
| Logic | ~varied | Rule-based matching |
| Simulation | ~varied | Rule-based matching |
| Tabular | ~varied | Rule-based matching |

The Logic domain covers symbolic grid puzzles, Zebra/Ordering/Graph constraint satisfaction puzzles. Simulation covers code I/O prediction (predicting program output without executing it). Tabular covers hierarchical table QA. These three had not been covered by any prior large-scale open RL effort; existing datasets claiming "general reasoning" coverage remained confined to STEM.

**Difficulty filtering** uses empirical pass rates across 16 runs from both a weak model (Qwen2.5-7B-Instruct) and a strong model (Qwen3-30B-A8B). Samples are discarded if: the weak model solves them almost always (too easy), neither model can solve them (likely noisy or broken), or the weak model outperforms the strong model (label contamination). This reduces the raw pool of 684.9K examples to 91.9K. Science loses 98.4% of its raw samples in the process, the most aggressive filtering of any domain.

**Training:** GURU-7B and GURU-32B are trained directly with GRPO on the full GURU dataset using the verl framework, without any SFT warmup, so performance gains are attributable to RL data rather than confounded by SFT.

---

## Key Findings

### 1. The elicitation vs. acquisition divide follows pretraining exposure

The paper's central empirical finding is a clean two-tier structure based on how much pretraining data covered each domain:

- **Math, Code, Science** (high pretraining coverage): benefit from cross-domain RL training. A model trained only on Logic data still improves meaningfully on Math. The knowledge was already there; RL from almost any domain can unlock it.
- **Logic, Simulation, Tabular** (low pretraining coverage): show near-zero gain from any non-in-domain training. On Zebra Puzzle, math-focused baselines like ORZ-7B score 1.00% and SimpleRL-7B scores 0.62%, while GURU-7B (which saw Logic training data) scores 39.40%.

This reframes the prior debate. The claim that "RL elicits but doesn't teach" was never wrong for math; it just doesn't generalize. RL's role becomes increasingly generative as training is applied to domains with thin pretraining coverage.

Pass@k analysis supports this interpretation directly. On AIME24 at 7B scale, GURU-7B and the base model cross at k=64, reproducing the Yue et al. (2025) pattern suggesting existing capability exploitation. On Zebra Puzzle, GURU-7B and GURU-32B both exceed the base model at every tested value of k, indicating genuine expansion of the reachable reasoning space.

### 2. Uniform domain mixing matches single-domain specialists

GURU-18K (3K samples per domain, uniformly mixed) matches or exceeds single-domain training performance across all individual benchmarks. This is a non-trivial result: cross-domain data does not introduce significant interference between domains at this scale, and the generalist model inherits the gains of each specialist without curriculum design, domain weighting, or multi-stage training.

This finding matters practically: it suggests the standard recipe (pick a math dataset, train) is leaving general reasoning performance on the table for free.

### 3. Response length is domain-contingent, not a universal RL property

RL training contracts output length on Code, Logic, and Tabular tasks, while expanding it on Math and Science. The common belief that "RL drives models to produce longer responses" is a Math-specific artifact, not a property of RL. Length correlates with performance gains in Math and Science but not in Code, Logic, or Tabular domains. This makes response length an unreliable proxy for reasoning effort.

### 4. Difficulty filtering introduces a cross-domain tradeoff

Domain-specific difficulty filtering consistently improves in-domain performance (AIME24: +5.9, AMC: +6.3) but causes notable degradation on easier tasks in other domains (HumanEval: -9.2, HiTab: -3.0). Filtering for hard math problems creates a training distribution that harms simpler cross-domain generalization. This difficulty-transfer tradeoff had not been previously characterized.

---

## Results

GURU-7B and GURU-32B achieve 43.29% and 54.24% on a 17-task evaluation suite across six domains, outperforming the best open baselines by 9.0% and 6.7% respectively.

Domain-specific baselines degrade badly outside their training distribution:
- Math-focused ORZ-7B and SimpleRL-7B: near-zero on Zebra Puzzle, weak on tabular tasks.
- STEM-focused General-Reasoner: improves over math-only baselines but still fails on Logic and Simulation domains.

The most difficult tasks remain largely unsolved:
- ARC-AGI: GURU-7B achieves 3.31%, GURU-32B achieves 7.63%, with negligible gains from RL.
- CodeI/O (code execution simulation, hardest variant): similarly stagnant.

Instruction following (IFEval) and open-ended adaptation (LiveBench) are degraded or not improved by reasoning RL, with GURU-7B scoring below General Reasoner baselines on both.

---

## Limitations and Open Questions

**Compute accessibility.** Training required 20 nodes × 8 Hopper GPUs for 2-3 days per model scale. The cost of domain-diverse curriculum experiments is prohibitive for most research groups.

**Model-family specificity.** RLVR gains are consistently pronounced with Qwen models. Generalization to other model families is significantly less reliable, undermining claims about the universality of the findings.

**Entropy collapse.** RL training narrows output diversity, reducing Pass@k at large k by converging toward similar reasoning trajectories. Raising sampling temperature or top-p partially counteracts this, but the underlying entropy collapse is a structural consequence of policy optimization, not a hyperparameter artifact.

**Science domain noise.** Model-based reward verification for science tasks filters 98.4% of raw data, and residual noise requires further stricter filtering. The 1.5B verifier introduces inherent noise that rule-based rewards avoid.

**ARC-AGI remains blocked.** Abstract pattern completion at the ARC-AGI level is not solved by any amount of multi-domain RL training at these scales. It likely requires something beyond coverage diversity, whether that is visual-spatial reasoning, program synthesis, or qualitatively different training signals.

**Pass@k sensitivity.** Pass@k curves are highly sensitive to decoding hyperparameters (temperature, top-p) and RL-induced entropy collapse, making cross-study comparisons unreliable. The paper recommends treating Pass@k as informative but not exhaustive.

**Instruction following and general adaptation.** Reasoning RL degrades IFEval and LiveBench performance relative to baselines, suggesting a specialization tradeoff where gains in structured problem-solving come at the cost of flexible instruction following.

---

## Connections

### Themes
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]: direct contribution; systematically characterizes RL's behavior across domains.
- [[themes/reinforcement_learning|Reinforcement Learning]]: methodology; GRPO training, reward design, policy optimization dynamics.
- [[themes/reasoning_and_planning|Reasoning and Planning]]: central evaluation target; multi-domain reasoning benchmarks across six categories.
- [[themes/reward_modeling|Reward Modeling]]: key contribution; domain-specific reward design including model-based verification for open-ended science.
- [[themes/pretraining_and_scaling|Pretraining and Scaling]]: foundational to the central finding; pretraining exposure determines whether RL elicits or acquires capabilities.

### Key relationships
- The elicitation/acquisition finding revises claims from prior work (Yue et al. 2025, Open-Reasoner-Zero, SimpleRL) that were derived entirely from math benchmarks.
- The entropy collapse finding connects to broader concerns about [[themes/reinforcement_learning|policy optimization]] narrowing model behavior; a related dynamic appears in RLHF reward hacking and mode collapse research.
- The difficulty-transfer tradeoff connects to curriculum learning and multi-task interference research: harder domain-specific training is not free when evaluated against generalist objectives.
- The ARC-AGI stagnation connects to the broader [[themes/reasoning_and_planning|abstract reasoning]] bottleneck, which RL at current scales does not appear to address.

---

## Significance

This paper is primarily a calibration work: it does not introduce a new training paradigm but instead provides the empirical infrastructure to test whether existing paradigms generalize. The GURU corpus addresses a genuine data gap, the cross-domain transfer analysis resolves a contested theoretical question, and the domain-contingent behavioral findings (length, Pass@k, elicitation vs. acquisition) provide concrete corrections to field-wide assumptions.

The most durable contribution is the pretraining-exposure framework: the "elicitation vs. acquisition" dichotomy is not about RL per se, but about the relationship between RL training domain and pretraining coverage. This reframes how researchers should think about where RL will and won't generalize as reasoning models are applied to new problem types.

## Key Concepts

- [[entities/arc-agi|ARC-AGI]]
- [[entities/grpo|GRPO]]
- [[entities/qwen25|Qwen2.5]]
- [[entities/rlvr|RLVR]]
- [[entities/passk|pass@k]]
- [[entities/verl|veRL]]
