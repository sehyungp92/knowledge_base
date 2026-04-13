---
type: source
title: Reinforcement learning with random rewards actually works with Qwen 2.5
source_id: 01KJSTGBK2S2N641WNQTS148ZD
source_type: article
authors: []
published_at: '2025-05-27 00:00:00'
theme_ids:
- mathematical_and_formal_reasoning
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Reinforcement learning with random rewards actually works with Qwen 2.5

**Authors:** 
**Published:** 2025-05-27 00:00:00
**Type:** article

## Analysis

# Reinforcement learning with random rewards actually works with Qwen 2.5
2025-05-27 · article
https://www.interconnects.ai/p/reinforcement-learning-with-random

---

## Briefing

**Qwen 2.5 Math 7B improves on MATH-500 by 15–24 points regardless of whether the reward signal is correct, random, or even inverted — because GRPO's clipping mechanism interacts with the model's pre-baked code-reasoning strategies to surface them regardless of reward content. This exposes a critical confound in the academic RLVR literature: the most-studied base models are precisely the ones where the reward signal is least meaningful, while the genuinely important question — whether RL can teach new capabilities at scale — remains unanswered by the open community.**

### Key Takeaways
1. **Random rewards improve MATH-500 by +15.8 pts on Qwen 2.5 Math 7B** — virtually the same order of magnitude as majority vote (+23.2) or even correct labels (+24.6), exposing that the reward signal is largely irrelevant for this model.
2. **The effect is Qwen-specific** — Llama 3.2 3B Instruct and OLMo 2 7B do not show analogous gains from random or spurious rewards, implicating unique pretraining decisions in the Qwen models.
3. **RLVR on Qwen is primarily eliciting code-assisted reasoning** — the rate of code reasoning strategies rises from ~65% at baseline to 90%+ after RLVR even with spurious rewards, and code-use correlates directly with MATH-500 accuracy gains.
4. **Qwen 2.5 Math was likely trained on perturbed test-set variants** — the model maintains accuracy when only numerical values in MATH problems are changed, suggesting near-contamination through synthetically modified questions.
5. **GRPO clipping is the mechanical culprit** — clipping disproportionately suppresses low-probability tokens, and without clipping the random-reward improvement vanishes, confirming that low-probability exploration tokens (code calls) are being uplifted as a side effect.
6. **Buggy or over-hard verifiers produce pathological gradients** — verifiers that are too strict yield near-zero gradients, while broken credit assignment biases the policy toward implementation artifacts like length.
7. **These results are the strongest evidence yet for the Elicitation Theory** — post-training appears to surface existing pretrained behaviors rather than add new ones, at least in the current academic compute regime.
8. **o3 represents a phase transition**: the author estimates o3 spent ~10–30% of total compute on post-training vs. ~1–3% for o1, and OpenAI confirmed ~10X the compute of o1, suggesting RL is moving from formatting tool to genuine capability engine.
9. **RL has no structural ceiling on capability gain** — Sholto Douglas argues DeepMind's Go/chess results show RL can exceed human-level performance from signal alone; the bottleneck is compute scale and algorithm quality, not the paradigm itself.
10. **Academic RLVR is stuck in the pre-scaling regime** — as long as experiments are small-scale on confounded base models, the community will debate artifacts rather than unlock genuine new capabilities.

---

### The RLVR Validity Crisis and the Qwen Anomaly

- A wave of papers has questioned whether RLVR actually improves mathematical capabilities in language models, showing competitive results from training on a single example, removing verifiers, or simply sampling more from base models.
  - The author previously attributed these findings to RLVR being mostly about **formatting rather than genuine capability gains**, a partial explanation that held until the Qwen random-reward results emerged.
