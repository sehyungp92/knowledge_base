---
type: source
title: 'GenARM: Reward Guided Generation with Autoregressive Reward Model for Test-time
  Alignment'
source_id: 01KJV4TENFJVB1SFDHWQ7S13DB
source_type: paper
authors:
- Yuancheng Xu
- Udari Madhushani Sehwag
- Alec Koppel
- Sicheng Zhu
- Bang An
- Furong Huang
- Sumitra Ganesh
published_at: '2024-10-10 00:00:00'
theme_ids:
- alignment_and_safety
- alignment_methods
- post_training_methods
- reinforcement_learning
- reward_modeling
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# GenARM: Reward Guided Generation with Autoregressive Reward Model for Test-time Alignment

GenARM introduces a novel reward model architecture — the Autoregressive Reward Model — that parametrizes trajectory-level rewards as sums of token-level log probabilities, enabling accurate and efficient next-token reward prediction from partial responses. This resolves a fundamental architectural mismatch in prior test-time alignment methods and allows a small (7B) reward model to steer frozen LLMs at any scale without retraining, matching DPO performance while supporting real-time multi-objective preference trade-offs.

**Authors:** Yuancheng Xu, Udari Madhushani Sehwag, Alec Koppel, Sicheng Zhu, Bang An, Furong Huang, Sumitra Ganesh
**Published:** 2024-10-10
**Type:** Paper
**Source:** https://arxiv.org/pdf/2410.08193

---

## Motivation

[[themes/alignment_methods|Training-time alignment]] methods like RLHF and DPO require full retraining for each new preference configuration — a fundamental scalability bottleneck that makes personalized or multi-objective alignment computationally prohibitive. [[themes/test_time_learning|Test-time alignment]] emerged as an alternative: guide a frozen LLM at inference without gradient updates. But existing test-time methods exposed a different structural problem.

All prior approaches relied on *trajectory-level* reward models — models trained to evaluate complete responses. Applied to autoregressive generation, which requires next-token rewards from *partial* responses, these models fail in one of two ways:

- **Inaccurate estimates** (ARGS, CARDS): Apply trajectory-level RMs directly to incomplete responses, but these models were never trained on partial sequences. Quality degrades severely on long responses, producing gibberish.
- **Prohibitive cost** (Transfer-Q, Huang et al., Chakraborty et al.): Generate full rollouts for every candidate next token to obtain a complete-response reward. Transfer-Q takes **130.53 seconds** to generate 128 tokens with a 7B LLM; GenARM takes **7.28 seconds**.

A third class (Mudgal et al., Han et al.) trains a separate value function for partial responses — adding training overhead that defeats the cost advantage of test-time alignment.

---

## Approach

### The Autoregressive Reward Model

GenARM's core contribution is a reward parametrization that is *natively compatible* with autoregressive generation. The Autoregressive RM treats the trajectory-level reward as:

$$r(x, y) = \log \pi_r(y|x) = \sum_t \log \pi_r(y_t \mid x, y_{<t})$$

where $\pi_r$ is a standard LM-architecture distribution. This decomposes the sparse trajectory reward into a **dense token-level signal**: each decoding step yields a next-token log probability directly from a single forward pass. No rollouts required, no partial-response approximation error.

Training uses the same Bradley-Terry preference loss as trajectory-level RMs, but enforces that accumulated token-level rewards are higher for preferred responses than dispreferred ones across the full sequence. No additional infrastructure is needed beyond a standard preference dataset.

**Theoretical grounding:** Theorem 3 proves that every reward equivalence class under the Bradley-Terry framework contains a member of the form $\log \pi_r(y|x)$. The autoregressive parametrization loses no expressiveness relative to unconstrained trajectory-level RMs within the KL-regularized RL objective.

### Inference

At each decoding step, GenARM combines the base LLM's logits with the Autoregressive RM's token distribution:

$$\tilde{\pi}_{decode}(y_t \mid x, y_{<t}) \propto \pi_{base}(y_t \mid x, y_{<t}) \cdot \pi_r(y_t \mid x, y_{<t})^{1/\beta}$$

This requires **one forward pass** through each model per token — equivalent to decoding from two LMs simultaneously, with no overhead relative to standard guided decoding.

### Multi-Objective Extension

Multiple Autoregressive RMs for separate preference dimensions compose naturally:

$$\tilde{\pi}_{decode}(y_t \mid x, y_{<t}) \propto \pi_{base} \cdot \prod_i \pi_r^{(i)}(y_t)^{\alpha_i / \beta}$$

The coefficients $\{\alpha_i\}$ can be adjusted at test time per request — no retraining required when preference weights change.

---

## Results

### Head-to-Head Alignment Quality

On HH-RLHF with LLaMA-7B, GPT-4 evaluation (win+½tie rate):

| Method | Score | Time (128 tokens) |
|---|---|---|
| **GenARM** | **51.44%** | **7.28s** |
| CARDS | 41.94% | 87.09s |
| Transfer-Q | 33.72% | 130.53s |
| ARGS | 26.89% | — |

