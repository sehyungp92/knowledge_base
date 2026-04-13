---
type: source
title: 'RLPR: Extrapolating RLVR to General Domains without Verifiers'
source_id: 01KJTPV81QCQHFFQ4QGCPKJ8FY
source_type: paper
authors:
- Tianyu Yu
- Bo Ji
- Shouli Wang
- Shu Yao
- Zefan Wang
- Ganqu Cui
- Lifan Yuan
- Ning Ding
- Yuan Yao
- Zhiyuan Liu
- Maosong Sun
- Tat-Seng Chua
published_at: '2025-06-23 00:00:00'
theme_ids:
- mathematical_and_formal_reasoning
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# RLPR: Extrapolating RLVR to General Domains without Verifiers

**Authors:** Tianyu Yu, Bo Ji, Shouli Wang, Shu Yao, Zefan Wang, Ganqu Cui, Lifan Yuan, Ning Ding, Yuan Yao, Zhiyuan Liu, Maosong Sun, Tat-Seng Chua
**Published:** 2025-06-23 00:00:00
**Type:** paper

## Analysis

# RLPR: Extrapolating RLVR to General Domains without Verifiers
2025-06-23 · paper · Tianyu Yu, Bo Ji, Shouli Wang, Shu Yao, Zefan Wang et al. (12 total)
https://arxiv.org/pdf/2506.18254

---

