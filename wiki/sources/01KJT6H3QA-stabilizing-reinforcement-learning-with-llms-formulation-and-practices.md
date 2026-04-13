---
type: source
title: 'Stabilizing Reinforcement Learning with LLMs: Formulation and Practices'
source_id: 01KJT6H3QAXK80C0930JASQBPF
source_type: paper
authors:
- Chujie Zheng
- Kai Dang
- Bowen Yu
- Mingze Li
- Huiqiang Jiang
- Junrong Lin
- Yuqiong Liu
- Hao Lin
- Chencan Wu
- Feng Hu
- An Yang
- Jingren Zhou
- Junyang Lin
published_at: '2025-12-01 00:00:00'
theme_ids:
- adaptive_computation
- model_architecture
- policy_optimization
- reinforcement_learning
- rl_theory_and_dynamics
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 18
tags: []
---
# Stabilizing Reinforcement Learning with LLMs: Formulation and Practices

**Authors:** Chujie Zheng, Kai Dang, Bowen Yu, Mingze Li, Huiqiang Jiang, Junrong Lin, Yuqiong Liu, Hao Lin, Chencan Wu, Feng Hu, An Yang, Jingren Zhou, Junyang Lin
**Published:** 2025-12-01 00:00:00
**Type:** paper

## Analysis

# Stabilizing Reinforcement Learning with LLMs: Formulation and Practices
2025-12-01 00:00:00 · paper · Chujie Zheng, Kai Dang, Bowen Yu, Mingze Li, Huiqiang Jiang et al. (13 total)
https://arxiv.org/pdf/2512.01374

---

### Motivation & Prior Limitations
- Mainstream RL algorithms for LLMs (REINFORCE, GRPO) optimize token-level objectives while rewards are assigned at the sequence level, and no principled justification existed for why this mismatch should be acceptable or under what conditions it could be tolerated.
  - Prior work proposed ad hoc fixes (length normalization, various clipping strategies) without a theoretical grounding linking those choices to training stability.
  - For Mixture-of-Experts (MoE) models specifically, the dynamic expert routing mechanism further invalidates token-level importance sampling ratios, creating a compounded instability problem that prior work only partially addressed (Zheng et al., 2025) without formal explanation.
- Training instability in large-scale RL with LLMs is a known scaling bottleneck: collapse events — characterized by sharp entropy drops and training-inference KL spikes — can derail long training runs and negate expensive compute investments.
  - No prior work had systematically identified the joint conditions (training–inference discrepancy and policy staleness) that must both be controlled to avoid collapse, nor validated these conditions at the scale of hundreds of thousands of GPU hours.

---

### Proposed Approach
- The paper proposes a novel formulation showing that the token-level RL objective is a first-order Taylor approximation to the true sequence-level reward objective, and that this approximation is valid if and only if two quantities are jointly minimized: the training–inference discrepancy (numerical differences between training and inference engines) and policy staleness (divergence between the rollout policy and the policy being optimized).
  - The derivation proceeds by writing the sequence-level importance sampling weight as a product of per-token ratios, then applying a first-order expansion that collapses the product to a sum — yielding the token-level objective — under the condition that each per-token ratio is close to 1.
  - The IS weight, PPO-style clipping, and Routing Replay are all shown to be consequences of this same approximation condition rather than independent heuristics: IS corrects for training–inference discrepancy, clipping limits policy staleness, and Routing Replay reduces both for MoE models by fixing expert routing decisions during gradient updates.
- Two concrete variants of Routing Replay are formalized: Vanilla Routing Replay (R2), which replays the experts selected by the rollout policy in the training engine and primarily reduces policy staleness; and Rollout Routing Replay (R3), which replays the experts selected in the inference engine and reduces both training–inference discrepancy and policy staleness simultaneously.
  - The paper notes that R2 leaves the target policy unaltered on the first mini-batch while R3 introduces bias from the start, predicting and empirically confirming that R2 is preferable at low off-policiness and R3 at high off-policiness.