GenARM matches DPO (training-time baseline) while operating on a frozen base LLM.

### Weak-to-Strong Guidance

On AlpacaEval 2 with the Tulu2 model family, a single **7B Autoregressive RM** improves frozen base LLMs at all scales (7B, 13B, 70B) without training them:

- At 70B scale: recovers **>70% of the performance gap** between Tulu2-SFT-70B and Tulu2-DPO-70B in both raw and length-controlled win rates.
- Outperforms Best-of-N (N=16) at every scale, despite BoN requiring 16× more base LLM inference.
- ARGS breaks down on long responses at all scales, confirming that trajectory-level RM guidance is fundamentally unsuited to autoregressive token prediction.

Qualitative inspection confirms semantic coherence of token-level rewards: the Autoregressive RM assigns higher scores to harmless tokens like 'respect' and 'kind', and lower scores to harmful tokens, demonstrating that the dense reward signal is meaningfully grounded.

### Multi-Objective Alignment

On PKU-SafeRLHF-10K (helpfulness vs. harmlessness), GenARM produces a Pareto frontier that surpasses Rewarded Soups and is comparable to Multi-objective RL — without retraining for any point on the frontier. GenARM also extends weak-to-strong multi-objective guidance to 65B scale (7B RM → Alpaca-65B), a configuration that MORL and Rewarded Soups cannot match without training the full 65B model.

---

## Limitations & Open Questions

**Architectural scope.** The approach has only been validated for [[themes/alignment_and_safety|human preference alignment]]. Extension to reasoning tasks (mathematics, coding) — where reward signals differ structurally — is entirely unexplored. *(severity: significant)*

**Scale ratio degradation.** At 70B scale, the 7B reward model recovers only ~70% of the DPO performance gap. Whether this diminishes further at larger size ratios (e.g., 7B RM → 405B LLM) is unknown, and larger autoregressive reward models (13B, 34B, 70B) have not been evaluated as guidance sources. *(severity: minor, trajectory: unclear)*

**Evaluation methodology.** Response quality is measured exclusively via GPT-4-as-judge rather than human raters, introducing potential systematic biases in preference measurement. The degree to which GPT-4 judgments reflect true human alignment is not validated. *(severity: minor)*

**Largest-scale multi-objective comparison missing.** Multi-objective baselines (MORL, Rewarded Soups) are not compared at 65B scale due to compute cost, leaving open whether GenARM's advantage holds at scale or is partially an artifact of baseline under-resourcing. *(severity: minor)*

**Trajectory-level RM failure mode confirmed.** The paper demonstrates clearly that applying trajectory-level RMs to partial sequences causes catastrophic output degradation on long responses — a [[themes/reward_modeling|reward modeling]] failure mode that extends to any system using standard RMs for token-level guidance, not just ARGS.

---

## Implications

**Decoupling alignment capability from training scale.** A 7B reward model is sufficient to steer a 70B frozen LLM to near-DPO quality. This suggests the performance penalty observed in prior test-time alignment was not a fundamental limitation of the paradigm — it was a *mismatch* between the reward model's architecture and the generation process. Once the architectural mismatch is fixed, test-time alignment becomes competitive with training-time methods.

**Real-time personalization becomes tractable.** By adjusting scalar coefficients at inference, operators can serve diverse user preference profiles from a single frozen base LLM and a small set of dimension-specific reward models. This has direct implications for [[themes/alignment_methods|alignment at deployment scale]] — no per-user fine-tuning, no preference-specific model variants.

**Bottleneck resolution for test-time alignment.** Prior work established a bottleneck: trajectory-level RMs are architecturally incompatible with autoregressive generation, blocking efficient test-time alignment. GenARM resolves this with a reparametrization that fits naturally into standard decoding, opening the path toward practical deployment of test-time alignment methods.

**Connection to [[themes/reinforcement_learning|RL-based alignment]].** The theoretical result (Theorem 3) establishes formal equivalence between autoregressive reward parametrization and unconstrained trajectory-level rewards within the KL-regularized objective — grounding GenARM not as an approximation but as an exact alternative within the standard RLHF framework.

---

## Related Themes

- [[themes/alignment_and_safety|Alignment & Safety]]
- [[themes/alignment_methods|Alignment Methods]]
- [[themes/post_training_methods|Post-Training Methods]]
- [[themes/reinforcement_learning|Reinforcement Learning]]
- [[themes/reward_modeling|Reward Modeling]]
- [[themes/test_time_learning|Test-Time Learning]]

## Key Concepts

- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/length-controlled-win-rate|Length-Controlled Win Rate]]
- [[entities/lora|LoRA]]
- [[entities/rlhf|RLHF]]
- [[entities/reinforcement-learning-from-human-feedback|Reinforcement Learning from Human Feedback]]
- [[entities/ultrafeedback|UltraFeedback]]
