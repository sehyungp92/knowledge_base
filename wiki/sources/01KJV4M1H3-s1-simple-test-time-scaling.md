---
type: source
title: 's1: Simple test-time scaling'
source_id: 01KJV4M1H37QFTG0NF996MPAA3
source_type: paper
authors:
- Niklas Muennighoff
- Zitong Yang
- Weijia Shi
- Xiang Lisa Li
- Li Fei-Fei
- Hannaneh Hajishirzi
- Luke Zettlemoyer
- Percy Liang
- Emmanuel Candès
- Tatsunori Hashimoto
published_at: '2025-01-31 00:00:00'
theme_ids:
- finetuning_and_distillation
- mathematical_and_formal_reasoning
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# s1: Simple test-time scaling

**Authors:** Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, Li Fei-Fei, Hannaneh Hajishirzi, Luke Zettlemoyer, Percy Liang, Emmanuel Candès, Tatsunori Hashimoto
**Published:** 2025-01-31 00:00:00
**Type:** paper

## Analysis

# s1: Simple test-time scaling
2025-01-31 · paper · Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, Li Fei-Fei et al. (10 total)
https://arxiv.org/pdf/2501.19393

---

### Motivation & Prior Limitations
- OpenAI's o1 demonstrated that test-time scaling is a viable paradigm for improving LM performance, but its methodology was not publicly disclosed, leaving the community without a clear replication path.
  - Prior replication attempts using MCTS, multi-agent approaches, and RL (including DeepSeek R1) required massive data (>800K samples) and multi-stage training pipelines, making them expensive and complex to reproduce.
  - Critically, none of the prior open replication attempts had demonstrated a clear, measurable test-time scaling behavior — monotonically increasing accuracy with more compute — despite achieving competitive absolute performance.
- There was no principled, minimal recipe for achieving both test-time scaling and strong reasoning simultaneously, leaving open the question of how much data and compute are truly necessary.

---

### Proposed Approach
- The paper proposes two components: (1) s1K, a carefully curated dataset of exactly 1,000 question-reasoning trace pairs, and (2) budget forcing, a decoding-time intervention that controls the number of thinking tokens at inference without any additional training.
  - s1K is constructed by first collecting 59,029 questions from 16 sources, then filtering down to 1,000 samples using three criteria applied jointly: quality (removing formatting errors and API failures), difficulty (removing questions solvable by Qwen2.5-7B or Qwen2.5-32B), and diversity (sampling one problem per domain using the Mathematics Subject Classification taxonomy, weighted by reasoning trace length).
  - Reasoning traces in s1K are distilled from Gemini Flash Thinking Experimental via API; 53.6% of s1K traces are graded correct, meaning incorrect reasoning chains are intentionally retained to capture the reasoning process itself.
- Budget forcing operates in two directions: to enforce a maximum, the end-of-thinking delimiter is appended early, forcing the model to produce its current best answer; to enforce a minimum, the end-of-thinking token is suppressed and the string "Wait" is appended to the current reasoning trace, prompting the model to continue reasoning and self-correct.
  - This differs from prior conditional-length methods (token-conditional, step-conditional, class-conditional prompting) which rely on instructing the model in the prompt — methods that fail because models cannot reliably count tokens and learn to "hack" step targets by redistributing token density.
  - Budget forcing requires no reward model, no tree search, and no additional training beyond the initial SFT on 1,000 samples (26 minutes on 16 H100s).

---

### Results & Capabilities
- s1-32B (Qwen2.5-32B-Instruct finetuned on s1K with budget forcing) exceeds o1-preview on competition math: 56.7% vs. 44.6% on AIME24 and 93.0% vs. 85.5% on MATH500, while using only 1,000 training examples.
  - Budget forcing extrapolates AIME24 performance from 50% (no forcing) to 57% by suppressing the end-of-thinking token up to 6 times per problem, demonstrating a clear positive scaling slope.
