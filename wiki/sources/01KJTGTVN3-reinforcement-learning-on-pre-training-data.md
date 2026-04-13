---
type: source
title: Reinforcement Learning on Pre-Training Data
source_id: 01KJTGTVN37FWVW25Q995TQF4K
source_type: paper
authors:
- Siheng Li
- Kejiao Li
- Zenan Xu
- Guanhua Huang
- Evander Yang
- Kun Li
- Haoyuan Wu
- Jiajia Wu
- Zihao Zheng
- Chenchen Zhang
- Kun Shi
- Kyrierl Deng
- Qi Yi
- Ruibin Xiong
- Tingqiang Xu
- Yuhao Jiang
- Jianfeng Yan
- Yuyuan Zeng
- Guanghui Xu
- Jinbao Xue
- Zhijiang Xu
- Zheng Fang
- Shuai Li
- Qibin Liu
- Xiaoxue Li
- Zhuoyu Li
- Yangyu Tao
- Fei Gao
- Cheng Jiang
- Bo Chao Wang
- Kai Liu
- Jianchen Zhu
- Wai Lam
- Wayyt Wang
- Bo Zhou
- Di Wang
published_at: '2025-09-23 00:00:00'
theme_ids:
- chain_of_thought
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Reinforcement Learning on Pre-Training Data

**Authors:** Siheng Li, Kejiao Li, Zenan Xu, Guanhua Huang, Evander Yang, Kun Li, Haoyuan Wu, Jiajia Wu, Zihao Zheng, Chenchen Zhang, Kun Shi, Kyrierl Deng, Qi Yi, Ruibin Xiong, Tingqiang Xu, Yuhao Jiang, Jianfeng Yan, Yuyuan Zeng, Guanghui Xu, Jinbao Xue, Zhijiang Xu, Zheng Fang, Shuai Li, Qibin Liu, Xiaoxue Li, Zhuoyu Li, Yangyu Tao, Fei Gao, Cheng Jiang, Bo Chao Wang, Kai Liu, Jianchen Zhu, Wai Lam, Wayyt Wang, Bo Zhou, Di Wang
**Published:** 2025-09-23 00:00:00
**Type:** paper

## Analysis

# Reinforcement Learning on Pre-Training Data
2025-09-23 · paper · Siheng Li, Kejiao Li, Zenan Xu, Guanhua Huang, Evander Yang et al. (36 total)
https://arxiv.org/pdf/2509.19249

---

### Motivation & Prior Limitations
- Conventional training-time scaling for LLMs faces a fundamental bottleneck: compute is growing exponentially while the supply of high-quality text data grows only finitely, making data-based scaling increasingly untenable.
  - Training corpora have grown from billions of tokens (BERT) to trillions (Llama), but Villalobos et al. (2024), Muennighoff et al. (2023), and Ruan et al. (2025) document that high-quality web corpora are being exhausted.
  - Parameter scaling is similarly constrained: growing model size requires prohibitive infrastructure and inflates inference costs, as evidenced by the trillion-parameter scale of Kimi K2.

- Existing RL paradigms for LLMs — RLHF and RLVR — both depend on human annotation for reward construction, which prevents them from scaling to the full breadth of pre-training corpora.
  - RLHF relies on neural reward models trained on human-annotated preference pairs; RLVR relies on rule-based functions comparing outputs against reference answers, limiting applicable domains to those with verifiable ground truth.

- Supervised fine-tuning (SFT) under the standard next-token prediction (NTP) objective has been shown by Chu et al. (2025), Lai et al. (2025), and Shenfeld et al. (2025) to promote surface-level memorization rather than the deeper generalization achievable with RL, suggesting that the NTP training paradigm itself has generalization limitations independent of data quantity.

---

### Proposed Approach
- RLPT (Reinforcement Learning on Pre-Training data) is a training-time scaling paradigm that applies RL directly to large unlabeled pre-training corpora by replacing human-annotated rewards with a self-supervised next-segment reasoning objective.
  - Unlike RLHF and RLVR, RLPT requires no human labels; the ground-truth reward signal is derived entirely from the natural structure of pre-training text (the next segment in a document).
  - Unlike related work RPT (Dong et al., 2025) and Quiet-STaR (Zelikman et al., 2024), which also apply RL on unlabeled data but target next-token prediction, RLPT operates at the segment level, encouraging the model to generate intermediate reasoning chains before committing to a prediction.

