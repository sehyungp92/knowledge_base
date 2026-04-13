---
type: source
title: Model Merging in Pre-training of Large Language Models
source_id: 01KJTT48H0KBMW31VGJSGKCRMR
source_type: paper
authors:
- Yunshui Li
- Yiyuan Ma
- Shen Yan
- Chaoyi Zhang
- Jing Liu
- Jianqiao Lu
- Ziwen Xu
- Mengzhao Chen
- Minrui Wang
- Shiyi Zhan
- Jin Ma
- Xunhao Lai
- Deyi Liu
- Yao Luo
- Xingyan Bin
- Hongbin Ren
- Mingji Han
- Wenhao Hao
- Bairen Yi
- LingJun Liu
- Bole Ma
- Xiaoying Jia
- Xun Zhou
- Siyuan Qiao
- Liang Xiang
- Yonghui Wu
published_at: '2025-05-17 00:00:00'
theme_ids:
- adaptive_computation
- finetuning_and_distillation
- model_architecture
- post_training_methods
- pretraining_and_scaling
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Model Merging in Pre-training of Large Language Models

**Authors:** Yunshui Li, Yiyuan Ma, Shen Yan, Chaoyi Zhang, Jing Liu, Jianqiao Lu, Ziwen Xu, Mengzhao Chen, Minrui Wang, Shiyi Zhan, Jin Ma, Xunhao Lai, Deyi Liu, Yao Luo, Xingyan Bin, Hongbin Ren, Mingji Han, Wenhao Hao, Bairen Yi, LingJun Liu, Bole Ma, Xiaoying Jia, Xun Zhou, Siyuan Qiao, Liang Xiang, Yonghui Wu
**Published:** 2025-05-17 00:00:00
**Type:** paper

## Analysis

# Model Merging in Pre-training of Large Language Models
2025-05-17 · paper · Yunshui Li, Yiyuan Ma, Shen Yan, Chaoyi Zhang, Jing Liu et al. (26 total)
https://arxiv.org/pdf/2505.12082

---

### Motivation & Prior Limitations
- Model merging during post-training is well-studied, but its application during large-scale pre-training remains almost entirely unexplored, leaving substantial efficiency gains on the table for the community building foundation models.
  - DeepSeek V3 and LLaMA 3.1 both acknowledge using model merging during pre-training, but neither has disclosed their methodology, creating an information gap for open-source practitioners.
  - Prior pre-training merging work (e.g., LAWA) focused narrowly on training acceleration and was not evaluated at modern scales (100B+ parameters); independent researchers face a further barrier of limited access to intermediate checkpoints from large-scale runs.
- Predicting annealing performance during the constant learning rate phase of the WSD schedule requires actually running the expensive cosine decay, making rapid validation cycles and hyperparameter search computationally prohibitive.
  - There is no reliable, low-cost proxy for the final annealed model quality short of completing the full decay, which consumes significant compute for each configuration being evaluated.
- Large-scale LLM training is susceptible to irrecoverable loss spikes and GradNorm explosions, and the standard recovery option — retraining from scratch — wastes enormous computational resources with no systematic mitigation strategy.

---

### Proposed Approach
- The paper introduces **Pre-trained Model Averaging (PMA)**, a framework for merging sequential checkpoints sampled along the stable (constant learning rate) phase of the WSD training schedule to produce a single averaged model, evaluated across both Dense and MoE architectures from 411M to 200B total parameters.
  - Unlike post-training merging methods (Task Arithmetic, DARE, TIES-Merging) that combine independently fine-tuned models, PMA operates on checkpoints from a single training trajectory, exploiting the temporal diversity within the stable phase rather than task-specific weight divergence.
  - Three weighting schemes are compared — Simple Moving Average (SMA, uniform weights), Weighted Moving Average (WMA, linearly increasing weights toward recency), and Exponential Moving Average (EMA, exponentially decaying weights) — with merged model computed as $M_{avg} = \sum_{i=1}^{N} w_i M_i$, where checkpoints are spaced by a token-interval $V$ forming an arithmetic sequence.
