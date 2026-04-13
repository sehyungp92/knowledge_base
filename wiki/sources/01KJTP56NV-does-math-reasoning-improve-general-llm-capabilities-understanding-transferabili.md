---
type: source
title: Does Math Reasoning Improve General LLM Capabilities? Understanding Transferability
  of LLM Reasoning
source_id: 01KJTP56NVHW0GKJH3XQCG4E4V
source_type: paper
authors:
- Maggie Huan
- Yuetai Li
- Tuney Zheng
- Xiaoyu Xu
- Seungone Kim
- Minxin Du
- Radha Poovendran
- Graham Neubig
- Xiang Yue
published_at: '2025-07-01 00:00:00'
theme_ids:
- finetuning_and_distillation
- mathematical_and_formal_reasoning
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Does Math Reasoning Improve General LLM Capabilities? Understanding Transferability of LLM Reasoning

**Authors:** Maggie Huan, Yuetai Li, Tuney Zheng, Xiaoyu Xu, Seungone Kim, Minxin Du, Radha Poovendran, Graham Neubig, Xiang Yue
**Published:** 2025-07-01 00:00:00
**Type:** paper

## Analysis

# Does Math Reasoning Improve General LLM Capabilities? Understanding Transferability of LLM Reasoning
2025-07-01 · paper · Maggie Huan, Yuetai Li, Tuney Zheng, Xiaoyu Xu, Seungone Kim et al. (9 total)
https://arxiv.org/pdf/2507.00432

---

### Motivation & Prior Limitations
The dominant assumption in post-training research is that improving math reasoning — a verifiable, well-posed proxy task — yields broadly transferable problem-solving ability, but this assumption had not been rigorously tested across diverse task categories.
- Math leaderboards had been advancing rapidly (some models surpassing human expert performance on AIME and MATH), yet evaluation remained siloed within math benchmarks, leaving the question of cross-domain transfer empirically unresolved.
  - OpenAI's o1, while excelling on STEM benchmarks, raised concerns about versatility on non-STEM tasks; Wang et al. (2024b) observed that fine-tuning on narrow instruction types degrades performance on other skills — but no systematic study had isolated the causal role of the fine-tuning paradigm (RL vs. SFT) while controlling for dataset, architecture, and model size.
- SFT-based distillation pipelines (e.g., training on CoT traces from a strong teacher via rejection sampling) had become the standard post-training recipe for reasoning models, without adequate understanding of their downstream effects on general-domain representations.

---

### Proposed Approach
The paper conducts a two-part empirical investigation: a large-scale audit of over 20 open-weight reasoning-tuned models evaluated across math, other reasoning, and non-reasoning benchmarks, followed by a controlled ablation experiment directly comparing SFT and RL on identical data from the same base model (Qwen3-14B-Base).
- To enable quantitative comparison across models and task groups, the authors introduce the Transferability Index (TI), a metric that normalizes per-benchmark gains via z-scoring, applies difficulty weighting (harder tasks receive higher weight via `w_b = 100 − R_base`), uses signed square-root compression to control outliers, and expresses cross-domain transfer as a ratio relative to math improvement.
  - TI > 0 indicates positive transfer; TI < 0 indicates the model degraded below its base on that task group, allowing negative transfer to be detected and quantified across both "other reasoning" and "non-reasoning" task clusters.
- For the controlled study, SFT targets are CoT traces from Qwen3-32B with rejection sampling (keeping only correct answers), while RL (GRPO) uses only ground-truth answer labels as reward — ensuring both paradigms learn from the same underlying math queries, isolating the training objective as the sole variable.
- To diagnose mechanistic causes, the paper applies two diagnostic tools: (1) PCA shift analysis on hidden states across all layers (measuring Euclidean distance between representation centroids before and after fine-tuning), and (2) KL-divergence and token rank shift analysis on output token distributions.
- An ablation study systematically varies four RL components — sampling distribution (on-policy vs. off-policy), credit assignment (advantage weighting vs. uniform), KL regularization (present vs. absent), and negative gradient (RL penalizes bad samples; SFT does not) — using five experimental configurations on Qwen3-8B-Base with the same math dataset.

---