- The core objective consists of two interleaved tasks. Autoregressive Segment Reasoning (ASR) trains the policy to predict the next sentence $s_i$ given preceding context $s_{<i}$, directly mirroring the autoregressive generation paradigm. Middle Segment Reasoning (MSR) trains the policy to predict a masked middle segment $s_i$ given both preceding context $s_{<i}$ and the following segment $s_{i+1}$, analogous to masked language modeling and particularly suited to code completion and bidirectional understanding.
  - Segments are sentence-level by default (using NLTK), with the model prompted to reason step-by-step before emitting its prediction within special tags; preliminary experiments with LLM-extracted atomic reasoning steps did not outperform sentence-level segmentation.

- Reward is computed by a generative reward model (Grm) that scores semantic consistency between the predicted and reference segments on a binary 0/1 scale, using a relaxed prefix reward: the prediction is accepted if it forms a valid semantic prefix of the reference completion, rather than requiring exact semantic match to a single sentence.
  - This relaxed prefix reward was adopted after a stricter exact-match reward failed, causing frequent false negatives when model outputs spanned multiple ground-truth segments due to uneven information density across sentence boundaries; the prefix reward stabilises training, enables longer responses, and improves downstream mathematical reasoning performance.

- Training uses on-policy GRPO without KL regularisation, with a cold-start SFT phase on instruction-following data to give the base model the minimum instruction-following capability required to perform next-segment reasoning.

---

### Results & Capabilities
- RLPT yields consistent, substantial improvements over cold-start SFT baselines across all benchmarks and three model families (Llama-3.2-3B-Base, Qwen3-4B-Base, Qwen3-8B-Base), demonstrating generality across model size and architecture.
  - On Qwen3-4B-Base, absolute gains over the cold-start baseline are: +3.0 MMLU, +5.1 MMLU-Pro, +8.1 GPQA-Diamond, +2.0 SuperGPQA, +6.0 KOR-Bench, spanning STEM, law, economics, and health domains.
  - On Llama-3.2-3B-Base, the most striking gain is +11.6 on GPQA-Diamond, indicating RLPT disproportionately improves hard scientific reasoning.

- On mathematical reasoning, RLPT applied to Qwen3-4B-Base improves Pass@1 by +6.6 on AIME24 and +5.3 on AIME25 over the cold-start baseline, and improves Pass@8 by +5.0 and +1.4 respectively, showing gains in both exploitation (Pass@1) and exploration (Pass@8).
  - When RLPT is used as the initialisation for subsequent RLVR training, Pass@1 improves by an additional +2.3 (AIME24) and +1.3 (AIME25) over RLVR trained from cold-start alone, and Pass@8 improves by +3.7 and +2.0, demonstrating that RLPT and RLVR are complementary rather than redundant.

- RLPT performance follows a power-law scaling relationship with training tokens across all evaluated benchmarks (MMLU, MMLU-Pro, GPQA-Diamond, SuperGPQA, MATH-500, AMC23, MinervaMath, AIME24, AIME25), empirically establishing a scaling law for this paradigm.
  - Fitted curves follow the form $y = a \cdot \exp(b \cdot x^c)$, with exponents that vary by benchmark difficulty; harder benchmarks like AIME show steeper gains (exponent ~0.77) relative to saturating benchmarks like MMLU (exponent ~0.03), suggesting RLPT's marginal value grows with task difficulty.

- Qualitative analysis of RLPT reasoning trajectories reveals structured multi-step patterns: the model abstrac

## Key Claims

1. The growing disparity between the exponential scaling of computational resources and the finite growth of high-quality text data constrains conventional scaling approaches for LLMs.
2. RLHF and RLVR rely on human annotation for reward construction, limiting their scalability on pre-training data.
3. RLPT derives reward signals directly from pre-training data, eliminating the dependency on human annotation.
4. When applied to Qwen3-4B-Base, RLPT yields absolute improvements of 3.0, 5.1, 8.1, 6.0, 6.6, and 5.3 on MMLU, MMLU-Pro, GPQA-Diamond, KOR-Bench, AIME24, and AIME25 respectively.
5. RLPT performance demonstrates favorable scaling behavior following a power-law with respect to training compute.
6. Training corpora for LLMs have grown from billions of tokens (BERT) to trillions of tokens (Llama), while model sizes have scaled from millions to the trillion-parameter level.
7. Parameter scaling requires increasingly demanding infrastructure and results in prohibitive inference costs; data scaling is constrained by the scarcity of high-quality web corpora.
8. RLPT enables reasoning for learning: rather than learning token by token, the model generates intermediate reasoning content that uncovers latent thought processes underlying data construction.
9. RL leverages self-explored trajectories for training, maintains proximity to the original policy distribution, and fosters stronger generalization capabilities compared to supervised learning.
10. RLPT uses two tasks: Autoregressive Segment Reasoning (ASR), which predicts the next sentence from preceding context, and Middle Segment Reasoning (MSR), which predicts a masked span using both preced

