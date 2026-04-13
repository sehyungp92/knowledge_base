---
type: source
title: 'RM-R1: Reward Modeling as Reasoning'
source_id: 01KJTV56APTC54QC8EHJNJE2DG
source_type: paper
authors:
- Xiusi Chen
- Gaotang Li
- Ziqi Wang
- Bowen Jin
- Cheng Qian
- Yu Wang
- Hongru Wang
- Yu Zhang
- Denghui Zhang
- Tong Zhang
- Hanghang Tong
- Heng Ji
published_at: '2025-05-05 00:00:00'
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# RM-R1: Reward Modeling as Reasoning

**Authors:** Xiusi Chen, Gaotang Li, Ziqi Wang, Bowen Jin, Cheng Qian, Yu Wang, Hongru Wang, Yu Zhang, Denghui Zhang, Tong Zhang, Hanghang Tong, Heng Ji
**Published:** 2025-05-05 00:00:00
**Type:** paper

## Analysis

# RM-R1: Reward Modeling as Reasoning
2025-05-05 · paper · Xiusi Chen, Gaotang Li, Ziqi Wang, Bowen Jin, Cheng Qian et al. (12 total)
https://arxiv.org/pdf/2505.02387

---

### Motivation & Prior Limitations
Existing reward models lack the interpretable reasoning necessary to reliably judge complex, nuanced preference comparisons, limiting their usefulness for RLHF alignment.
- Scalar-based reward models (ScalarRMs) frame reward modeling as classification, producing opaque scalar outputs with no intermediate reasoning steps to justify decisions, making them unsuitable for reasoning-intensive preference tasks.
  - Without visible reasoning, ScalarRMs cannot handle multifaceted judgments requiring rubric inference, criterion trade-offs, or consequence simulation.
- Generative reward models (GenRMs) improve transparency by producing free-form text judgments, but their reasoning is often superficial and unhelpful for reliable discrimination, leading to suboptimal performance.
  - An off-the-shelf instruct model used as a GenRM overfits to surface-level patterns in supervised data (e.g., selecting a well-formed but subtly toxic response over a genuinely supportive one), failing to evaluate deeper impact.
- Simply applying reinforcement learning with verifiable rewards (RLVR) directly to a generative model does not fully realize reasoning capabilities, and plain chain-of-thought (CoT) reasoning fails to perceive fine-grained distinctions across different question types (e.g., chat vs. math/code).

---

### Proposed Approach
The paper introduces Reasoning Reward Models (ReAsRMs), a new class of generative reward models that explicitly formulate reward assignment as a reasoning task, and trains a family of them — RM-R1 — using a two-stage pipeline of reasoning distillation followed by reinforcement learning.
- The **Chain-of-Rubrics (CoR)** mechanism is the core inference innovation: the model first classifies each input as either `Chat` or `Reasoning`, then applies a type-specific rollout strategy before assigning a judgment.
  - For **chat tasks**, the model self-generates evaluation rubrics with justifications tailored to the specific question, then evaluates responses against those rubrics.
  - For **reasoning tasks** (math, code, domain knowledge), the model first solves the problem itself, then compares candidate responses against its own solution for correctness-first judgment.
- **Stage 1 — Reasoning Distillation**: An instruction-tuned base model (e.g., Qwen-2.5-14B-Instruct) is fine-tuned on high-quality reasoning traces synthesized by oracle models (o3, claude-3-7-sonnet), which generate structured justifications for preference labels. Training minimizes NLL over these traces to bootstrap reward modeling reasoning patterns.
- **Stage 2 — RL with Verifiable Rewards**: The distilled model is further optimized using GRPO with a binary correctness reward (+1 if the extracted `<answer>` matches ground truth label, −1 otherwise), overcoming the overfitting and generalization constraints of distillation alone. Format reward was tested but found to offer no significant improvement, as distillation already instills proper formatting.
- An alternative path for models already reasoning-capable (e.g., DeepSeek-distilled Qwen variants) skips Stage 1 and applies only RLVR fine-tuning, leveraging pre-existing reasoning distillation.

---

### Results & Capabilities
RM-R1 achieves state-of-the-art average performance across RewardBench, RM-Bench, and RMB benchmarks, outperforming both much larger open-weight models and proprietary ones.
- RM-R1-Qwen-Instruct-32B scores 91.4 / 79.1 / 73.0 (average 81.2) and RM-R1-DeepSeek-Distilled-Qwen-32B scores 90.9 / 83.9 / 69.8 (average 81.5), both surpassing INF-ORM-Llama3.1-70B (78.8 average) and GPT-4o-0806 (77.7 average) by up to 4.9% on average.
- RM-R1 outperforms all prior ReAsRM baselines including Self-taught-evaluator-llama3.1-70B (76.2 average) and DeepSeek-GRM-27B (partially reported), despite using smaller base models.
- The DeepSeek-distilled 14B variant (average 79.6) beats the instruction-tuned 32B variant (81.2 is needed for comparison, but 14B at 79.6 still exceeds all GenRM and ScalarRM baselines except the 32B models), demonstrating that strong prior reasoning distillation substantially compensates for smaller model size.
- RM-R1 produces highly interpretable, coherent reasoning traces with structured rubrics and explicit evaluations — enabling auditable reward assignment rather than opaque scalar scores.
- Ablations confirm that the two-stage pipeline (distillation → RL) is essential: RLVR alone without distillation underperforms, and distillation alone without RL overfits. CoR task-type classification provides additional gains over undifferentiated CoT.

---

