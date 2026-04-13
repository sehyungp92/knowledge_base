---
type: source
title: 'DiffuCoder: Understanding and Improving Masked Diffusion Models for Code Generation'
source_id: 01KJTPC0T74FVTRCTH3Q6YM2XC
source_type: paper
authors:
- Shansan Gong
- Ruixiang Zhang
- Huangjie Zheng
- Jiatao Gu
- Navdeep Jaitly
- Lingpeng Kong
- Yizhe Zhang
published_at: '2025-06-25 00:00:00'
theme_ids:
- code_and_software_ai
- code_generation
- model_architecture
- policy_optimization
- reinforcement_learning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# DiffuCoder: Understanding and Improving Masked Diffusion Models for Code Generation

**Authors:** Shansan Gong, Ruixiang Zhang, Huangjie Zheng, Jiatao Gu, Navdeep Jaitly, Lingpeng Kong, Yizhe Zhang
**Published:** 2025-06-25 00:00:00
**Type:** paper

## Analysis

# DiffuCoder: Understanding and Improving Masked Diffusion Models for Code Generation
2025-06-25 · paper · Shansan Gong, Ruixiang Zhang, Huangjie Zheng, Jiatao Gu, Navdeep Jaitly et al. (7 total)
https://arxiv.org/pdf/2506.20639

---

### Motivation & Prior Limitations
Masked diffusion LLMs (dLLMs) have shown potential as autoregressive (AR) alternatives by operating over entire sequences and enabling global planning, properties that intuitively align with code generation's non-sequential, iterative refinement nature — but their training and inference mechanisms for coding tasks remain under-explored and poorly understood.
- Existing post-training methods for dLLMs either produce marginal gains or rely on semi-AR (block) decoding, which undermines the global planning that is diffusion's primary advantage over AR models.
  - LLaDA1.5 with DPO and d1/MMaDA with GRPO both fall into this category; d1 in particular masks all condition tokens to increase diversity, which the authors show destabilizes code training because code demands higher token-level accuracy than math.
- Instruction tuning yields far smaller gains for dLLMs than for AR models: DiffuCoder-Instruct improves only +1.1% average over its base on the reported benchmarks, compared to +9.1% for Qwen2.5-Coder+SFT on the same data, motivating RL-based post-training specific to diffusion.
- A fundamental gap exists in understanding how dLLMs actually decode: whether their generation is truly non-autoregressive or merely approximating AR generation, and how temperature, data modality, and training stage affect decoding order.

---

### Proposed Approach
The paper introduces DiffuCoder, a 7B masked diffusion model for code, as a testbed, and makes two interrelated contributions: a framework of AR-ness metrics for analyzing dLLM decoding behavior, and coupled-GRPO, a diffusion-native reinforcement learning algorithm that exploits the non-autoregressive properties of dLLMs without resorting to semi-AR decoding.

- **AR-ness metrics** quantify how closely a dLLM's unmasking schedule resembles left-to-right AR generation using two complementary measures: local AR-ness (fraction of decoding steps where newly unmasked tokens form consecutive next-token spans) and global AR-ness (fraction of steps where the model unmasks one of the earliest remaining masked positions).
  - These metrics reveal an "entropy sink" phenomenon: in the first diffusion step, tokens immediately to the right of the prompt prefix receive disproportionately high confidence, creating a causal bias even in diffusion models — analogous to attention sinks in AR models.
  - Analysis shows that dLLMs adapted from AR models (Dream, DiffuCoder) inherit stronger AR-ness than those trained from scratch (LLaDA), and that code generation exhibits lower mean and higher variance in global AR-ness than math, consistent with code's non-sequential structure.
  - Increasing sampling temperature from 0.2 to 1.2 simultaneously diversifies token choices *and* generation order — a property unique to dLLMs, since in AR models temperature only affects token selection.

- **Coupled-GRPO** addresses the high variance of Monte Carlo log-likelihood estimation in GRPO for dLLMs by using paired complementary mask noise: for each completion sequence, two masks are sampled such that their union covers all completion tokens exactly once, then their log-probabilities are averaged.
  - This is formally equivalent to applying Antithetic Variates variance reduction, which the authors prove theoretically in the appendix.
  - Unlike d1's full-mask-at-t=T baseline (which over-estimates probability for high-entropy early tokens due to the entropy sink), coupled-GRPO evaluates each token under a realistic partial-masking context, reducing bias and variance simultaneously.
  - Rollouts are generated at temperature 1.2 to exploit the rich generation-order diversity unique to dLLMs, and the method uses verifiable rewards (execution pass rate on test cases plus a code format reward) on 21K hard samples from AceCoder-87K.