- A secondary technique, **PMA-init**, repurposes PMA-merged weights as initialization for downstream continued training (CT) or supervised fine-tuning (SFT) stages, rather than for inference directly.
  - PMA-init exploits the observation that averaged weights produce smoother gradient norm curves at the start of new training phases, providing a stabilization mechanism without requiring any changes to the downstream training recipe.
  - For training recovery, PMA-init merges $N$ checkpoints saved immediately before a loss spike and resumes pre-training from that averaged point, avoiding full restarts.
- The theoretical grounding derives from a second-order Taylor expansion of the loss around an optimum, showing that merging improves over individual checkpoints when the off-diagonal Hessian cross-terms $\delta_i^T H \delta_j$ are predominantly negative — i.e., when checkpoint deviation vectors are complementary in the curvature geometry of the loss landscape.
  - Contour visualizations of MMLU score landscapes confirm this: individual checkpoint weight positions distribute along score contours with a complementary pattern, and their average lands in a higher-scoring region than most individuals.

---

### Results & Capabilities
- PMA applied during the stable training phase yields consistent performance improvements across all tested model sizes and architectures. On Humaneval, Seed-MoE-1.3B/13B improves from 31.1 to 36.6 and Seed-MoE-10B/100B improves from 54.3 to 61.6 after merging.
  - Gains are robust across BBH, MMLU, GSM8K, and HumanEval; larger models show smaller absolute gains on near-saturated benchmarks (e.g., BBH for the 20B/200B model) but improvements remain present.
- PMA applied early in the cosine annealing phase achieves performance **comparable to or exceeding** the fully annealed model, establishing it as a reliable low-cost simulator for final annealing quality.
  - In a controlled fork experiment on Seed-MoE-1.3B/13B at 1.4T tokens, constant-lr training with PMA significantly outperformed both the constant-lr baseline and the annealing run during early stages, converging to comparable final performance — demonstrating that the decay phase can effectively be simulated without executing it.
- Merging strategy differences matter early in training but converge as training stabilizes: at 204B tokens WMA outperforms SMA and EMA, but by 1,607B tokens differences become negligible (within ~0.3 points), justifying SMA as the practical default for its simplicity.
- The optimal merging interval $V$ exhibits a clear scaling relationship with model size: ~4B tokens for 0.7B/7B, ~8B tokens for 1.3B/13B, and ~80B tokens for 10B/100B models, consistent with larger models using larger batch sizes and requiring wider temporal diversity.
  - Increasing $N$ (number of merged checkpoints) from 3 to 15 improves final performance by ~1 point; N=10 is recommended as the practical optimum balancing cost and gain.
- PMA-init for CT consistently lowers loss at training onset and slightly improves early MMLU scores, though models converge to parity with the baseline by training end; it is robust across varied learning rate schedules, requiring no additional LR tuning.
- PMA-init successfully recovers pre-training from irrecoverable loss spikes on a 330M/3.3B MoE model trained at an intentionally high learning rate (6e-3), stabilizing the tr

## Key Claims

1. Merging checkpoints from the stable (constant learning rate) training phase produces consistent and significant performance improvements across different model sizes and architectures.
2. Applying PMA at the early stage of the cosine-decay annealing phase achieves comparable or even superior performance to models naturally annealed to completion.
3. Pre-training with a constant learning rate combined with model merging (PMA) can effectively match the performance of a fully annealed model at any point in the training process, without requiring lea
4. PMA enables accurate simulation of post-annealing model performance during the lengthy constant-learning-rate pre-training stage, enabling faster validation cycles and significant computational saving
5. Performance differences among SMA, WMA, and EMA merging strategies gradually become negligible as training advances toward completion.
6. In early training phases, WMA outperforms SMA and EMA because assigning higher weights to checkpoints with more training tokens produces superior models when model weights are still undergoing signifi
7. The optimal merging interval between checkpoints exhibits a clear scaling relationship with model size, with larger models requiring larger intervals.
8. Incorporating more checkpoints in the merging process consistently improves performance once training is completed, with N=15 achieving nearly 1 point higher overall performance than N=3.
9. Using PMA-merged weights as initialization (PMA-init) for continued training or SFT stages yields smoother GradNorm curves, improving training stability without harming final performance.
10. PMA-init can reliably recover training from irrecoverable loss spikes by merging checkpoints saved before the collapse and resuming from the merged checkpoint, avoiding the need to restart training fr

