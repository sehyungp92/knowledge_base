---
type: source
title: 'Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty'
source_id: 01KJTN6GH7AG4Y8XWP6J7Y2BTN
source_type: paper
authors:
- Mehul Damani
- Isha Puri
- Stewart Slocum
- Idan Shenfeld
- Leshem Choshen
- Yoon Kim
- Jacob Andreas
published_at: '2025-07-22 00:00:00'
theme_ids:
- alignment_and_safety
- chain_of_thought
- hallucination_and_reliability
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty

**Authors:** Mehul Damani, Isha Puri, Stewart Slocum, Idan Shenfeld, Leshem Choshen, Yoon Kim, Jacob Andreas
**Published:** 2025-07-22 00:00:00
**Type:** paper

## Analysis

# Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty
2025-07-22 00:00:00 · paper · Mehul Damani, Isha Puri, Stewart Slocum, Idan Shenfeld, Leshem Choshen et al. (7 total)
https://arxiv.org/pdf/2507.16806

---

### Motivation & Prior Limitations
- Standard RL training for reasoning models (RLVR) uses binary correctness rewards that treat confident correct answers identically to lucky guesses, and treat abstentions identically to incorrect answers — creating a structural incentive for overconfident guessing rather than calibrated prediction.
  - Studies confirm that LLMs become overconfident following RL training (Leng et al., 2025), with reasoning models specifically showing worsened calibration and increased hallucination rates relative to base models (Kirichenko et al., 2025; Yao et al., 2025; OpenAI, 2025).
  - In high-stakes domains such as healthcare and law, a model that is accurate but cannot communicate its uncertainty appropriately is insufficient — trustworthiness requires both.
- Post-hoc confidence estimation methods (classifiers, probes, sampling-based surrogates) are either expensive (requiring a second large model), poorly generalizing, or divorced from the model's internal reasoning process.
  - Prior RL-based calibration work (Xu et al., 2024; Stangel et al., 2025) optimized solely for calibration using proper scoring rules, which can harm task accuracy — particularly in larger models that may learn to output deliberately wrong answers with zero confidence to maximize calibration scores.
  - These prior methods were also evaluated exclusively on non-reasoning tasks, leaving the interaction between calibration training and chain-of-thought reasoning unexplored.

---

### Proposed Approach
- RLCR (Reinforcement Learning with Calibration Rewards) augments the standard binary correctness reward with a Brier score term, training models to jointly output a natural language reasoning chain, a final answer, an uncertainty analysis, and a numerical confidence score.
  - The combined reward is `R_RLCR(y, q, y*) = 1[y≡y*] − (q − 1[y≡y*])²`, where the first term rewards correctness and the Brier term penalizes miscalibrated confidence — high confidence on wrong answers and low confidence on correct ones.
  - A formal theorem (Theorem 1) proves that this reward function satisfies two properties simultaneously: (1) for any fixed answer, expected reward is maximized when the stated confidence equals the true success probability; and (2) among all calibrated predictions, expected reward is maximized by the answer most likely to be correct. This two-property guarantee does not hold for all proper scoring rules — notably, using log-loss instead of the Brier score can incentivize outputting incorrect answers.
  - The approach uses a single model for both solution generation and confidence estimation, structured via `<think>`, `<answer>`, `<analysis>`, and `<confidence>` tags, trained with GRPO on Qwen2.5-7B Base without KL regularization.

---

### Results & Capabilities
- RLCR matches RLVR accuracy while dramatically improving calibration in-distribution: on HotpotQA, ECE drops from 0.37 (RLVR) to 0.03 (RLCR); on math benchmarks, ECE drops from 0.26 to 0.10.
  - RLCR slightly outperforms dedicated post-hoc classifiers on in-distribution calibration (ECE 0.03 vs. 0.07 for RLVR + BCE Classifier on HotpotQA), while requiring no second model at inference time.
