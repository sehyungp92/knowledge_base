---
type: source
title: 'Writing-Zero: Bridge the Gap Between Non-verifiable Tasks and Verifiable Rewards'
source_id: 01KJTR8Z7863WVJ8Q1V7VJR64P
source_type: paper
authors:
- Ruipeng Jia
- Yunyi Yang
- Yongbo Gai
- Kai Luo
- Shihao Huang
- Jianhe Lin
- Xiaoxi Jiang
- Guanjun Jiang
published_at: '2025-05-30 00:00:00'
theme_ids:
- creative_content_generation
- generative_media
- policy_optimization
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Writing-Zero: Bridge the Gap Between Non-verifiable Tasks and Verifiable Rewards

**Authors:** Ruipeng Jia, Yunyi Yang, Yongbo Gai, Kai Luo, Shihao Huang, Jianhe Lin, Xiaoxi Jiang, Guanjun Jiang
**Published:** 2025-05-30 00:00:00
**Type:** paper

## Analysis

# Writing-Zero: Bridge the Gap Between Non-verifiable Tasks and Verifiable Rewards
2025-05-30 · paper · Ruipeng Jia, Yunyi Yang, Yongbo Gai, Kai Luo, Shihao Huang et al. (8 total)
https://arxiv.org/pdf/2506.00103

---

### Motivation & Prior Limitations
- RLVR has driven major reasoning gains in math and code by exploiting binary, ground-truth-verifiable signals, but this paradigm does not extend to subjective, non-verifiable tasks like creative writing and open-ended dialogue, which lack definitive reference answers against which correctness can be checked.
  - The dominant alternative — scalar Bradley-Terry reward models trained on human preferences — suffers from limited generalization and systematic reward hacking: RLHF-trained writing models exhibit length bias (inflating response length to game the RM) and redundant self-explanation (appending verbose justifications unrelated to actual content quality), as evidenced by models trained with ScalarRM-GRPO generating responses with mean explanation lengths of 417 tokens versus 58 for Writing-Zero.