### Results & Capabilities
RL fine-tuning on math-only data generalizes broadly across task types, while SFT fine-tuning on the same data causes catastrophic forgetting on non-reasoning tasks — a finding that holds consistently across model sizes, families, and training data distributions.
- In the controlled study on Qwen3-14B-Base, the RL-tuned UniReason model achieves TI_non = +52.2, while the best SFT variant (SFT-think) achieves TI_non = −104.1, despite both being trained on the same math queries; the SFT model's non-reasoning average drops from 45.7% (base) to 21.1%, while RL raises it to 53.2%.
- On math benchmarks, RL slightly outperforms SFT: UniReason-RL reaches 55.7% on AIME24 and 87.8% on MATH-500, vs. 52.0% and 85.0% for the best SFT variant; the RL advantage on OlympiadBench is larger (+8.8 points), suggesting RL generalizes better even within harder math.
- PCA shift analysis confirms that RL preserves internal representation geometry: RL models show mean PCA shift distances of 8.5 (math), 3.5 (other-reasoning), and 36.9 (non-reasoning), compared to SFT-think values of 19.2, 6.7, and 38.2 — and SFT-no-think values of 21.4, 10.9, and 113.7.
  - The most dramatic divergence appears on HalluEval, where SFT-no-think causes a centroid shift distance of 109.3 while RL causes only 26.0, consistent with the observed 26.9-point accuracy drop for SFT vs. a +5.0-point gain for RL on that benchmark.
- KL-divergence analysis shows RL models maintain near-baseline token distributions: UniReason-RL achieves KL divergences of 0.084 (MATH-500) and 0.019 (IFEval), versus 0.372 and 0.283 for SFT-no-think on the same tasks. RL shifts an average of only 0.98 token rank positions, compared to 10.6 for SFT-no-think.
  - Word cloud analysis reveals that RL selectively shifts logical-structural tokens ("But", "So", "define", "add") while SFT shifts hundreds of tokens including query-irrelevant ones that inject reasoning markers into non-reasoning prompts (390 shifted tokens for reasoning, 158 for non-reasoning in SFT vs. a small targeted set for RL).
- The ablation identifies on-policy sampling as the single most important factor driving generalization: on-policy SFT outperforms off-policy SFT on both other-reasoning and non-reasoning tasks (TI_non = +30.2 vs. −40.5), and on-policy RL outperforms off-policy RL similarly. Credit assignment and negative gradient also improve transferability, while KL regularization has minimal marginal effect when training is already on-policy.
  - Gradient norm trajectories confirm that off-policy methods produce large, abrupt gra

## Key Claims

1. Most reasoning-tuned models that succeed in math fail to transfer their gains to other domains such as scientific QA, agent planning, coding, and instruction-following.
2. Reinforcement learning (RL)-tuned models generalize well across domains when trained on math-only data, while supervised fine-tuning (SFT)-tuned models often exhibit catastrophic forgetting of general
3. SFT induces substantial latent-space representation drift and output token distribution drift, while RL preserves general-domain feature geometry and token distribution stability.
4. The fine-tuning paradigm (RL vs. SFT) is the dominant factor predicting transferability across model families and sizes, outweighing model size, data distribution, and architecture.
5. RL-tuned models consistently achieve higher Transferability Index on both other-reasoning and non-reasoning tasks, whereas SFT-trained models often yield negative TI on non-reasoning tasks.
6. SFT on large static reasoning corpora can over-specialize the latent space, degrading non-reasoning performance, while on-policy RL reinforces reasoning while minimally perturbing general-domain repre
7. UniReason-Qwen3-14B trained with RL on 47K math examples achieves 55.7% on AIME24, 87.8% on MATH500, and 33.8% on OlympiadBench, outperforming SFT-based models on math reasoning.
8. SFT-trained models on non-reasoning tasks (CoQA, MC-TACO, IFEval, HaluEval) stagnate or drastically decline, while the RL model recovers and exceeds the base model in nearly all non-reasoning benchmar
9. RL-trained models exhibit the lowest PCA shift magnitudes across math, other-reasoning, and non-reasoning tasks, indicating stable latent representations compared to SFT models.
10. SFT models exhibit scattered and larger latent shifts, particularly for non-reasoning inputs, whereas RL models yield minimal and tightly clustered latent shifts across diverse benchmarks.