- Out-of-distribution generalization is where RLCR most clearly separates from alternatives: RLVR actively harms OOD calibration relative to the base model (ECE 0.40 → 0.46 on HotpotQA OOD), while RLCR improves it substantially (0.40 → 0.21), also improving OOD accuracy slightly (53.3% → 56.2%).
  - The authors hypothesize three mechanisms for this OOD generalization: uncertainty reasoning during CoT enables explicit reflection on confidence; the non-stationarity of calibration targets during RL training (targets shift as accuracy improves) may produce more robust representations; and a shared model for solution and calibration allows the latter to leverage internal solution representations.
- Verbalized confidence scores can be used directly in test-time scaling: confidence-weighted majority voting outperforms both vanilla majority voting and max-confidence selection, and ensembling K uncertainty analysis CoTs for a fixed answer reduces Brier score monotonically with ensemble size.
  - These scaling gains require no external reward model or additional supervision — only additional sampling from the trained model.
- An ablation comparing classifiers trained on RLCR outputs (with confidence tags removed) versus RLVR outputs demonstrates that RLCR reasoning chains carry calibration-relevant information independently of the confidence score itself — the effect is most pronounced for smaller (0.5B, 1.5B) classifiers where model capacity is limiting.
- RLCR confidence estimates are self-consistent: confidence scores across multiple independently sampled uncertainty analysis chains for the same answer show low standard deviation, and in-distribution confidence sums across mutually exclusive answers cluster tightly around 1.

---

### Implications
- RLCR demonstrates that the binary reward structure of RLVR is not a necessary constraint — proper scoring rules can be integrated into reasoning training with provable theoretical guarantees and no accuracy cost, suggesting calibration should be treated as a first-class objective in reasoning model training rather than a post-hoc patch.
- The result that RLVR actively degrades OOD calibration is a significant finding for deployment: reasoning models trained with standard methods may be systematically less trustworthy than base models when applied outside their training distribution, with no visible accuracy signal alerting practitioners.
- Verbalized confidence as a proxy reward for test-time scaling opens a path to self-supervised scaling that does not depend on external verifier

## Key Claims

1. Binary correctness reward functions used in RLVR have the unintended side-effect of degrading calibration and increasing hallucination rates in other problem domains.
2. RLCR matches the task accuracy of RLVR while substantially improving calibration, reducing expected calibration error from 0.37 to 0.03 on HotpotQA in-distribution.
3. RLVR substantially worsens calibration relative to the base model on out-of-domain tasks, while RLCR substantially improves calibration on out-of-domain tasks.
4. Standard binary correctness reward incentivizes overconfident guessing because it rewards models equally whether they are confidently correct or merely guessing.
5. LLMs tend to become overconfident following RL training even when initially well-calibrated.
6. Reasoning models exhibit worsened calibration and increased hallucination rates compared to base models, particularly when trained with reward signals that emphasize only correctness.
7. RLCR provably incentivizes both accuracy and calibration: the combined reward is maximized when the model outputs the most likely correct answer with a calibrated confidence estimate.
8. The log-likelihood loss, despite being a proper scoring rule, cannot be used as the calibration term in RLCR because it can incentivize models to output incorrect answers.
9. Any bounded proper scoring rule can be used to construct a calibration reward that provably incentivizes both correctness and calibration.
10. The Answer Probability baseline exhibits poor calibration because the model typically arrives at its answer during chain-of-thought reasoning, making the subsequent token probability within answer tag

## Capabilities

- RLCR (Reinforcement Learning with Calibration Rewards) trains reasoning models to jointly optimize accuracy and calibrated confidence estimation by augmenting binary correctness rewards with a Brier score calibration term, achieving ECE reduction from 0.37→0.03 on HotpotQA and 0.26→0.10 on math data
- Confidence-weighted majority vote using verbalized confidence scores from RLCR models as proxy reward signals outperforms both vanilla majority voting and max-confidence best-of-N selection at test-time scaling, without requiring external reward models or additional supervision
- Ensembling multiple uncertainty chain-of-thought analyses (sampling K analysis CoTs for a fixed answer and averaging verbalized confidence scores) monotonically improves calibration with ensemble size — a lightweight alternative to training additional probe/classifier models
- RLCR-trained reasoning models produce self-consistent verbalized confidence estimates: most samples exhibit low standard deviation across multiple uncertainty reasoning chains for the same answer, and confidence sums across mutually exclusive answers cluster near 1 in-distribution