- DiffuCoder itself is trained in four stages: adaptation pre-training from Qwen-2.5-Coder on 65B tokens of RefineCode/Stackv2, mid-training annealing on 16B tokens from OpenCoder, instruction tuning on 436K SFT samples, and coupled-GRPO post-training — with early stopping in Stage 1 at 65B tokens after finding that 700B-token training increased AR-ness and degraded performance.

---

### Results & Capabilities
Coupled-GRPO improves DiffuCoder-Instruct by +4.4% on EvalPlus (average of HumanEval+ and MBPP+) using only 21K training samples, closing a significant portion of the gap between dLLMs and their AR counterparts after instruction tuning.

- On EvalPlus, DiffuCoder + coupled-GRPO scores 68.3% (HumanEval+) and 67.5% (MBPP+), versus 65.2% and 61.9% for DiffuCoder-Instruct without RL — a net gain of +3.1% and +5.6% respectively.
  - For comparison, Qwen2.5-Coder+SFT with standard GRPO shows a −2.4% regression on HumanEval, illustrating that coupled-GRPO is more stable than vanilla GRPO even for AR models on this task.
- DiffuCoder base (after Stages 1–2) achieves performance on par with Qwen2.5-Coder-7B and OpenCoder-8B on coding benchmarks, establishing it as a competitive open-source dLLM for code.
- After coupled-GRPO training, the model's global AR-ness decreases, and when decoding steps are halved (2× speedup), the performance drop is smaller than for the instruct model without RL — suggesting that RL training reduces reliance on AR-ordered generation and increases effective parallelism.
- Temperature 1.2 during rollout is critical: pass@10 at temperature 1.2 substantially exceeds pass@10 at 0.2 for both base and instruct models, confirming that dLLMs have latent capability that diverse generation order can expose — the key prerequisite for effective RL.
- Post-RL training, the optimal *evaluation* temperature shifts from 0.2 to 0.3–0.4, consistent with findings in AR LLMs that RL sharpens 

## Key Claims

1. DiffuCoder is a 7B masked diffusion model trained on 130B tokens of code that achieves performance competitive with AR code models.
2. coupled-GRPO improves DiffuCoder's performance on code generation benchmarks by +4.4% on EvalPlus using only 21K training samples.
3. In dLLMs, increasing sampling temperature diversifies not only token choices but also the order in which tokens are generated, unlike AR models where temperature only affects token selection.
4. All current dLLMs show only marginal improvement over their base models after instruction tuning, compared to the large improvements seen in AR models on the same data.
5. Existing RL post-training approaches for dLLMs (d1, MMaDA) rely heavily on semi-AR block decoding, which deviates from the global non-autoregressive nature of diffusion models.
6. dLLMs exhibit an entropy sink phenomenon during conditional generation, where the confidence score distribution shows an 'L'-shaped pattern biased toward tokens immediately to the right of the given p
7. The entropy sink phenomenon causes a strong causal bias during conditional generation using low-confidence remasking decoding in dLLMs.
8. Adapted dLLMs (those initialized from pretrained AR LLMs) exhibit stronger AR-ness during generation than dLLMs trained from scratch, due to inherited left-to-right token dependencies.
9. Code generation by dLLMs has lower mean and higher variance in global AR-ness compared to math generation, suggesting that models plan token generation more globally for code tasks.
10. During instruction tuning, dLLMs first exhibit a high causal bias in the first epoch, but AR-ness declines as more data is seen, implying the model captures dependencies beyond pure AR order.

## Capabilities

- Masked diffusion LLMs at 7B scale achieve performance on par with autoregressive code models (Qwen2.5-Coder, OpenCoder) on code generation benchmarks after pre-training on 130B code tokens
- Commercial-scale diffusion LLMs (Mercury, Gemini Diffusion) achieve code generation performance rivaling top autoregressive models at ~90% HumanEval, demonstrating production viability
- Coupled-GRPO: a diffusion-native RL training algorithm that improves dLLM code generation by +4.4% on EvalPlus using complementary mask noise, without relying on semi-autoregressive decoding
- In diffusion LLMs, increasing sampling temperature diversifies not only token choices but also token generation order, creating a richer search space for RL rollouts — a capability absent in autoregressive models
- Diffusion LLMs exhibit data-modality-specific global generation order: code generation produces lower global AR-ness with higher variance, reflecting non-sequential back-and-forth refinement analogous to human programmers
- RL post-training via coupled-GRPO reduces performance degradation when halving diffusion decoding steps, enabling a 2× generation speedup with smaller accuracy loss

