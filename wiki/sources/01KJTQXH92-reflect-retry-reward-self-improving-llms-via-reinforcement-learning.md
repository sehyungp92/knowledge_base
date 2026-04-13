---
type: source
title: 'Reflect, Retry, Reward: Self-Improving LLMs via Reinforcement Learning'
source_id: 01KJTQXH92QANC6B16JEK1TBFS
source_type: paper
authors:
- Shelly Bensal
- Umar Jamil
- Christopher Bryant
- Melisa Russak
- Kiran Kamble
- Dmytro Mozolevskyi
- Muayad Ali
- Waseem AlShikh
published_at: '2025-05-30 00:00:00'
theme_ids:
- chain_of_thought
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Reflect, Retry, Reward: Self-Improving LLMs via Reinforcement Learning

**Authors:** Shelly Bensal, Umar Jamil, Christopher Bryant, Melisa Russak, Kiran Kamble, Dmytro Mozolevskyi, Muayad Ali, Waseem AlShikh
**Published:** 2025-05-30 00:00:00
**Type:** paper

## Analysis

# Reflect, Retry, Reward: Self-Improving LLMs via Reinforcement Learning
2025-05-30 · paper · Shelly Bensal, Umar Jamil, Christopher Bryant, Melisa Russak, Kiran Kamble et al. (8 total)
https://arxiv.org/pdf/2505.24726

---

### Motivation & Prior Limitations
- LLMs have unpredictable blind spots: a model that succeeds at one task may fail at a structurally similar one, and there is no guarantee of consistent performance across task variants.
  - Direct remediation via retraining or fine-tuning is blocked when no dataset exists for the failed task, and synthetic data generation is also blocked when frontier models themselves fail the task.
- Prompting-based self-reflection improves accuracy in many settings but its effectiveness is strongly context-dependent, with known failure modes including inability to reliably identify self-errors without ground-truth oracles, diminishing returns from repeated reflection, and performance deterioration on easier prompts or high-performing base models.
  - Self-reflection is most effective when initial accuracy is low and external verification is available — conditions that limit its general applicability.
- Existing training-based self-improvement methods typically rely on larger teacher models for data generation or supervision, making them a form of knowledge distillation rather than true self-improvement.

---

### Proposed Approach
- The paper introduces "Reflect, Retry, Reward" (R3), a two-stage RL framework that trains models to generate better self-reflections by rewarding only the self-reflection tokens when a failed attempt is followed by a successful retry.
  - This contrasts with prior training-based methods that require teacher models or task-specific datasets; R3 bootstraps entirely from the model's own outputs and requires only a binary success/failure signal from an external validator.
  - Crucially, the reward signal is applied exclusively to the self-reflection tokens (all other token advantages are set to zero), so the model learns to improve general reflective reasoning rather than memorizing solutions to specific tasks.
- The optimization algorithm is Group Relative Policy Optimization (GRPO), chosen because it estimates advantages by comparing a group of sampled completions without a separate critic network, making it well-suited to sparse, end-of-sequence supervision.
  - The authors extend TRL's GRPOTrainer with a custom `second_step` function that generates a second completion conditioned on the self-reflection, applies the reward mask only to reflection tokens, and leaves the GRPOTrainer's existing mask structure intact.
- Training efficiency is improved by first constructing a "dataset of failures" through rejection sampling: up to 64 responses per query are generated, and only queries where the model failed are retained, avoiding wasted compute on examples the model already handles correctly.

---

### Results & Capabilities
- On the APIGen function calling benchmark (12,000 test samples), GRPO self-reflection training improved average accuracy by 9.0% across models, with individual gains as high as 16.3 percentage points (Qwen-2-1.5B rising from 32.6% to 48.6% on the first attempt).
  - After training, Qwen-2-7B Instruct given two attempts (77.3%) outperforms vanilla Qwen-2-72B Instruct given two attempts (76.6%), despite the latter being 10× larger.
- On the Countdown math equation dataset (15,000 test samples), GRPO training improved average accuracy by 16.0%, with the most dramatic gain being Qwen-2.5-1.5B rising from 6.0% to 45.0% on two attempts — a 39 percentage point absolute improvement.
  - The paper reports a headline figure of 34.7% improvement at math equation writing and 18.1% improvement at function calling as peak single-model gains.
- A secondary finding is that GRPO self-reflection training improves first-attempt accuracy even when no explicit self-reflection is generated at inference time, suggesting that reflection training improves general reasoning ability rather than only the retry mechanism.
  - The authors hypothesize that optimizing for self-reflection forces models to internalize meta-cognitive reasoning skills that transfer to initial-attempt performance.
- Catastrophic forgetting is minimal: on MMLU-Pro, GSM8K, HellaSwag, and MATH benchmarks, fine-tuned models show less than 1% degradation versus their vanilla baselines in nearly all cases, and some models show marginal improvements (e.g., Qwen-2.5-1.5B gains 0.6% on MMLU-Pro and 0.8% on MATH).
- Qualitatively, GRPO-trained self-reflections are markedly shorter, less repetitive, and more actionable than vanilla self-reflections, which tend to be verbose and redundant — an emergent property the authors note contrasts with chain-of-thought findings that favor verbosity.