## Limitations

- Standard RLVR training with binary correctness rewards degrades model calibration relative to the base model, particularly on out-of-distribution tasks, where it makes models more overconfident than before RL training — the training procedure actively harms a property the base model possessed
- Out-of-domain calibration error remains high in absolute terms even after RLCR training, with models still assigning high confidence to multiple mutually exclusive contradictory answers on unseen task distributions — in-domain calibration success does not fully transfer
- SFT warmup before RLCR (SFT+RLCR variant) causes catastrophic forgetting, significantly reducing out-of-distribution accuracy despite achieving the best in-domain and OOD calibration scores — best calibration and best generalization accuracy are mutually exclusive with current methods
- Answer token probability — computed from average probability of tokens within <answer> tags — is a systematically poor calibration proxy for CoT reasoning models, exhibiting pathological overconfidence because the model commits to its answer during the thinking phase before answer tokens are generat
- The log-likelihood loss — the ubiquitous standard language model training objective, itself a proper scoring rule — cannot theoretically incentivize both correctness and calibration simultaneously, and can perversely incentivize models to output deliberately incorrect answers to minimize calibration
- Without SFT warmup providing demonstration examples, RLCR-trained math reasoning models produce qualitatively generic uncertainty analyses that lack reasoning tied to specific solution steps — the uncertainty chain-of-thought is superficial hedging rather than substantive self-assessment
- For sufficiently expressive large models (7B+), RLCR uncertainty reasoning chains provide no measurable advantage over baseline classifiers trained on outputs without uncertainty analysis — at sufficient model capacity, calibration-relevant features can be inferred from the solution alone, making ex
- RLCR is validated only on question-answering tasks with verifiable binary ground truth; no evaluation on open-ended, multi-turn, or agentic tasks where calibration matters most and where verifiable binary correctness — required by the Brier score reward — is unavailable
- All RLCR experiments use a 7B parameter model; no evaluation at frontier scale (70B+) leaves open whether calibration gains transfer, whether larger models exploit the Brier reward differently, or whether the OOD calibration gap closes or widens with scale
- Post-hoc classifier approaches (RLVR + classifier) for confidence calibration require training and serving two separate large models simultaneously — operationally expensive and impractical compared to RLCR's single-model approach, yet classifiers match or exceed RLCR in-distribution calibration
- Uncertainty analysis faithfulness is unverified: verbalized confidence scores may be computed from internal representations independently of the explicit uncertainty reasoning chain, meaning the uncertainty CoT may be post-hoc rationalization rather than genuine calibration reasoning

## Bottlenecks

- Binary correctness rewards in RLVR structurally degrade calibration while improving accuracy — no existing RLVR formulation simultaneously incentivizes reasoning accuracy and well-calibrated uncertainty communication, blocking trustworthy deployment of reasoning models in high-stakes domains
- Out-of-distribution calibration generalization gap: models trained for calibration on one task distribution remain poorly calibrated on novel distributions, blocking reliable uncertainty quantification for AI systems exposed to the full diversity of real-world inputs

## Breakthroughs

- First formal proof and empirical demonstration that RL reward functions using bounded proper scoring rules (RLCR) can simultaneously and provably incentivize both reasoning accuracy and calibration — resolving the previously observed accuracy-calibration tradeoff in RL training and establishing a th

## Themes

- [[themes/alignment_and_safety|alignment_and_safety]]
- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/hallucination_and_reliability|hallucination_and_reliability]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/gpqa|GPQA]]
- [[entities/grpo|GRPO]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/rlvr-reinforcement-learning-with-verifiable-rewards|RLVR (Reinforcement Learning with Verifiable Rewards)]]