## Capabilities

- Averaging sequential pre-training checkpoints (PMA) from the stable constant-learning-rate phase yields consistent, significant benchmark performance improvements across MoE model scales from 1.3B/13B activated/total parameters up to 20B/200B
- PMA applied at the early stage of cosine-decay annealing achieves performance comparable to or exceeding fully annealed models, enabling accurate simulation of final model quality without completing the full annealing schedule
- Pre-training with a constant learning rate combined with PMA checkpoint merging matches the performance of a fully annealed model at any point in the training process, eliminating learning rate annealing as a required training step
- PMA-init — initializing continued training or SFT from averaged pre-training checkpoints — reliably recovers large-scale LLM training from irrecoverable loss spikes without retraining from scratch
- PMA-init produces smoother gradient norm curves when initializing downstream training stages (CT and SFT), reducing training instability and loss spike frequency without degrading final performance

## Limitations

- PMA provides negligible performance improvement when applied to models that have been tightly converged via low learning rate annealing — the technique requires geometric diversity among checkpoints to function and fails when checkpoints occupy a narrow basin
- PMA-init does not consistently improve SFT stage performance — gains are occasional and unreliable, limiting its utility as a systematic SFT enhancement strategy
- Direct empirical study of training instability and PMA-init recovery is infeasible at production large-model scales due to prohibitive cost — all instability recovery experiments use small proxy models (330M/3.3B) with artificially inflated learning rates, leaving generalization to 100B+ parameter t
- Performance gains from PMA are smaller and less consistent for larger models on benchmarks approaching saturation — improvements are bounded by available benchmark headroom, masking genuine capability improvements at the top of the scale range
- The specific model architectures, training datasets, and internal pre-training corpus used in all experiments are not publicly disclosed, preventing independent replication and external validation of PMA results
- At early training stages, using large merging intervals or merging too many checkpoints hurts performance by introducing unstable early weights — the technique requires training to be sufficiently advanced before it becomes beneficial, requiring careful timing
- PMA-based recovery from loss spikes requires that checkpoints were saved prior to the instability event — if checkpoint saving frequency is too low, the technique cannot be applied and the training run remains unrecoverable
- The optimal merging interval and number of checkpoints must be empirically determined per model size through ablation — there is no closed-form formula, only post-hoc heuristics that scale loosely with batch size conventions

## Bottlenecks

- Training instability — loss spikes and GradNorm explosions — in large-scale LLM pre-training is described as 'almost inevitable,' causing costly training restarts with no principled prevention mechanism, only reactive mitigations
- Long feedback loops during stable-phase pre-training: determining final model quality previously required committing to a complete annealing run, preventing rapid iteration on training recipes and architectural decisions during the most expensive phase of training

## Breakthroughs

- Checkpoint averaging (PMA) during stable constant-LR pre-training accurately predicts and replicates final annealed model performance without requiring actual annealing, fundamentally changing the economics of LLM validation by collapsing feedback loop length
- PMA-init provides a practical recovery mechanism for irrecoverable loss spikes in large-scale LLM training — averaging checkpoints saved before a collapse and resuming from the averaged weights reliably restores the training trajectory without full restart

## Themes

- [[themes/adaptive_computation|adaptive_computation]]
- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/model_architecture|model_architecture]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/scaling_laws|scaling_laws]]