- The minimalist baseline algorithm MiniRL is introduced as the cleanest instantiation of the formulation: REINFORCE with token-level IS correction, group-normalized advantage, and decoupled PPO clipping — with no length normalization, preserving exact alignment with the first-order approximation.

---

### Results & Capabilities
- In on-policy training with a 30B MoE model (Qwen3-30B-A3B-Base cold-start, FP8 inference, BF16 training), MiniRL with IS correction achieves the highest benchmark score and training stability on HMMT25, AIME25, and AIME24 (90 competition math problems total, scored as average accuracy over 32 samples).
  - Removing the training–inference IS correction causes immediate training collapse and a sharp entropy drop, confirming that the IS weight is structurally necessary rather than optional.
  - Adding length normalization degrades benchmark performance without causing collapse, consistent with it biasing the token-level objective away from the sequence-level reward without fully breaking the approximation.
- In off-policy training (mini-batch size fixed at 1,024; global batch size varied to 2,048, 4,096, and 8,192 corresponding to N=2, 4, 8 gradient updates per rollout), both Routing Replay and clipping are necessary for stable training; omitting either causes premature collapse.
  - At low off-policiness (gbs = 2×mbs), R2 outperforms R3. At higher off-policiness (gbs = 4×mbs and 8×mbs), R3 surpasses R2 and R2 fails to sustain stable training, with R2's peak performance before collapse slightly lower than R3's final performance.
- Models initialized from three different cold-start datasets — distilled from Qwen3-Max-Thinking-Preview, DeepSeek-R1-0528, and gpt-oss-120b (high mode) — converge to comparable final benchmark scores (AIME25 & AIME24) given a stable RL recipe with sufficient training steps, despite notable early divergence in trajectory and response length.
  - This result suggests that cold-start initialization differences are transient and that stable RL training is the decisive variable for final capability, motivating researchers to invest in RL recipe quality over cold-start data curation.

---

### Implications
- The formulation provides a principled unifying explanation for a collection of previously empirical stabilization techniques, which should accelerate the design of new RL algorithms for LLMs by giving practitioners a diagnostic lens (minimize training–inference discrepancy and policy staleness) rather than a trial-and-error checklist.
- The finding that cold-start initialization does not determine final performance — given sufficient stable RL — shifts the scaling strategy for post-training: compute should be directed toward longer, more stable RL runs rather than ever-more-expensive c

## Key Claims

1. The token-level optimization objective used in policy gradient methods like REINFORCE can be viewed as a first-order approximation to the true expected sequence-level reward.
2. Importance sampling correction for the training-inference discrepancy is an inherent component of the valid token-level objective, and omitting it causes rapid training collapse.
3. For on-policy training, the basic policy gradient algorithm with importance sampling correction achieves the highest training stability.
4. Expert routing in Mixture-of-Experts models amplifies both training-inference discrepancy and policy staleness, making the first-order approximation more likely to break down.
5. Routing Replay reduces training-inference discrepancy and policy staleness in MoE models, but introduces bias into the optimization objective by constraining routed experts.
6. When off-policy updates are introduced, combining clipping and Routing Replay is essential to mitigate training instability caused by policy staleness.
7. Vanilla Routing Replay (R2) outperforms Rollout Routing Replay (R3) at low off-policiness, while R3 surpasses R2 and is necessary at high off-policiness.
8. Models initialized with different cold-start data consistently achieve comparable final performance when trained with a stable RL recipe, indicating cold-start differences vanish with prolonged RL tra
9. It is inherently difficult to devise general and scalable approaches to obtaining reliable value models, making value-based RL methods like PPO hard to apply at scale.
10. The sequence-level importance sampling gradient is intractable due to the large numerical range and high variance of sequence likelihood.

## Capabilities

- Stable RL training of 30B MoE language models demonstrated over hundreds of thousands of GPU hours via importance sampling correction, PPO-style clipping, and Routing Replay — achieving consistent benchmark improvement without collapse
- Routing Replay (R2/R3) stabilises RL training for MoE models by fixing expert routing during policy optimisation gradient updates, restoring the validity of token-level policy gradient objectives that MoE routing would otherwise break
- Off-policy RL training with up to 8x batch/mini-batch ratio achieves stable convergence for MoE LLMs when combining PPO-style clipping with Routing Replay, enabling higher compute utilisation without training collapse
- Cold-start initialisation is rendered irrelevant by stable RL training: models distilled from Qwen3-Max-Thinking, DeepSeek-R1-0528, and GPT-4 converge to statistically comparable benchmark scores under the same stable RL recipe

