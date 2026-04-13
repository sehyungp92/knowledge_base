---
type: source
title: Reinforcement Pre-Training
source_id: 01KJTQH85KRGRP02JGFVY2ZZF6
source_type: paper
authors:
- Qingxiu Dong
- Li Dong
- Yao Tang
- Tianzhu Ye
- Yutao Sun
- Zhifang Sui
- Furu Wei
published_at: '2025-06-09 00:00:00'
theme_ids:
- chain_of_thought
- policy_optimization
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 18
tags: []
---
# Reinforcement Pre-Training

**Authors:** Qingxiu Dong, Li Dong, Yao Tang, Tianzhu Ye, Yutao Sun, Zhifang Sui, Furu Wei
**Published:** 2025-06-09 00:00:00
**Type:** paper

## Analysis

# Reinforcement Pre-Training
2025-06-09 · paper · Qingxiu Dong, Li Dong, Yao Tang, Tianzhu Ye, Yutao Sun et al. (7 total)
https://arxiv.org/pdf/2506.08007

---

### Motivation & Prior Limitations
- Current RL applications in LLM training suffer from a fundamental scalability-generality tradeoff that prevents RL from being used during pre-training at web-text scale.
  - RLHF depends on costly human preference data and learned reward models that are susceptible to reward hacking, limiting its scalability and reliability.
  - RLVR (reinforcement learning with verifiable rewards) mitigates reward hacking via rule-based rewards from question-answer pairs, but is constrained by the scarcity of annotated data with verifiable answers, restricting it to domain-specific fine-tuning rather than general-purpose pre-training.
- Standard next-token prediction (NTP), while scalable and general, trains models to learn superficial token-level correlations rather than the hidden knowledge underlying sequences, potentially limiting reasoning depth and generalization.

---

### Proposed Approach
- RPT reframes next-token prediction as a *next-token reasoning* task trained with on-policy RL, using the ground-truth next token from the corpus itself as an intrinsic, verifiable reward signal — eliminating the need for any external annotations or domain-specific reward functions.
  - For each context prefix `x<t`, the model generates G chain-of-thought reasoning trajectories (involving brainstorming, self-critique, and self-correction) before predicting the next token; a binary reward of 1 is assigned if the prediction exactly matches the ground-truth continuation, 0 otherwise.
  - A *prefix matching reward* is introduced to handle multi-token predictions and out-of-vocabulary tokens, checking that the byte sequence of the prediction is an exact prefix of the ground-truth completion at a valid token boundary — making the reward robust to tokenization artifacts.
  - Token-level data filtering is applied before training: a small proxy model (DeepSeek-R1-Distill-Qwen-1.5B) computes entropy over the top-16 next tokens at each position, and low-entropy (easily predictable) positions are filtered out, concentrating compute on challenging tokens where reasoning is most valuable.
  - Training uses DeepSeek-R1-Distill-Qwen-14B as the base model with the GRPO algorithm, implemented via the verl library, on the OmniMATH dataset (4,428 competition-level math problems).
- The key architectural insight is that the internal chain-of-thought during pre-training functions as training-time inference scaling — the model allocates more computational effort per token prediction, analogous to test-time compute but applied during pre-training itself.

---

### Results & Capabilities
- RPT significantly improves next-token prediction accuracy compared to standard NTP on the pre-training corpus, with performance consistently increasing as training compute scales up.
  - The scaling curves show a clear positive relationship between training compute and next-token prediction accuracy under RPT, positioning it as a sustainable scaling paradigm.
- RPT yields a stronger pre-trained foundation for subsequent reinforcement fine-tuning, leading to better final task performance compared to models pre-trained with standard NTP.
- RPT improves zero-shot performance on various downstream tasks, suggesting the next-token reasoning objective induces more generalizable representations than rote memorization of token sequences.

---

### Implications
- RPT opens a new axis of RL scaling that is not constrained by annotated data: by deriving verifiable rewards intrinsically from any text corpus, it makes RL applicable during pre-training at the scale of the entire web — a qualitative shift from RLVR's domain-specific fine-tuning regime.
- The result challenges the assumption that RL's role in LLM training is confined to post-training alignment and skill elicitation; if pre-training itself can be RL-driven with verifiable rewards, the distinction between pre-training and fine-tuning objectives may blur significantly.
- The framing of chain-of-thought generation as training-time inference scaling has implications for learning dynamics research: it suggests that allocating more compute *within* each training step (via reasoning traces) may be an alternative or complement to simply increasing the number of training steps or model parameters.
- RPT's favorable scaling behavior positions it as a candidate for inclusion in future scaling law analyses, potentially adding a new dimension (RL pre-training compute vs. supervised pre-training compute) to existing Chinchilla-style frameworks.
- For safety and alignment, the use of rule-based, intrinsic rewards that are immune to reward hacking — derived from corpus ground truth rather than a learned reward model — demonstrates a design pattern that could inform more robust RLHF alternatives.

---

### Remaining Limitations & Next Steps
- The experiments are conducted on OmniMATH, a domain-specific dataset of competition-level math problems, rather than a general web-text corpus; this raises questions about whether the benefits of next-token reasoning transfer to diverse, noisy, non-mathematical text at true pre-training scale.
  - Authors acknowledge RPT as a "scalable" paradigm and present scaling curves, but the largest experiments reported are still bounded by the OmniMATH corpus size and the 14B base model — full web-scale validation is not demonstrated in this paper.
