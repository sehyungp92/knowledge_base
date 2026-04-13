---
type: source
title: The Unreasonable Effectiveness of Entropy Minimization in LLM Reasoning
source_id: 01KJTTJRKW5STTRMCED89QY35D
source_type: paper
authors:
- Shivam Agarwal
- Zimin Zhang
- Lifan Yuan
- Jiawei Han
- Hao Peng
published_at: '2025-05-21 00:00:00'
theme_ids:
- finetuning_and_distillation
- mathematical_and_formal_reasoning
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The Unreasonable Effectiveness of Entropy Minimization in LLM Reasoning

**Authors:** Shivam Agarwal, Zimin Zhang, Lifan Yuan, Jiawei Han, Hao Peng
**Published:** 2025-05-21 00:00:00
**Type:** paper

## Analysis

# The Unreasonable Effectiveness of Entropy Minimization in LLM Reasoning
2025-05-21 · paper · Shivam Agarwal, Zimin Zhang, Lifan Yuan, Jiawei Han, Hao Peng
https://arxiv.org/pdf/2505.15134

---

### Motivation & Prior Limitations
Post-training methods like GRPO and RLOO achieve strong reasoning performance but require large labeled datasets (60K examples with output verification), raising the question of how much improvement is attributable to algorithmic innovation versus the model's intrinsic pretrained capabilities.
- Prior supervised RL and SFT methods depend on output verification (e.g., answer extraction), which is non-trivial or inapplicable for complex tasks like scientific code generation where multiple plausible solutions exist and answer extraction is undefined.
- Inference-time scaling methods like self-consistency require O(Nn) forward passes and assume extractable outputs, while iterative refinement is bottlenecked by context length — both are compute-intensive and task-constrained.
- The contribution of pretrained model capability to post-training gains is systematically underappreciated; without an unsupervised baseline, it is difficult to attribute observed improvements to the training algorithm itself.

---

### Proposed Approach
The paper proposes entropy minimization (EM) as a standalone objective — without any labeled data, output verification, or reward models — covering three post-pretraining regimes: finetuning (EM-FT), reinforcement learning (EM-RL), and inference-time scaling (EM-INF).
- **EM-FT** directly minimizes token-level Shannon entropy over unlabeled outputs sampled from the model itself, mirroring the computational structure of supervised finetuning but replacing labeled targets with entropy of the model's own distribution.
- **EM-RL** uses negative entropy as the sole RL reward signal, in two variants: trajectory-level (EM-RL-sequence, rewarding high joint sequence probability) and token-level (EM-RL-token, rewarding low per-step decisional entropy); a KL regularizer with β=0.001 prevents large deviation from the base policy without suppressing the entropy gradient.
- **EM-INF** treats output logits at each decoding step as free parameters and runs 5–15 gradient descent steps to minimize token-level entropy with a minimum entropy threshold δ ∈ (0.1, 0.5) to prevent collapse to greedy decoding; it requires only O(n) forward passes (identical to regular decoding) and never updates model weights.
- Unlike temperature scaling — which preserves logit rank order and merely sharpens the distribution — EM-INF logit optimization can reorder non-top logits under high-entropy conditions, enabling qualitatively different token selections in uncertain states (Proposition 1).
- The core hypothesis is that capable pretrained models assign higher probability to correct outputs, so concentrating probability mass on confident outputs reinforces correct pretraining priors without external supervision.

---

### Results & Capabilities
EM-RL on Qwen2.5-7B, trained on 60K unlabeled prompts, achieves comparable or better performance than GRPO and RLOO trained on 60K labeled examples across math and coding benchmarks.
- EM-RL-token scores 42.9% average math and 27.0% average coding versus GRPO's 42.1% math and 25.4% coding; it outperforms GRPO on AMC (57.8% vs 56.6%), Minerva (30.9% vs 25.0%), and LeetCode (29.5% vs 25.0%).
- EM-FT with N=1 (single sampled trajectory per prompt, 1× FLOPs) achieves 40.2% average math versus GRPO's 42.1% at 13.1× the FLOPs, demonstrating strong compute efficiency.