- University of Washington graduate students (with the author's involvement) ran systematic ablations on Qwen 2.5 Math 7B across six reward variants and found MATH-500 improvements ranging from +15.8 to +24.6 across all of them:
  - Ground truth (correct answers): **+24.6 pts**
  - Majority vote reward: **+23.2 pts**
  - One-Shot RL (single example): **+21.4 pts**
  - Format reward (\\boxed{} presence only): **+19.8 pts**
  - Incorrect labels (wrong answers rewarded): **+21.2 pts**
  - **Random rewards (content-independent probability): +15.8 pts**
- The ordering matters: random rewards produce the smallest gain, but the gap from worst to best is only ~9 points, far smaller than the gap from zero to any reward.
- The effect is **entirely absent on Llama 3.2 3B Instruct and OLMo 2 7B**, ruling out any explanation that applies to RL in general and pointing squarely at Qwen's pretraining.
- The author frames this charitably: this does not indict Qwen's engineering, it just makes these models **scientifically messy** — the wrong substrate for studying whether RL genuinely improves capabilities.

---

### What Is Unusual About Qwen 2.5 Math's Pretraining

- The paper hypothesises that RLVR outcome differences trace to **reasoning strategies learned during pretraining**, with some strategies more readily elicited by any form of policy gradient and others absent or inaccessible.
  - The specific strategy identified: **code-assisted mathematical reasoning** — generating executable code to solve math problems — which Qwen-Math uses heavily and other families do not.
- Evidence for near-test-set contamination:
  - Qwen 2.5 Math 7B maintains high accuracy on MATH benchmark problems when **only the numerical values are substituted** (e.g., coefficients, constants), while the structural setup remains identical.
  - The model can produce **complex numerical answers to high decimal precision** when predicting code outputs, far beyond what pure symbolic reasoning would yield.
  - The implied training regime: Qwen trained on questions structurally identical to MATH problems but with different integers, a form of data augmentation that produced near-contamination without literally using test examples.
    - Example: evaluation asks for degree of polynomial with specific coefficients; training used the same polynomial structure with different numbers.
  - The MATH-Pertur

## Key Claims

1. Qwen 2.5 Math 7B improves MATH-500 scores by 15+ points even when trained with random rewards under GRPO.
2. Standard RLVR with ground truth rewards improves Qwen 2.5 Math 7B MATH-500 score by +24.6 points.
3. Training Qwen 2.5 Math 7B with majority vote rewards improves MATH-500 by +23.2 points.
4. One-Shot RL (using a single example) improves Qwen 2.5 Math 7B MATH-500 by +21.4 points.
5. Rewarding only for the presence of \boxed{} formatting improves Qwen 2.5 Math 7B MATH-500 by +19.8 points.
6. Rewarding only incorrect answers improves Qwen 2.5 Math 7B MATH-500 by +21.2 points.
7. Random rewards (awarding 1 reward per rollout prompt with a fixed probability in GRPO) improve Qwen 2.5 Math 7B MATH-500 by +15.8 points.
8. The random-reward RLVR improvement effect on MATH-500 does not generalise to Llama 3.2 3B Instruct or OLMo 2 7B.
9. Differences in RLVR training outcomes are hypothesised to stem from differences in reasoning strategies learned during pretraining, with some strategies more readily elicited by RLVR than others.
10. Qwen 2.5 Math appears to have been pretrained on synthetic SFT data curated with code/tool-assisted math reasoning in the loop.

## Capabilities

- GRPO clipping interaction with pre-existing code reasoning strategies in Qwen 2.5 Math base models allows random or broken reward signals to shift code reasoning rate from ~65% to 90%+, yielding 15-20 point MATH-500 improvements — without any valid reward signal
- Scaling RL post-training to an estimated 10–30% of total training compute (as estimated for o3, versus ~1–3% for o1) unlocks genuinely new model behaviors beyond elicitation of pretrained knowledge

## Limitations

- Qwen 2.5 Math base models are unsuitable for reliable RLVR science because apparent gains reflect elicitation of pre-baked code reasoning strategies rather than reward-driven capability acquisition
- GRPO clipping causes entropy collapse and restricts exploration of low-probability token behaviors, biasing policy updates toward already-likely outputs and preventing genuine strategy discovery
- Overly strict reward verifiers produce near-zero policy gradients; buggy verifiers silently corrupt policy updates in unpredictable directions (e.g. toward length bias), with no obvious training-time warning
- Small-scale open RLVR research measures formatting improvements and base-model elicitation, not genuine capability acquisition — results are non-representative of frontier RL scaling and will not transfer
- Random-reward RLVR improvements are model-specific and require well-defined pre-existing strategies in the base model; the effect fails entirely on models like Llama 3.2 3B or OLMo 2 7B that lack such strategies
- Qwen 2.5 Math appears contaminated with near-duplicate benchmark variants (same problem structure, different integers), making MATH-500 scores an unreliable measure of generalisation for this model family
- Majority-vote as an RLVR surrogate reward may only be valid for models with sufficient base reliability; effectiveness on other model families is unclear and requires further study
- Open research community cannot replicate or study the RL scaling regime (estimated 10–30% of total compute) at which models begin learning genuinely new behaviors rather than eliciting existing ones

## Bottlenecks

- Open RLVR research is confined to the elicitation compute regime, where improvements reflect pretraining data artifacts rather than RL-learned behaviors, blocking scientific understanding of genuine post-training capability gains
- Pretraining data contamination in widely-used open base models (Qwen 2.5 Math) creates confounded experimental conditions that make it impossible to isolate genuine RLVR signal from base-model artifacts
- GRPO's clipping mechanism suppresses exploration of low-probability token sequences during RL training, potentially preventing acquisition of qualitatively novel behavioral strategies

## Breakthroughs

- Mechanistic explanation established for why random rewards improve MATH-500 in Qwen 2.5 Math: GRPO clipping interacts with the model's pre-existing code reasoning strategies to shift the policy toward code use regardless of reward signal validity, with code use rate rising from ~65% to 90%+ under sp

## Themes

- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]

## Key Concepts

- [[entities/entropy-collapse|Entropy Collapse]]
- [[entities/grpo-group-relative-policy-optimization|GRPO (Group Relative Policy Optimization)]]
- [[entities/policy-gradient|Policy Gradient]]
- [[entities/reinforcement-learning-with-verifiable-rewards-rlvr|Reinforcement Learning with Verifiable Rewards (RLVR)]]