## Capabilities

- RLPT enables reinforcement learning to scale on unlabeled pre-training corpora by deriving self-supervised reward signals from next-segment prediction accuracy, removing all dependency on human annotation or verifiable ground-truth answers
- RLPT as initialization for RLVR yields cumulative improvements over RLVR alone: additional 2.3/1.3 Pass@1 and 3.7/2.0 Pass@8 gains on AIME24/AIME25, improving both exploitation and exploration simultaneously
- RLPT performance follows an empirical power-law scaling relationship with training compute tokens across diverse benchmarks, establishing a training-time RL scaling law analogous to pretraining scaling laws
- Interleaved ASR (autoregressive segment reasoning) and MSR (middle segment reasoning) RL training simultaneously improves forward autoregressive generation and bidirectional contextual in-filling in base LLMs within a single training run

## Limitations

- RLPT requires a cold-start supervised fine-tuning phase on instruction-following data before RL training can begin — base models lack sufficient instruction-following ability to engage in structured next-segment reasoning prompts
- Sentence-level segmentation is the default but may not be optimal; alternatives such as LLM-extracted atomic reasoning steps showed no improvement in preliminary studies, leaving the full segmentation design space unexplored
- Uneven information density across sentence segments (some containing only a formula, others a full solution) disrupts strict reward matching, requiring a relaxed prefix reward workaround that changes what the model is being rewarded for
- RLPT reward quality depends entirely on a generative reward model (GRM) for semantic consistency scoring, which is itself a learned model subject to its own hallucination, distributional bias, and inconsistent scoring
- All RLPT experiments are conducted on 3B–8B parameter base models; whether benefits transfer to frontier-scale models (70B+, MoE-scale) or to instruction-tuned models is entirely unvalidated
- All evaluation benchmarks are English-language (MMLU, GPQA, AIME, KOR-Bench, etc.); whether RLPT's gains extend to non-English languages or multilingual benchmarks is absent from the paper despite the training corpus including Chinese Wikipedia
- No comparison of RLPT compute efficiency against equivalent tokens spent on continued supervised pretraining; relative cost per benchmark-point improvement is unreported, making the efficiency case for RLPT over simple data scaling unproven
- MSR (middle segment reasoning) trains the model to fill masked spans using bidirectional context, but there is no analysis of whether this creates a training-inference distribution mismatch since LLMs generate autoregressively at inference time
- Scaling law curves for several benchmarks (MMLU, MATH-500, AMC23) show saturating or near-flat trends at higher token counts, suggesting diminishing returns for benchmarks where the model is already near ceiling
- Conventional LLM training-time scaling through data expansion is now fundamentally constrained by the exhaustion of high-quality web text, making continued capability improvements through the existing supervised pretraining paradigm increasingly difficult

## Bottlenecks

- Absence of scalable self-supervised reward signals for RL on general text confines RL-based capability improvement to narrow verifiable domains — RLPT's next-segment objective partially resolves this but reward quality is bounded by the precision of the generative reward model used for semantic cons
- Optimal segmentation granularity for segment-level RL objectives is empirically unsolved — sentence-level segmentation is used by default but preliminary studies with finer-grained alternatives (LLM-extracted atomic steps) showed no improvement, blocking maximally efficient use of RLPT across code, 

## Breakthroughs

- RLPT demonstrates that RL training can be scaled on unlimited unlabeled text by using next-segment prediction as a self-supervised reward signal, decoupling RL capability improvement from human annotation and verifiable domain constraints for the first time at training time

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/scaling_laws|scaling_laws]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/cold-start-phase|Cold-Start Phase]]
- [[entities/grpo-group-relative-policy-optimization|GRPO (Group Relative Policy Optimization)]]
- [[entities/mmlu|MMLU]]
- [[entities/minerva-math|Minerva Math]]
- [[entities/olympiadbench|OlympiadBench]]
- [[entities/reinforcement-learning-from-human-feedback-rlhf|Reinforcement Learning from Human Feedback (RLHF)]]
- [[entities/reinforcement-learning-with-verifiable-rewards-rlvr|Reinforcement Learning with Verifiable Rewards (RLVR)]]
- [[entities/test-time-scaling|Test-time Scaling]]
- [[entities/passk|pass@k]]