EM-INF enables Qwen2.5-32B-Instruct to outperform GPT-4o, Claude 3 Opus, and Gemini 1.5 Pro on the SciCode scientific coding benchmark while using 3× less compute than self-consistency or sequential refinement.
- On SciCode main problems with background knowledge, EM-INF with Qwen2.5-32B scores 10.7% versus GPT-4o's 9.2%, Claude 3.5 Sonnet's 12.3%, and the base Qwen2.5-32B's 4.6%.
- EM-INF outperforms adaptive temperature scaling on SciCode by approximately 3%, attributed to its ability to reorder non-top logits under high uncertainty, whereas temperature scaling only rescales without rank changes.
- On AMC, EM-INF achieves equivalent accuracy to self-consistency (N=4) while consuming roughly one-third of the wall-clock compute time.
- EM-INF improves over baseline by ~3% on average across math, coding, and physics tasks for Qwen models; on AIME it outperforms self-consistency by 4%, and on UGPhysics by 3.6%.

---

### Implications
Entropy minimization establishes a strong unsupervised baseline that should be included in all future evaluations of post-training and inference-time scaling algorithms, to properly separate algorithmic contribution from latent pretrained capability.
- Many pretrained LLMs already possess substantial reasoning capacity that is latent rather than absent; post-training methods may be largely eliciting this capacity rather than instilling new reasoning ability, which reframes how gains from RLHF and SFT should be interpreted.
- EM-RL's success without output verification opens a path for post-training on tasks where answer extraction is ill-defined (scientific coding, open-ended generation), removing a key bottleneck in applying RL to complex reasoning domains.
- EM-INF's parameter-free, task-agnostic nature makes it immediately deployable as an inference wrapper on existing models without retraining, offering a practical compute efficiency gain in production settings.
- The finding that EM fails on individualistic value alignment (where confidence does not proxy correctness) draws a principled boundary: EM is effective when model confidence and correctness are correlated, which holds for well-scoped reasoning tasks but not for pluralistic value reasoning or tasks with distribution shift from pretraining.

---

### Remaining Limitations & Next Steps
Entropy minimization's effectiveness is tightly conditioned on the pretrained model already possessing strong 

## Key Claims

1. Entropy minimization alone, without any labeled data, can substantially improve LLM performance on challenging math, physics, and coding tasks.
2. Many pretrained LLMs possess previously underappreciated reasoning capabilities that can be elicited through entropy minimization alone, without labeled data or parameter updates.
3. EM-RL without any labeled data achieves comparable or better performance than GRPO and RLOO trained on 60K labeled examples on Qwen-7B.
4. EM-INF enables Qwen-32B to match or exceed GPT-4o, Claude 3 Opus, and Gemini 1.5 Pro on the SciCode benchmark while being 3x more efficient than self-consistency and sequential refinement.
5. EM-FT improves performance over the base model by 8% on average on math and coding without using any labels.
6. EM-FT with N=1 trajectory sampled outperforms GRPO and RLOO (which use N=4 trajectories with output verification) on Minerva and LeetCode by 5% on average.
7. Unsupervised RL methods (SC-RL, EM-RL) improve base model performance by 11% on average and maintain competitive performance against output-verified GRPO and RLOO.
8. EM-RL improves model performance on LiveCode by 6% where direct entropy minimization (EM-FT) did not work, indicating that reward-based design can better enhance learning from unlabeled data.
9. EM-INF improves the performance of the base model for almost all tasks and model classes by 3% on average at inference time without updating parameters.
10. EM-INF requires only O(n) forward passes equivalent to regular decoding, whereas self-consistency and sequential refinement require O(Nn) forward passes.

## Capabilities