## Capabilities

- RL-tuned models trained exclusively on math data achieve positive transfer to both other reasoning and non-reasoning tasks — UniReason-Qwen3-14B (RL) trained on 47K math examples improves over the base model on all non-reasoning benchmarks (53.2% avg vs 45.7% base), while SFT variants degrade to 21.
- GRPO-based on-policy RL fine-tuning on math achieves competitive math performance while preserving general-domain capabilities — UniReason-Qwen3-14B (RL) reaches 55.7% AIME24, 87.8% MATH500, 33.8% OlympiadBench using only 47K math examples
- PCA shift analysis on hidden states across layers provides a reliable, interpretable diagnostic for measuring representational drift and predicting cross-domain transferability after fine-tuning — more faithful than weight-based metrics
- On-policy RL training selectively shifts only a small set of task-relevant tokens (avg 0.98 positions shift) while preserving the base token distribution — enabling stable cross-domain generalization without multi-domain training data

## Limitations

- SFT fine-tuning on math reasoning causes catastrophic forgetting of non-reasoning capabilities — the SFT-think variant drops CoQA from 10.0% to 1.7%, IFEval from 69.2% to 42.3%, and HalluEval from 35.7% to 2.3%, yielding a TInon of –104.1
- The majority of reasoning-tuned open-weight models fail to transfer math gains to other domains — negative Transferability Index on non-reasoning tasks is the norm for SFT-based models regardless of size or architecture
- SFT fine-tuning induces substantial latent space drift on non-reasoning inputs — PCA centroid distance reaches 129.8 for SFT-no-think on non-reasoning tasks vs 36.9 for RL, indicating disrupted internal feature geometry for out-of-distribution prompts
- SFT models inject reasoning markers (logical tokens, CoT structure) into responses to non-reasoning prompts — token rank analysis shows SFT shifts 390 tokens for reasoning and 158 for non-reasoning tasks, most of them query-irrelevant
- KL regularization in RL training has only subtle effects on cross-domain transferability — on-policy RL performance is largely unchanged with or without KL penalty, indicating standard regularization techniques are insufficient to resolve generalization gaps on their own
- Controlled experiments are limited to 8B and 14B parameter models — whether the RL vs SFT generalization gap holds at frontier scale (70B+, GPT-4 class) is unverified and may not extrapolate
- The study is limited to math as the source domain for RL fine-tuning — whether RL on other reasoning domains (code, scientific reasoning) shows comparable cross-domain generalization is not investigated
- Evaluation is confined to accuracy on fixed benchmarks — generation quality, fluency, open-ended instruction following, and real-world deployment behavior are not assessed; the paper acknowledges no tools exist for transferability in multi-modal or long-context settings

## Bottlenecks

- Standard SFT-distilled post-training recipe for reasoning causes systematic catastrophic forgetting — the dominant training approach (SFT on teacher-generated CoT traces from stronger models) structurally degrades non-reasoning capabilities, blocking deployment of reasoning-specialized models as gen
- Off-policy training data distribution mismatch in SFT blocks generalization — models trained on static, fixed teacher-generated datasets face systematic distribution shift at inference time, causing latent space over-specialization and degraded cross-domain transfer

## Breakthroughs

- Empirical demonstration across 20+ models and controlled experiments that fine-tuning paradigm (RL vs SFT) is the decisive factor in cross-domain transferability of reasoning capabilities — independent of model size, architecture, and training data distribution
- Mechanistic quantification of why SFT causes catastrophic forgetting and RL preserves generalization — PCA centroid shift (up to 129.8 for SFT vs 36.9 for RL on non-reasoning tasks) and KL divergence (0.37–0.49 for SFT vs 0.02–0.08 for RL) precisely characterize the representational divergence respo

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/catastrophic-forgetting|Catastrophic Forgetting]]
- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/grpo|GRPO]]
- [[entities/ifeval|IFEval]]
- [[entities/math500|MATH500]]
- [[entities/olympiadbench|OlympiadBench]]
- [[entities/rejection-sampling-fine-tuning|Rejection Sampling Fine-Tuning]]