## Limitations

- Diffusion LLMs show only marginal improvement after instruction tuning (SFT), in stark contrast to autoregressive models which achieve large gains — DiffuCoder-Instruct gains only +1.1 avg vs Qwen2.5-Coder+SFT gaining +9.1 avg on identical data
- Entropy sink phenomenon: diffusion LLMs are systematically biased toward generating tokens immediately to the right of the input prefix during the first decoding step, creating an inescapable causal bias that limits true parallel non-AR generation
- Monte Carlo sampling for token log-probability estimation in diffusion RL training introduces high variance, creating significant computational overhead and making direct GRPO application unstable
- Prior RL methods for diffusion LLMs rely on semi-autoregressive (block) decoding during rollout, which contradicts and partially cancels the global planning advantage of diffusion models
- Pre-training code data quality creates an early-stopping ceiling: extending Stage 1 pre-training from 65B to 700B tokens actually degrades downstream performance, indicating the corpus contains significant noise
- Adapting diffusion LLMs from pre-trained AR models (as done with Qwen-2.5-Coder base) inherits stronger causal bias, limiting non-AR generation capabilities relative to models trained from scratch
- All evaluations restricted to Python-only benchmarks (HumanEval, MBPP, EvalPlus, BigCodeBench), with no evidence of multilingual code generation capability or performance on real-world multi-file engineering tasks
- Large capability gap persists between open-source 7B diffusion LLMs and commercial diffusion code models: DiffuCoder+coupled-GRPO achieves 73.2% HumanEval vs Mercury/Gemini Diffusion at ~90%, suggesting scale or proprietary training data are dominant factors
- Coupled-GRPO training shows inconsistent gains: BigCodeBench Hard subset drops from 12.2 to 10.8 (−1.4), and the LOO variant causes regression on HumanEval (−1.3/−3.0), revealing that RL gains are benchmark-dependent and not uniformly reliable
- RL training for diffusion LLMs requires substantial compute (8–10 nodes × 8 H100 GPUs) and depends on verifiable test cases, restricting applicability to executable code tasks with ground-truth checkers
- Instruction tuning (Stage 3) causes AR-ness to spike sharply on the first epoch before gradually decreasing — revealing that standard SFT training actively degrades the non-AR generation patterns learned during pre-training

## Bottlenecks

- Instruction tuning SFT produces large gains in AR models but only marginal gains in diffusion LLMs — the standard SFT recipe is architecturally mismatched to diffusion models, blocking post-training alignment for dLLMs
- Entropy sink in masked diffusion creates a structural AR bias: the model's confidence distribution is skewed toward leftmost positions, forcing near-sequential unmasking regardless of temperature and preventing full exploitation of parallel non-AR generation
- High-variance Monte Carlo log-probability estimation in masked diffusion creates unstable policy gradients, blocking scalable RL post-training for diffusion LLMs without architectural modifications to sampling

## Breakthroughs

- Coupled-GRPO: first RL algorithm for masked diffusion LLMs that achieves meaningful benchmark gains (+4.4% EvalPlus) without relying on semi-autoregressive decoding, by using complementary mask noise pairs to reduce variance in log-probability estimation
- Empirical discovery of the entropy sink phenomenon in masked diffusion LLMs: a structural L-shaped confidence distribution that forces near-sequential unmasking, providing the first mechanistic explanation for why dLLMs exhibit near-AR behavior despite their parallel architecture

## Themes

- [[themes/code_and_software_ai|code_and_software_ai]]
- [[themes/code_generation|code_generation]]
- [[themes/model_architecture|model_architecture]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/transformer_alternatives|transformer_alternatives]]

## Key Concepts

- [[entities/bigcodebench|BigCodeBench]]
- [[entities/grpo|GRPO]]
- [[entities/llada|LLaDA]]
- [[entities/rlvr|RLVR]]
- [[entities/passk|pass@k]]