- s1-32B is the most sample-efficient open reasoning model on the Pareto frontier: Sky-T1 uses 17K samples for 43.3% AIME24, Bespoke-32B uses 17K for 63.3%, and r1-distill uses 800K for 72.6%, while s1-32B achieves 56.7% with 1K.
- Data ablations confirm that combining all three selection criteria is essential: selecting by quality alone (1K-random) yields 36.7% on AIME24, diversity alone (1K-diverse) yields 26.7%, difficulty alone (1K-longest) yields 33.3%, and training on all 59K samples yields only 53.3% — worse than the 1K selection with 56× less compute (7 vs. 394 H100 GPU hours).
- Budget forcing achieves 100% control and a scaling slope of 15 on AIME24, outperforming all tested baselines; token-conditional control achieves only 40% control and negative scaling (−24), while rejection sampling yields inverse scaling (−35) because shorter generations correlate with the model being on the correct track from the start.
- Sequential scaling via budget forcing outperforms parallel scaling via majority voting on Qwen2.5-32B-Instruct at matched compute levels, validating the intuition that sequential computation can build on intermediate results more effectively.

---

### Implications
- The results support a version of the Superficial Alignment Hypothesis applied to reasoning: because LLMs are exposed to large-scale reasoning data during pretraining, SFT on just 1,000 high-quality samples can "activate" latent reasoning capabilities rather than instilling them from scratch, suggesting the marginal cost of building competitive reasoning models may be far lower than assumed.
- Budget forcing establishes a concrete three-metric framework (Control, Scaling, Performance) for evaluating test-time scaling methods, which provides the field with a standardized vocabulary for comparing future approaches.
- The inverse scaling behavior of rejection sampling reveals a structural property of reasoning traces: trace length and correctness are negatively correlated when sampling freely, because short correct solutions reflect early commitment to the right approach while long traces reflect backtracking from errors — this has implications for how process reward models and verifiers should be designed.
- Fully open release of model weights, s1K data, and code directly addresses the transparency gap left by o1 and partially by DeepSeek R1, lowering the barrier for future research on test-time compute scaling.

---

### Remaining Limitations & Next Steps
- Budget forcing eventually flattens and degrades: suppressing the end-of-thinking token more than ~6 times causes the model to enter repetitive loops rather than continuing productive reasoning, imposing a hard ceiling on sequential scaling via this method alon

## Key Claims

1. Training on only 1,000 samples with next-token prediction combined with budget forcing produces a reasoning model that scales in performance with more test-time compute.
2. Supervised finetuning of Qwen2.5-32B-Instruct on s1K required only 26 minutes of training on 16 H100 GPUs.
3. Sequential test-time scaling via budget forcing is more effective than parallel scaling via majority voting for the same base model.
4. Jointly incorporating difficulty, diversity, and quality into data selection is critical; relying on any single criterion leads to significantly worse performance (around -30% on AIME24 on average).
5. Training on all 59K samples does not offer substantial gains over training on the curated 1K subset, while requiring 56x more GPU hours (394 vs 7 H100 GPU hours).
6. Budget forcing achieves 100% controllability over test-time compute, the best among all evaluated methods.
7. Token-conditional control fails without budget forcing because the model cannot reliably count tokens, even when trained to do so.
8. Rejection sampling produces an inverse scaling trend: longer generation budgets lead to lower accuracy because shorter generations correlate with cases where the model was on the correct track from th
9. Budget forcing eventually flattens out as suppressing the end-of-thinking token too often leads the model into repetitive loops rather than continued reasoning.
10. The context window of the underlying language model is a hard constraint on further sequential test-time scaling.

## Capabilities

- SFT on 1,000 carefully curated reasoning samples combined with budget forcing achieves o1-preview-level performance on competition math (56.7% AIME24, 93% MATH500, 59.6% GPQA Diamond), making s1-32B the most sample-efficient open reasoning model
- Budget forcing — suppressing or appending the end-of-thinking delimiter at inference time to force longer or shorter reasoning traces — provides 100% controllability over test-time compute with a positive scaling slope, enabling performance extrapolation from 50% to 57% on AIME24 without any additio
- Sequential test-time scaling via budget forcing empirically dominates parallel scaling via majority voting — majority voting on the base Qwen2.5-32B-Instruct model cannot match s1-32B's accuracy even at much higher parallel compute budgets
- Budget forcing enables mid-reasoning self-correction: when a model tries to terminate with an incorrect answer, suppressing the end-of-thinking token and appending 'Wait' causes the model to re-examine and fix incorrect reasoning steps
- Combining difficulty, diversity, and quality in data curation produces a 1,000-sample SFT dataset competitive with training on 59K samples — reducing compute from 394 GPU hours to 7 GPU hours while achieving near-identical benchmark performance
- Tree search via REBASE (process reward model-guided search) scales beyond the context window ceiling of sequential budget forcing, achieving the best AIME24 accuracy at large compute budgets and outperforming both majority voting and sequential scaling beyond 32K thinking tokens