- Unsupervised finetuning via direct token-level entropy minimization (EM-FT) improves LLM performance on math and coding tasks by ~8% on average without any labeled data, achieving competitive or better results than supervised GRPO/RLOO on several benchmarks including LeetCode and Minerva
- RL with negative entropy as the sole reward signal (EM-RL), using no labeled data, achieves comparable or better performance than GRPO and RLOO trained on 60K labeled examples on math and coding benchmarks, with 11% average improvement over the base model
- Inference-time entropy minimization via logit optimization (EM-INF) improves reasoning performance without parameter updates, requiring only O(n) forward passes equivalent to regular decoding — achieving 3x better compute efficiency than self-consistency while outperforming it on high-uncertainty ta
- Qwen-32B with EM-INF logit optimization outperforms GPT-4o, Claude 3 Opus, and Gemini 1.5 Pro on the SciCode scientific coding benchmark without any parameter updates, training data, or multi-sample inference

## Limitations

- Entropy minimization is entirely ineffective for tasks where model confidence does not correlate with output quality — individualistic value reasoning shows zero improvement under all three EM variants, and the paper explicitly rules out EM for human preference alignment
- EM improvements are critically contingent on the base model already possessing the target reasoning capability from pretraining — models lacking sufficient initial reasoning behaviours (Llama-3.1-8B on math) see minimal gain or are actively harmed by entropy minimization
- Entropy minimization provides no improvement on tasks significantly out-of-distribution from the pretraining mixture — EM-FT shows zero gains on LiveCodeBench because it is continuously updated with novel problems outside pretraining coverage
- Entropy minimization can actively hurt performance on weaker base models — EM-FT and EM-RL sometimes decrease accuracy for Llama-3.1-8B on math tasks, constituting a hard performance cliff that reverses the gains seen on stronger models
- Self-consistency as an inference-time scaling method is inapplicable to code generation and scientific coding tasks where final answer extraction is non-trivial or impossible, creating a systematic coverage gap for the most challenging reasoning domains
- Iterative refinement for sequential inference-time scaling is hard-bounded by the model's maximum context length, preventing effective refinement of long reasoning chains on complex tasks — and actually degrades performance on SciCode
- EM-INF requires empirical tuning of a minimum entropy threshold δ to prevent collapse to greedy decoding — the effective range (0.1 < δ < 0.5) is determined heuristically rather than analytically, and optimal α for adaptive temperature is similarly task-dependent
- Standalone entropy maximization as a training objective is unstable and causes policy collapse, constraining the entropy-based training design space to minimization only — the asymmetry between stable minimization and unstable maximization is unexplained
- LLMs are systematically biased toward coarse majority values from pretraining, causing high model confidence to be unreliable as a quality signal for tasks requiring pluralistic or individual-specific value reasoning — a fundamental miscalibration not addressable by EM

## Bottlenecks

- Confidence-correctness calibration gap in pretrained LLMs limits the generality of all unsupervised confidence-based improvement methods — entropy minimization, self-consistency, and frequency-based reward estimation only work when model confidence reliably tracks correctness, which holds for in-dis

## Breakthroughs

- LLM reasoning performance can be substantially improved through entropy minimization alone — without labeled data, verifiable rewards, or external supervision — by exploiting latent reasoning capability already present in pretrained models, matching or beating supervised RL on 60K labeled examples
- Inference-time logit gradient descent (EM-INF) enables a 32B open-weight model to match or exceed GPT-4o, Claude 3 Opus, and Gemini 1.5 Pro on scientific coding (SciCode) at 3x better compute efficiency than self-consistency, with no parameter updates and single-trajectory generation

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/amc|AMC]]
- [[entities/grpo|GRPO]]
- [[entities/llama-31-8b|Llama-3.1-8B]]
- [[entities/minerva|Minerva]]
- [[entities/qwen25|Qwen2.5]]
- [[entities/rloo|RLOO]]