### Implications
Framing reward modeling as a reasoning task rather than a classification or shallow generation task suggests that the quality of RLHF reward signals can be substantially improved without scaling up the reward model size, by instead deepening its reasoning process.
- This challenges the assumption that larger ScalarRMs (e.g., 70B–340B) are the natural path to better reward signals; a well-trained 14B–32B ReAsRM can exceed them, with the added benefit of interpretability.
- The CoR mechanism — which generates evaluation criteria on-the-fly rather than relying on fixed rubrics — points toward reward models that generalize across heterogeneous task types, a meaningful step toward unified reward modeling for diverse RLHF applications including chat safety, math, and code.
- The distillation-then-RL training recipe mirrors the DeepSeek-R1 recipe for general reasoning, validating that the same paradigm transfers to reward modeling specifically, potentially unifying the training methodology for both reasoning and evaluation models.
- For the code and math domains specifically, the correctness-first rollout (solving before judging) suggests reward models could serve as verifier-

## Key Claims

1. Scalar-based reward models are opaque, offering no intermediate reasoning steps to justify the model's decisions, which may limit their capacity to handle reasoning-intensive preference tasks.
2. Generative reward models provide transparency but their reasoning is often superficial, leading to suboptimal performance.
3. Integrating reasoning capabilities into reward modeling significantly enhances a reward model's interpretability and performance.
4. Solely applying reinforcement learning with verifiable rewards (RLVR) in reward modeling does not fully realize the model's reasoning capabilities.
5. Plain chain-of-thought reasoning falls short at perceiving fine-grained distinctions across different question types in reward modeling.
6. Reasoning distillation prior to RLVR is necessary to fully realize the reasoning capabilities of reward models.
7. Distilled reward models often overfit to specific patterns in training data, limiting their generalization ability for critical thinking.
8. RM-R1 achieves state-of-the-art performance on average across RewardBench, RM-Bench, and RMB benchmarks, outperforming models up to 70B, 340B, GPT-4o, and Claude by up to 4.9%.
9. RM-R1-DeepSeek-Distilled-Qwen-32B achieves the highest average score of 81.5 among all evaluated models.
10. The Chain-of-Rubrics mechanism has the model first classify each input as either Chat or Reasoning type, then apply type-specific evaluation strategies.

## Capabilities

- Reasoning Reward Models (ReasRMs) trained with distillation + RLVR generate explicit chain-of-thought preference judgments that outperform scalar models 2-10x their size and proprietary frontier models (GPT-4o, Claude) on preference evaluation benchmarks
- Chain-of-Rubrics (CoR) enables reward models to dynamically adapt their evaluation strategy by task type — generating explicit rubric criteria for chat/safety tasks and solving problems from scratch before judging for reasoning tasks
- Pre-trained reasoning models (e.g., DeepSeek-distilled Qwen variants) can be directly converted into high-performance reward models via RLVR alone — no additional distillation stage required — achieving SOTA reward modeling performance

## Limitations

- Scalar reward models are fundamentally opaque — they produce no intermediate reasoning steps to justify their decisions, limiting reliability on complex reasoning-intensive preference tasks
- Standard generative reward models (GenRMs) produce superficial reasoning that fails to reliably judge complex preferences, yielding suboptimal performance despite surface-level interpretability
- Applying RLVR alone to reward model training — without a prior distillation stage — fails to fully realize the model's reasoning capabilities for preference evaluation
- Distillation-only training for reward models causes overfitting to surface patterns in training traces, limiting generalization to novel preference scenarios and reasoning styles
- Plain chain-of-thought (CoT) reasoning is insufficient for reward modeling — it fails to perceive fine-grained distinctions across different question types, producing undifferentiated evaluation strategies
- Training high-quality reasoning reward models requires access to frontier 'oracle' models (o3, Claude-3-7-Sonnet) for distillation data generation — creating a cost and API-access barrier preventing self-sufficient open training pipelines
- RM-R1's binary task classifier (Chat vs. Reasoning) cannot handle ambiguous or mixed task types — prompts that require both stylistic quality and logical correctness receive a sub-optimal single-strategy evaluation
- RM-R1 RL training uses a binary ±1 correctness reward that cannot distinguish a model picking the right response through correct reasoning from one picking it via spurious correlation — quality of the reasoning chain receives no gradient signal
- Small reasoning reward models (7B) exhibit a sharp performance cliff relative to 32B variants — a 12-point average gap (69.2 vs 81.5) that is particularly pronounced on the RMB benchmark (55.1 vs 69.8)
- RM-R1 evaluation is restricted to static preference benchmarks — there is no assessment of reward model robustness when deployed inside an active RLHF training loop where the policy learns to exploit the reward model

## Bottlenecks

- Reward model opacity in scalar RMs prevents RLHF pipelines from debugging, validating, or trusting reward signals — the absence of interpretable reasoning makes systematic reward hacking detection and correction structurally impossible
- Training reasoning reward models requires frontier oracle models (o3, Claude-3-7-Sonnet) for distillation data — creating a dependency loop where only labs with access to top-tier proprietary models can bootstrap the next generation of open reward models

## Breakthroughs

- Compact open-weight reasoning reward models (7B–32B) trained via distillation + RLVR surpass both massive scalar models (340B) and proprietary frontier GenRMs (GPT-4o, Claude) on preference evaluation — demonstrating that interpretability and accuracy are not in tension

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/generative-reward-model-genrm|Generative Reward Model (GenRM)]]
- [[entities/group-relative-policy-optimization-grpo|Group Relative Policy Optimization (GRPO)]]
- [[entities/reinforcement-learning-from-human-feedback-rlhf|Reinforcement Learning from Human Feedback (RLHF)]]
- [[entities/reinforcement-learning-with-verifiable-rewards-rlvr|Reinforcement Learning with Verifiable Rewards (RLVR)]]