---

### Implications
- Effective self-improvement via RL no longer requires teacher models or labeled datasets for the target task, only a binary verifier — a condition satisfied by a wide class of practically important tasks (JSON validation, code execution, equation checking, API response validity), substantially lowering the barrier to improving specialized model capabilities.
- The result that 7B models trained with R3 outperform vanilla 72B models on two separate tasks challenges the assumption that capability gaps between model size classes are fixed, and suggests that targeted RL training on meta-cognitive skills may be a more compute-efficient path than scaling model size.
- The finding that self-reflection training generalizes to first-attempt performance supports a broader hypothesis: that training models to reason about their own errors may be a task-agnostic route to improved reasoning, with potential implications for how RL fine-tuning is designed across the field.
- The task-agnostic nature of the reward signal — applied only to reflection tokens, not task-completion tokens — establishes a separation between learning *how to think about failure* and learning *how to

## Key Claims

1. The Reflect, Retry, Reward framework achieves up to 34.7% improvement at math equation writing and 18.1% improvement at function calling.
2. Smaller fine-tuned models (1.5B to 7B parameters) can outperform models in the same family that are 10 times larger.
3. The R3 framework requires only a binary success/failure signal from a response verifier, making it suitable for tasks where success can be easily verified.
4. The R3 framework bootstraps solely from the model's own outputs without relying on external LLMs.
5. In the R3 framework, only the tokens generated during the self-reflection phase are rewarded, not the tokens of the correct answer.
6. GRPO-trained models perform better even on their first attempt (without needing to explicitly self-reflect), suggesting self-reflection training improves general reasoning.
7. Qwen-2-7B Instruct after GRPO training outperforms vanilla Qwen-2-72B Instruct on function calling when both models are given two attempts.
8. On function calling (APIGen), GRPO-trained models improved performance by an average of 9.0% on the 12,000-sample test set.
9. On Countdown math equation solving, GRPO-trained models improved performance by an average of 16.0% on the 15,000-sample test set.
10. Self-reflections generated by GRPO fine-tuned models are shorter, clearer, and more generalisable compared to those from vanilla models.

## Capabilities

- LLMs can be trained via GRPO to generate better self-reflections using only binary success/failure feedback, achieving substantial performance gains without task-specific training data or teacher models
- Small fine-tuned models (7B parameters) can outperform models 10x their size on structured verifiable tasks after self-reflection training
- Self-reflection training generalises to improve first-attempt performance even when no explicit self-reflection is generated at test time, suggesting generalised reasoning enhancement
- GRPO-based self-reflection training preserves general language model capabilities across diverse benchmarks with less than 1% degradation

## Limitations

- Self-reflection training requires a binary success/failure validator, which cannot be readily defined for open-ended, creative, or subjective tasks
- Models must have a minimum baseline capability to perform the task, self-reflect, and learn — the method fails entirely for models below this capability threshold
- GRPO has known computational efficiency and scalability concerns that cap the method's applicability to models between 1.5B and 8B parameters
- Sub-1.5B models completely fail to benefit from self-reflection training, with near-zero baseline task performance and no capacity for meaningful self-reflection
- Self-reflection training has only been validated on two highly structured verifiable task types (function calling, math equations); cross-domain generalisation is unproven and explicitly deferred to future work
- Self-reflection effectiveness degrades for easier prompts, high-performing base models, and shows diminishing returns with repeated reflection iterations
- The framework provides only two attempts per task — if the second attempt fails, no further improvement is available, limiting recovery from fundamentally flawed approaches
- Model family architecture creates large and persistent capability disparities on reasoning tasks that self-reflection training cannot overcome — Llama 70B is outperformed by Qwen 3B on Countdown math
- Constructing a failure dataset requires rejection sampling with up to 64 generations per query, making dataset construction disproportionately expensive for capable models that fail infrequently
- Microsoft Phi 3.5 mini, despite handling function calling well, failed significantly on equation writing — revealing task-specific capability gaps within the same model that architecture cannot explain

## Bottlenecks

- Lack of reliable automated verifiers for open-ended tasks blocks application of RL-based self-reflection training to most real-world domains beyond structured outputs
- GRPO computational scalability issues block application of self-reflection training to frontier-scale models above ~10B parameters
- Minimum model capability threshold blocks applying self-correction training to sub-1.5B models, preventing cost-effective deployment of self-improving AI on edge devices

## Breakthroughs

- Task-agnostic self-reflection training via GRPO with binary-only feedback enables small models (7B) to outperform models 10x their size, bootstrapping entirely from the model's own outputs without teacher models or task-specific data

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/catastrophic-forgetting|Catastrophic Forgetting]]
- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/gsm8k|GSM8K]]
- [[entities/hellaswag|HellaSwag]]
- [[entities/knowledge-distillation|Knowledge Distillation]]
- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