## Limitations

- Direct optimisation of sequence-level rewards is computationally intractable — the high variance and large numerical range of full-sequence likelihood ratios make exact gradient computation unusable, requiring biased token-level surrogates
- Value-based RL approaches (PPO with explicit value models) are practically unscalable for LLMs — the authors explicitly found it 'inherently difficult (if not impossible) to devise general and scalable approaches to obtaining reliable value models'
- MoE expert routing invalidates token-level importance sampling ratios — the dynamic expert selection mechanism entangles routing decisions with both training-inference discrepancy and policy staleness, breaking the first-order approximation that justifies token-level RL objectives
- Training-inference numerical discrepancy is an inherent, infrastructure-level instability source — different computational kernels in training (Megatron/FSDP) vs inference (SGLang/vLLM) engines produce divergent outputs for identical model weights and inputs
- Off-policy RL training stability degrades with higher off-policiness — R2 Routing Replay fails to sustain training at batch/mini-batch ratios of 4x and 8x, requiring the more aggressive R3 variant which itself introduces greater optimisation bias
- Routing Replay introduces systematic optimisation bias as an unavoidable side effect of stabilisation — constraining expert routing to stale decisions causes the actual optimised policy to deviate from the intended target policy
- Length normalisation in RL objectives is theoretically harmful — widely used in GRPO and similar algorithms, it invalidates the first-order approximation to sequence-level reward and produces systematically biased gradients regardless of whether training remains numerically stable
- Omitting training-inference IS correction causes rapid, catastrophic training collapse — the importance sampling weight for the training-inference discrepancy is structurally required, not optional; its omission causes entropy collapse within hundreds of steps
- FP8 inference with BF16 training creates severe training-inference discrepancy that breaks algorithms validated only under matched precision — many existing RL recipes fail under this production-realistic precision mismatch
- On-policy RL compute scaling is hard-bounded by generation length — the rollout phase cannot be parallelised to leverage additional GPUs, creating a throughput ceiling that forces use of stability-degrading off-policy updates for production-scale training
- All empirical validation is limited to mathematical reasoning with binary rewards using a single MoE architecture — the stabilisation recipes' generalisability to open-ended tasks, continuous rewards, dense model architectures, or non-math domains is entirely unvalidated
- Achieving initialisation-independent RL convergence requires prolonged training — while cold-start differences eventually vanish, this requires sufficient gradient steps (hundreds to thousands) at 5–6 GPU hours each, implying very high total compute requirements

## Bottlenecks

- MoE expert routing creates fundamental algorithmic incompatibility with standard token-level policy gradient RL — dynamic expert selection during training vs inference introduces compounding numerical divergence that causes GRPO/REINFORCE to collapse without architectural workarounds
- Infrastructure-level training-inference numerical discrepancy is an unavoidable engineering bottleneck for production RL pipelines — separate throughput-optimised kernels in training (Megatron/FSDP) and inference (SGLang/vLLM) engines produce inherently different probability estimates that bias all 

## Breakthroughs

- First principled theoretical justification that token-level RL objectives are a valid first-order Taylor approximation to sequence-level rewards — identifying precisely that the approximation holds only when training-inference discrepancy and policy staleness are jointly minimised
- Empirical demonstration that cold-start initialisation source is irrelevant to final RL performance under stable training — models initialised from three different frontier distillation sources converge to statistically comparable benchmark scores, reorienting the field away from initialisation engi

## Themes

- [[themes/adaptive_computation|adaptive_computation]]
- [[themes/model_architecture|model_architecture]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]

## Key Concepts

- [[entities/cold-start-initialization|Cold-Start Initialization]]
- [[entities/grpo|GRPO]]