- The base model used (DeepSeek-R1-Distill-Qwen-14B) already possesses basic reasoning capabilities from distillation; it is unclear how much of RPT's benefit depends on this warm-start and whether the approach would work from a randomly initialized or standard pre-trained base.
- Token-level entropy filtering introduces a preprocessing dependency and hyperparameter (entropy threshold) whose sensitivity and optimal configuration are not fully chara

## Key Claims

1. Reinforcement Pre-Training (RPT) reframes next-token prediction as a reasoning task trained with reinforcement learning, using verifiable rewards derived directly from the pre-training corpus.
2. RPT transforms vast unannotated text data into a massive dataset for general-purpose RL without requiring external annotations or domain-specific reward functions.
3. RPT significantly improves the accuracy of next-token prediction.
4. RPT exhibits favorable scaling properties where next-token prediction performance consistently improves with increased training compute.
5. RPT provides a stronger pre-trained foundation for subsequent reinforcement fine-tuning, leading to better final task performance.
6. RPT enhances zero-shot performance on various downstream tasks.
7. Current RLHF applications rely on costly human preference data and learned reward models that are susceptible to reward hacking, limiting scalability.
8. RLVR is typically constrained by the scarcity of annotated data with verifiable answers, restricting its application to domain-specific fine-tuning rather than general-purpose pre-training.
9. RPT minimizes reward hacking risk by using direct, rule-based reward signals tied to the correctness of the predicted next token.
10. RPT promotes deeper understanding and generalization rather than rote memorization by encouraging next-token reasoning patterns.

## Capabilities

- RL can be scaled to unannotated web-text corpora for general-purpose pre-training by reframing next-token prediction as a reasoning task with intrinsic verifiable rewards derived from the corpus itself, without requiring domain-specific annotated Q&A pairs
- Using the ground-truth next token as a binary, rule-based verifiable reward signal for RL pre-training inherently minimises reward hacking compared to learned reward models
- RPT exhibits consistent compute scaling: increased training compute under the RPT framework monotonically improves next-token prediction accuracy, offering a new sustainable scaling axis alongside standard NTP
- Models pre-trained with RPT provide a stronger foundation for subsequent reinforcement fine-tuning, leading to better final task performance than standard NTP-pretrained models
- Token-level entropy filtering using a small proxy model (1.5B) efficiently identifies the subset of corpus positions that require non-trivial reasoning, enabling targeted RL training on hard-to-predict tokens

## Limitations

- Despite claiming to be a general-purpose pre-training paradigm scalable to the web-text corpus, RPT experiments are conducted exclusively on OmniMATH (4,428 math competition problems) — no validation on general web text is presented
- RPT requires a base model with pre-existing chain-of-thought reasoning capabilities; it is not demonstrated from a randomly initialised or standard NTP-pretrained model, raising questions about whether the benefits derive from RPT itself or the capable base
- On-policy rollout of G thinking trajectories per token position multiplies training compute by a large factor relative to standard NTP, making RPT vastly more expensive for equivalent corpus coverage
- Many tokens in any corpus are too easily predictable to benefit from reasoning; RPT must skip or filter these positions, meaning the approach covers only a subset of corpus content and cannot straightforwardly replace standard NTP
- The paper does not evaluate or compare RPT against alternative compute-equivalent approaches to scaling (e.g., synthetic data, self-play, longer standard RL fine-tuning), making it unclear whether the improvements are due to the RPT framing or simply more compute on math data
- RLHF and standard RLVR remain constrained to domain-specific fine-tuning because they depend on external annotated Q&A pairs with verifiable answers; RPT claims to address this but only validates on a single annotated math domain dataset
- RLHF relies on costly human preference data and learned reward models susceptible to reward hacking, fundamentally limiting scalability of alignment-oriented RL
- Downstream task evaluation of RPT models is asserted but not shown in the available text; zero-shot improvements are claimed without benchmark details, making the magnitude and breadth of gains difficult to assess

## Bottlenecks

- RL for LLM pre-training has been blocked by absence of scalable verifiable rewards over general unannotated text — RLVR only works where domain-specific labeled Q&A pairs exist, restricting RL benefits to narrow fine-tuning stages
- Compute cost of on-policy RL rollouts at pre-training scale: generating G reasoning trajectories per token position in a web-text corpus is prohibitively expensive without significant efficiency advances in inference and training infrastructure

## Breakthroughs

- Reinforcement Pre-Training (RPT) demonstrates that the entire unannotated text corpus can be converted into a general-purpose RL training signal by treating every next-token prediction as a reasoning problem with an intrinsic verifiable reward — breaking the prior constraint that RL for LLMs require

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/scaling_laws|scaling_laws]]

## Key Concepts

- [[entities/grpo|GRPO]]
- [[entities/omnimath|OmniMath]]
- [[entities/reinforcement-learning-with-verifiable-rewards-rlvr|Reinforcement Learning with Verifiable Rewards (RLVR)]]
- [[entities/reward-hacking|Reward Hacking]]
- [[entities/verl|verl]]