### Motivation & Prior Limitations
- RLVR has demonstrated strong reasoning gains for LLMs but remains almost entirely confined to mathematics and code domains, leaving the vast majority of knowledge domains unreachable by this training paradigm.
  - The core bottleneck is the dependence on domain-specific verifiers: rule-based verifiers require prohibitive heuristic engineering per domain and cannot handle free-form natural language answers due to their diversity and complexity (rule-based verifier achieves only 0.61 AUC on general-domain data vs. 0.95 on math).
  - Trained verifier models (e.g., General Reasoner's 1.5B verifier distilled from Gemini 2.0) require extensive annotation, introduce additional computation cost, complicate the RL training loop, and still generalize poorly across domains (General-Verifier AUC drops from 0.95→0.92 on math data when fine-tuned for general domains).
- Concurrent verifier-free work (VeriFree) uses sequence likelihood as reward but is constrained to reference answers shorter than 7 tokens, severely limiting data diversity, and requires an auxiliary fine-tuning loss; it also shows high sensitivity to prompt template choice (up to 8.0-point performance swings across templates).

---

### Proposed Approach
- RLPR (Reinforcement Learning with Reference Probability Reward) replaces external verifiers entirely with the policy model's own per-token decoding probabilities over the reference answer as the reward signal, enabling RLVR to scale to arbitrary domains without any specialized engineering.
  - The core insight is that the LLM's intrinsic probability of generating a correct answer reflects its internal evaluation of reasoning quality and naturally handles free-form language, including partially correct answers that binary verifiers would wrongly label as zero.
  - The **probability reward (PR)** is computed as the mean per-token probability of reference answer tokens — not the product (sequence likelihood) — which avoids the multiplicative instability where a single low-probability token (e.g., 1e−4 vs. 1e−5) can cause tenfold reward differences and force short-answer filtering.
- **Reward debiasing** subtracts a base score computed by running the reference answer through the model *without* the reasoning chain, so the final reward $\hat{r} = \text{clip}(0,1, r - r')$ measures the *improvement* in probability attributable to the reasoning content rather than confounds from question and answer surface form.
- **Standard deviation filtering** replaces accuracy-based filtering (which requires binary correctness) with an adaptive curriculum mechanism: prompts whose sampled responses yield low reward standard deviation (indicating uniformly easy or uniformly hard problems) are excluded using a dynamically updated EMA threshold, stabilizing training as the reward distribution shifts over time.

---

### Results & Capabilities
- RLPR consistently improves both general-domain and mathematical reasoning across Qwen2.5-7B, Llama3.1-8B, and Gemma2-2B base models without any external verifiers, achieving a 24.9% relative improvement on four general-domain benchmarks for Qwen2.5-7B.
  - On seven benchmarks, RLPR (no verifier) reaches 53.6 average accuracy vs. 52.0 for General Reasoner (which uses a dedicated 1.5B trained verifier), a +1.6 average point improvement.
  - RLPR outperforms concurrent verifier-free VeriFree by 7.6 points on TheoremQA (55.4 vs. 47.6) and 7.5 points on Minerva (56.5 vs. 49.0) on Qwen2.5-7B.
- PR achieves higher reward discrimination quality than both rule-based verifiers and trained verifier models across domains, as measured by ROC-AUC against human annotations: PR with Qwen2.5-7B achieves 0.97 AUC on math and 0.91 on general data, versus 0.61 for rule-based on general data and 0.92/0.69 for the trained General-Verifier.
  - Even the smallest Qwen2.5-0.5B used as the probability model outperforms the specifically trained General-Verifier on both math and general data, suggesting the intrinsic capability of base LLMs is a surprisingly strong evaluation signal.
- Training on general-domain data (77k non-math prompts from WebInstruct) also yields meaningful gains on math benchmarks not seen during training: +1.9 on TheoremQA and +4.3 on Minerva compared to math-only RLVR training, indicating positive cross-domain transfer.
- Ablation results confirm the necessity of each component: removing token-probability averaging (reverting to sequence likelihood) drops TheoremQA by 21.9 points and Minerva by 22.3 points; removing debiasing costs 2.7/2.4 points; removing std-filtering costs 2.9/1.4 points.
- PR values show negligible correlation with response length (average Spearman coefficient −0.060) and entropy (0.059), with only 8% of prompts yielding statistically significant correlations, confirming robustness to these confounds.
- PR also provides fine-grained signal in verifiable domains: combining rule-based rewards with PR on mathematical data improves TheoremQA from 44.8→48.8, as PR discriminates among responses that share the same binary correctness label.

---

### Implications
- By decoupling RLVR from domain-specific verifiers, RLPR removes the primary structural barrier to applying test-time compute scaling and RL post-training to the full breadth of human knowledge domains — science, law, medicine, social science — where ground-truth verifiers are impractical to build.
- The result that a model's own token probabilities constitute a higher-quality reward signal than dedicated trained verifier models challenges the assumption that reward modeling requires separate specialized infrastructure, suggesting that intrinsic LLM capabilities are underutilized in current RL pipelines.
- The approach creates a virtuous cycle for general reasoning: gene

## Key Claims

1. RLVR success remains largely confined to mathematical and code domains due to heavy reliance on domain-specific verifiers
2. Rule-based verifiers are impossible to devise for general-domain reasoning with free-form answers due to high diversity and complexity of natural language
3. Training specialized LLMs as verifier models requires non-trivial data annotation and often leads to unsatisfactory reward quality
4. LLM's intrinsic probability of generating a correct answer directly indicates its internal evaluation of reasoning quality
5. RLPR outperforms concurrent VeriFree by 7.6 points on TheoremQA and 7.5 points on Minerva
6. RLPR surpasses General-Reasoner (which uses a trained 1.5B-parameter verifier model) by 1.6 average points across seven benchmarks
7. RLPR improves average performance on four general-domain reasoning benchmarks by 24.9% on Qwen2.5-7B without any external verifier
8. RLPR achieves larger general reasoning improvement over RLVR for Gemma (+1.4), Llama (+3.9), and Qwen (+1.4) average points
9. Mean per-token probability is a more robust reward signal than normalized product (sequence likelihood) because it avoids extreme sensitivity to single low-probability tokens
10. Sequence likelihood as reward is overly sensitive to minor variations such as synonyms; probabilities of 1e-4 versus 1e-5 can lead to tenfold reward difference

## Capabilities

- RLVR training can be extended to general domains (beyond math/code) without external verifiers by using the LLM's own per-token probability scores for reference answers as the reward signal (RLPR framework), achieving 24.9% improvement on four general-domain benchmarks on Qwen2.5-7B
- LLM intrinsic per-token decoding probabilities serve as high-quality domain-agnostic reward signals for RL training, achieving higher reward quality (AUC 0.81–0.91 on general data) than trained 1.5B verifier models (0.69 AUC) and rule-based verifiers (0.61 AUC) on general domains
- General-domain RL training transfers to improve mathematical reasoning even when math prompts are excluded from training — training on 77k non-math prompts yields +1.9 on TheoremQA and +4.3 on Minerva compared to math-domain-only training
- Probability-based reward provides graded fine-grained reward discrimination for RL training, capturing partial correctness unlike binary rule-based verifiers — a per-token probability signal produced in a single forward pass, with negligible correlation to response length or entropy
- Adaptive curriculum learning via exponential-moving-average reward standard deviation filtering stabilizes RL training by dynamically tracking and removing prompts that are too easy or too complex, handling reward distribution shifts throughout training

## Limitations

- RLVR training success remains largely confined to mathematical and code domains — general-domain extension requires either prohibitive domain-specific verifier engineering or approximate probability-based substitutes
- Rule-based verifiers achieve only 0.61 AUC on general-domain prompts vs 0.95 on math — binary rule matching fundamentally fails to judge semantic equivalence, paraphrasing, or alternative valid answer formats in free-form natural language
- Trained verifier models (General-Verifier at 1.5B) suffer generalization failure across domains — AUC drops from 0.95 to 0.92 on math when trained for general domains, indicating fine-tuning creates hard capability tradeoffs between domains
- Raw sequence likelihood as reward is highly sensitive to single low-probability tokens — probabilities of 1e-4 vs 1e-5 yield a tenfold reward difference despite negligible absolute difference, making naive implementations of probability-based RL unstable
- Concurrent VeriFree approach (Zhou et al. 2025) is limited to reference answers ≤7 tokens, severely restricting applicable training data diversity — probability reward degrades for longer free-form answers without careful engineering to replace sequence likelihood
- Probability reward is systematically biased by latent factors independent of reasoning quality — question characteristics and reference answer text properties inflate raw probability scores, requiring a debiasing step that costs 2.4–2.7 performance points if omitted
- AIME24 hard mathematical olympiad performance remains poor under RLPR (16.3 Avg@16) compared to math-specialized RLVR methods (Oat-Zero: 29.8, SimpleRL-Zoo: 26.5) — general-domain RL training does not transfer to close the gap on hard formal competition math
- Training capped at 3072 max generation tokens — longer reasoning chains required for highly complex problems are excluded from RL training, likely creating a ceiling on gains for problems requiring extended deliberation
- RLPR training requires 77,000+ curated training prompts filtered via GPT-4.1 — the method implicitly depends on a capable external model for data curation, creating an unacknowledged dependency on closed frontier AI infrastructure
- Gemma and Llama model families require different training hyperparameters and template configurations — the <think> reasoning tag must be removed and temperature adjusted 'to prevent generation degradation', indicating fragility of probability-based RL across architectures
- Multimodal understanding domains are conspicuously absent from RLPR evaluation — the framework's applicability to image, video, or audio reference answers is entirely unexplored, suggesting probability-based reward may not generalize to non-text modalities
- Rule-based scoring scripts introduce systematic evaluation errors on benchmarks containing non-multiple-choice question formats — general-domain RL evaluation itself requires LLM judges, meaning evaluation quality is entangled with judge model capability

## Bottlenecks

- Domain-specific verifier requirement prevents RLVR from scaling beyond math and code — rule-based verifiers require prohibitive per-domain heuristic engineering, and trained model verifiers require extensive labeled data that generalizes poorly across domains
- Probability-based reward high variance and latent bias create training instability — continuous reward distributions make standard accuracy-based filtering inapplicable, and systematic bias from non-reasoning factors must be explicitly corrected to avoid degraded learning

## Breakthroughs

- RLPR demonstrates that LLM intrinsic token probability scores serve as sufficient domain-agnostic verifier replacements, enabling RLVR training across arbitrary general domains without any external verifier — outperforming both rule-based verifiers and trained 1.5B verifier models in reward quality

## Themes

- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/entropy-collapse|Entropy Collapse]]
- [[entities/gpqa|GPQA]]
- [[entities/grpo-group-relative-policy-optimization|GRPO (Group Relative Policy Optimization)]]
- [[entities/generative-reward-model|Generative Reward Model]]
- [[entities/minerva|Minerva]]
- [[entities/prime|PRIME]]
- [[entities/reinforcement-learning-with-verifiable-rewards-rlvr|Reinforcement Learning with Verifiable Rewards (RLVR)]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/webinstruct|WebInstruct]]