## Limitations

- Budget forcing eventually flattens out — suppressing the end-of-thinking token more than approximately 6 times causes the model to enter repetitive loops rather than continued productive reasoning, creating a hard ceiling on sequential scaling
- Context window creates a hard ceiling on sequential test-time scaling — when prompted to use up to 512 reasoning steps, 12 out of 30 AIME24 questions exceed the context window, causing a large performance drop
- Language models cannot reliably count tokens — token-conditional control (specifying a maximum number of thinking tokens in the prompt) fails even when models are explicitly trained to do so, making prompt-based compute budget control unreliable
- Models learn to hack step-conditional compute constraints — when given a target number of reasoning steps, models adjust token density per step (shifting between few long steps and many short steps) rather than actually varying total compute, undermining controllability
- Rejection sampling for compute-controlled inference shows inverse scaling — filtering for shorter generations produces better accuracy, because shorter traces correlate with correct initial approaches, not deeper reasoning; longer traces reflect backtracking from errors
- Nearly half (46.4%) of the s1K training data contains incorrect solutions — the fine-tuning dataset used to produce s1-32B has the model learning from traces where ground-truth answers are wrong, with correctness unverified at training time
- Budget forcing and test-time scaling are only demonstrated on mathematical and scientific reasoning benchmarks (AIME24, MATH500, GPQA Diamond) — generalisation to natural language tasks, commonsense reasoning, coding, or open-ended tasks is entirely unexamined
- Budget forcing performance is sensitive to the choice of appended continuation string — 'Wait' substantially outperforms 'Alternatively', 'Hmm', or no string on AIME24, but the optimal string is determined empirically with no theoretical grounding, requiring per-domain search
- SFT-only approach at 1K samples does not match RL-trained models — DeepSeek R1 trained with RL on 800× more samples achieves substantially stronger performance, leaving open whether 1K SFT represents a hard ceiling or is a current optimisation gap
- REBASE tree search requires an additional reward model forward pass at each reasoning step, adding proportional computation overhead — making it impractical for latency-sensitive or resource-constrained deployments despite its superior scaling properties
- Gemini API's 'recitation error' prevents systematic automated evaluation of the teacher model, forcing manual web interface evaluation for AIME24 and omitting MATH500 and GPQA Diamond entirely — introducing unscalable evaluation procedures and gaps in benchmark reporting
- Budget forcing's scaling effect is entirely contingent on SFT training with reasoning traces containing an end-of-thinking delimiter — the technique cannot be applied to arbitrary instruction-tuned models and provides no scaling benefit without the corresponding fine-tuning pipeline

## Bottlenecks

- Sequential test-time scaling via budget forcing is bounded by two compounding hard ceilings: the model's tendency to enter repetitive loops after ~6 forced continuations, and the context window size — both prevent indefinite accuracy extrapolation through sequential compute alone
- Absence of a theoretical understanding of why specific continuation strings ('Wait' vs alternatives) produce different scaling behaviours blocks domain-general, principled budget forcing without empirical search — requiring per-task string tuning with no predictive framework

## Breakthroughs

- First open replication of o1-style test-time scaling curves achieved with minimal training: SFT on 1,000 distilled reasoning examples plus budget forcing (a training-free decoding intervention) produces clear positive scaling behaviour and exceeds o1-preview on AIME24 by up to 27%

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/budget-forcing|Budget Forcing]]
- [[entities/math500|MATH500]]
- [[entities/majority-voting|Majority Voting]]
- [[entities/outcome-reward-model|Outcome Reward Model]]
- [[entities/rejection-sampling|Rejection Sampling]]
- [[entities/test-time-scaling|Test-time Scaling]]
- [[entities/knowledge-distillation-for-reasoning|knowledge distillation for reasoning]]
- [[entities/parallel-test-time-scaling|parallel test-time scaling]]
- [[entities/sequential-test-time-scaling|sequential test-time scaling]]