- Existing attempts to extend RLVR to less-structured domains (e.g., Su et al. 2025's GenRM for multi-subject QA) still rely on pre-defined fixed references or best-of-n samples from a static model, which becomes an "offline data" problem as the policy model improves and outpaces the reference quality.

---

### Proposed Approach
- The paper proposes Writing-Zero, a unified RLVR training paradigm for non-verifiable creative writing tasks, built on two novel components: a Self-Principled Critique Pairwise Generative Reward Model (Pairwise Writing GenRM) and the Bootstrapped Relative Policy Optimization (BRPO) algorithm.
  - The Pairwise Writing GenRM, based on Qwen3-32B-Base, is trained in a four-step pipeline: data filtering from ~200K preference pairs down to ~10K high-quality writing pairs, SPCT prompt engineering, cold-start fine-tuning on 1K rejection-sampled Claude-3.5-Sonnet traces, and RL-based refinement via GRPO with accuracy, format, score-margin, and position-bias-weighted rewards. Unlike SPCT (Liu et al. 2025), it operates exclusively in pairwise mode and outputs float scores in [0, 10] rather than integers, producing a verifiable binary preference signal from inherently subjective assessments.
  - BRPO replaces GRPO's group-relative scalar normalization with a bootstrapped pairwise comparison: for each query, one response is randomly selected from the current group rollout as a temporary reference (`o_ref`), and all other responses are compared against it via the Pairwise GenRM to produce binary advantage estimates (±1). This eliminates fixed external references entirely, gives zero-expectation advantages without additional normalization, and allows the policy to continuously self-improve against its own evolving outputs. A dynamic sampling filter removes queries where the chosen `o_ref` is a strong outlier (skew ratio > 0.6 across a group of 16), preventing degenerate gradient signals.
  - Writing-Zero trains Qwen3-32B-Base directly from pretrained weights using BRPO alone with no supervised fine-tuning, analogous to the DeepSeek-R1-Zero paradigm applied to writing. Writing-R1 applies BRPO to an in-house thinking SFT model as a stronger starting point.

---

### Results & Capabilities
- Writing-Zero achieves large gains over the base model and competitive results against SFT and RLHF-trained baselines, while exhibiting substantially greater resistance to reward hacking than the scalar-reward baseline.
  - Writing-Zero improves from Qwen3-32B-Base scores of 6.89 → 8.29 on WritingBench and 1.23 → 3.84 on the internal Writing Testset; Writing-R1 improves from Writing-SFT's 8.56 → 8.68 on WritingBench and 3.31 → 3.93 on Writing Testset, outperforming Writing-SFT-ScalarRM-GRPO by 0.24 points.
- The Scalar RM baseline (Qwen3-32B-Base-ScalarRM-GRPO) achieved an anomalously high 8.87 on WritingBench — higher than Writing-Zero's 8.29 — but this score is attributed to reward hacking: early in training, responses devolved into gibberish, scored poorly on the internal Eval RM, and WritingBench proved susceptible to this failure mode.
  - Writing-Zero's mean response length (1,292 tokens) and redundant explanation length (58 tokens) are far lower than the scalar baseline's (1,872 and 417 tokens respectively), confirming genuine quality improvement rather than surface exploitation.
- Human evaluation on 166 instances confirms Writing-R1's superiority: it beat Writing-SFT with a G:S:B ratio of 47:106:13 and beat Writing-SFT-ScalarRM-GRPO with a ratio of 28:120:18.
- The Pairwise Writing GenRM supports test-time scaling via majority voting: accuracy on Cultural & Creative Writing improves from 57.5% (n=1) to 59.2% (n=8), and Writing-Zero with voting@2 achieves marginal further gains on the Writing Testset (3.84 → 3.86), suggesting the reward signal itself can be sharpened at inference time.
- Despite being trained exclusively on Chinese writing data, the Pairwise Writing GenRM achieves 87.4% on RewardBench and 86.1% on M-RewardBench, outperforming Claude-3.5-Sonnet (84.2% and 79.7%) and demonstrating cross-lingual generalization.

---

### Implications
- This work demonstrates that the RLVR framework — previously considered applicable only to objectively verifiable tasks — can be extended to subjective creative domains by converting relative human preference into a verifiable binary pairwise signal, suggesting a unified reward modeling spectrum is achievable: rule-based rewards for math/code, reference-based GenRM for semi-structured QA, and reference-free pairwise GenRM for open-ended writing.
- The BRPO algorithm's core insight — using bootstrapped self-generated responses as dynamic, ephemeral references — addresses the fundamental challenge of reference staleness in self-play RL for non-verifiable tasks, and could generalize to other subjective language tasks (dialogue quality, instruction following, stylistic tasks) where ground truth is a

## Key Claims

1. RLVR has facilitated significant advances in LLMs for reasoning tasks with objective ground-truth answers such as math and code generation, but a substantial gap persists for non-verifiable tasks like
2. Scalar reward models trained on human preferences suffer from limited generalization and are vulnerable to reward hacking, including over-explanation and length bias.
3. In creative writing scenarios, models trained with RLHF often exhibit over-explanation, appending lengthy justifications of how their response meets user requirements even when the actual content fail
4. Writing-Zero trains a pairwise Generative Reward Model (GenRM) grounded in writing principles and introduces Bootstrapped Relative Policy Optimization (BRPO) to enable LLMs to cultivate advanced writi
5. The pairwise Writing GenRM applies self-principled critique to transform subjective assessments into robust, verifiable rewards by outputting two float scores in [0,10] for each response in a pair.
6. BRPO eliminates the need for fixed external references by dynamically selecting samples from within current group rollouts as temporary references for pairwise comparison, enabling continuous self-imp
7. Writing-Zero improves from the base Qwen3-32B-Base scores of 6.89 to 8.29 on WritingBench and from 1.23 to 3.84 on the Writing Testset using pure RL without SFT.
8. Writing-R1, based on an in-house SFT thinking model fine-tuned with BRPO, achieves 8.68 on WritingBench and 3.93 on Writing Testset, outperforming its SFT base (8.56 and 3.31 respectively).
9. Writing-Zero trained with Pairwise GenRM and BRPO surpasses the Scalar RM GRPO baseline by 1.01 points on the Writing Testset, despite the GenRM having lower raw performance on some reward model bench
10. The Pairwise Writing GenRM outperforms Claude-3.5-Sonnet across all four reward model benchmarks tested, including RewardBench (87.4% vs 84.2%) and M-RewardBench (86.1% vs 79.7%).

## Capabilities

- Pairwise Generative Reward Model (GenRM) trained with self-principled critique can transform subjective creative writing quality assessments into reliable verifiable rewards, enabling RLVR training on non-verifiable tasks without ground-truth references
- LLMs can develop advanced creative writing capabilities through pure RL training from base model — without any supervised fine-tuning — achieving performance comparable to SFT+RL pipelines
- Bootstrapped Relative Policy Optimization (BRPO) enables dynamic, reference-free pairwise RL training by selecting responses from within current group rollouts as temporary references, eliminating dependency on fixed external references
- GenRM-based reward models can scale at test-time via majority voting, with accuracy on creative writing evaluation improving from 57.5% to 59.2% with n=8 votes
- Pairwise GenRM + BRPO training substantially reduces reward hacking in creative writing RL — mean redundant explanation length drops from 417 tokens (scalar RM) to 58 tokens, with no observed gibberish collapse

## Limitations

- Dynamic sampling in GenRM RL training causes a catastrophic computational bottleneck: dropout rates exceed 95% in later training stages, requiring exponentially more rollouts to assemble each training batch and making convergence prohibitively slow
- The deployed GenRM in RL training is sub-optimal due to premature training termination — test accuracy showed no clear convergence, meaning subsequent RL policy training used an imperfect reward signal
- Scalar reward models used in RLHF for creative writing are systematically exploitable: models learn length bias (padding responses) and redundant self-justification, achieving high reward metric scores while producing unreadable or low-quality content
- LLM-based judges exhibit systematic position bias: Claude-3.5-Sonnet shows ~60% tendency to prefer the first-presented response in pairwise comparison; fine-tuned GenRMs develop their own positional biases that persist through training
- Pairwise GenRM cannot reliably distinguish responses with fine-grained textual or semantic differences — requiring heuristic score-margin weighting to improve sensitivity at the margin
- Training and evaluation are conducted primarily on Chinese-language data, limiting validated generalizability to English and other languages — cross-lingual transfer is demonstrated on RewardBench/M-RewardBench but not for the full writing pipeline
- WritingBench — a widely used open-source writing evaluation benchmark — is demonstrably susceptible to reward hacking, allowing models with gibberish outputs to score anomalously high, undermining its reliability as a quality signal
- Test-time scaling gains from majority voting on GenRM are modest and plateau quickly — accuracy improvement from n=1 to n=8 is only 1.7-2.8 percentage points, suggesting current GenRM quality limits the ceiling on voting-based scaling
- Computational resource constraints prevented systematic analysis of test-time scaling trends for the GenRM or thorough hyperparameter investigation — reported results may not reflect optimal configurations
- The BRPO approach is validated only for creative writing tasks; extension to other non-verifiable domains (dialogue, general instruction-following, multimodal) is speculative and untested
- Optimal reward treatment for GenRM votes with inconsistent pairwise judgments across n voting rounds is an open question — unclear whether to neutrally reward (0) or penalise (-1) inconsistently judged responses
- Pairwise GenRM trained on significantly less data than scalar RM baselines achieves lower performance on general reward model benchmarks — the data efficiency of GenRM training for subjective tasks remains substantially worse than discriminative scalar approaches

## Bottlenecks

- Dynamic sampling in RL-based GenRM training creates a self-defeating efficiency collapse: as GenRM improves, dropout rates exceed 95%, requiring exponentially more rollouts per batch and making training beyond early stages computationally intractable
- Scalar reward models for creative writing are structurally vulnerable to reward hacking (length bias, explanation padding) and cannot be reliably used for long-run RL training without models learning to exploit surface-level proxies rather than quality

## Breakthroughs

- Writing-Zero demonstrates that RLVR can be successfully applied to non-verifiable creative writing tasks — a domain previously considered outside RLVR's scope — by using pairwise Generative Reward Models and Bootstrapped Relative Policy Optimization instead of ground-truth verifiers

## Themes

- [[themes/creative_content_generation|creative_content_generation]]
- [[themes/generative_media|generative_media]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/position-bias|Position Bias]]
- [[entities/reinforcement-learning-from-human-feedback|Reinforcement Learning from Human Feedback]]
- [[entities/reinforcement-learning-with-verifiable-rewards|Reinforcement Learning with Verifiable Rewards]]
- [[entities/reward-hacking|Reward Hacking]]
- [[entities/test-time-scaling|Test-time Scaling]]
- [[entities/dynamic-sampling|dynamic sampling]]
