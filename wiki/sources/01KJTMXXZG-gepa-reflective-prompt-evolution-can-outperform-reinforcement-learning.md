---
type: source
title: 'GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning'
source_id: 01KJTMXXZGZQAMKDR6N10JMD1M
source_type: paper
authors:
- Lakshya A Agrawal
- Shangyin Tan
- Dilara Soylu
- Noah Ziems
- Rishi Khare
- Krista Opsahl-Ong
- Arnav Singhvi
- Herumb Shandilya
- Michael J Ryan
- Meng Jiang
- Christopher Potts
- Koushik Sen
- Alexandros G. Dimakis
- Ion Stoica
- Dan Klein
- Matei Zaharia
- Omar Khattab
published_at: '2025-07-25 00:00:00'
theme_ids:
- agent_systems
- in_context_and_meta_learning
- post_training_methods
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning

GEPA (Genetic-Pareto) introduces a prompt-space optimizer for compound AI systems that replaces weight-space reinforcement learning with natural language reflection over execution and evaluation traces. By evolving prompts rather than model weights and using a Pareto-based candidate selection strategy to escape local optima, GEPA outperforms GRPO (a leading RLVR method) on 5 of 6 benchmarks while using up to 35 times fewer rollouts, and more than doubles the aggregate gains of the leading prompt optimizer MIPROv2. The work challenges two prior consensus views: that RL is necessary for hard task adaptation, and that few-shot optimization dominates instruction-only optimization.

**Authors:** Lakshya A Agrawal, Shangyin Tan, Dilara Soylu, Noah Ziems, Rishi Khare, Krista Opsahl-Ong, Arnav Singhvi, Herumb Shandilya, Michael J Ryan, Meng Jiang, Christopher Potts, Koushik Sen, Alexandros G. Dimakis, Ion Stoica, Dan Klein, Matei Zaharia, Omar Khattab
**Published:** 2025-07-25
**Type:** Paper

---

## Motivation

[[themes/reinforcement_learning|Reinforcement learning]] methods like GRPO are severely sample-inefficient for adapting LLMs to downstream tasks, typically requiring tens of thousands to hundreds of thousands of rollouts. This bottleneck becomes acute for compound AI systems where tool calls are expensive, inference budgets are constrained, or the target model cannot be finetuned at all (as is the case for large closed-source APIs). The prior best prompt optimizers (MIPROv2, TextGrad, APO) fell short of RL performance on harder tasks, relied on greedy or beam-search candidate selection strategies that stalled in local optima, and produced long, costly prompts through joint instruction-and-few-shot optimization.

---

## Approach

GEPA treats prompt optimization as an evolutionary search over natural language, driven by reflection on full execution traces rather than scalar reward gradients.

**Reflective credit assignment.** Each optimization step serializes a full rollout (reasoning chains, tool calls, compiler errors, rubric feedback) into natural language and feeds it to a reflection LM. The LM performs implicit credit assignment across modules in the compound system and proposes targeted prompt updates. This contrasts with scalar RL, which compresses rich trajectory information into a single number before any learning occurs.

**Extended feedback function.** GEPA replaces the standard reward function with a feedback function `µf` that captures domain-specific textual diagnostics (compiler errors, code evaluation traces, rubric explanations) alongside the scalar score. This richer signal is the source of much of GEPA's sample efficiency advantage: it is most effective when evaluation naturally produces interpretable intermediate outputs.

**Pareto-based candidate selection.** Rather than always evolving from the globally best candidate, GEPA maintains a Pareto frontier of candidates that are each optimal on at least one training instance, then samples stochastically weighted by coverage frequency. This preserves diverse optimization lineages and provides a +7.33% aggregate advantage over greedy selection and +6.4% over beam search. The qualitative difference is visible in search trees: greedy strategies stall after one iteration; Pareto-based search maintains balanced, exploratory branching.

**System-Aware Merge (GEPA+Merge).** A secondary crossover strategy identifies distinct lineages that evolved different modules and assembles a new candidate by taking the best version of each module from separate lineages, capturing complementary strategies developed in parallel. Performance is model-dependent: it improves GPT-4.1 Mini results but degrades Qwen3-8B performance with the same hyperparameters.

---

## Results

### vs. Reinforcement Learning (GRPO)

On six benchmarks using Qwen3-8B and GPT-4.1 Mini, GEPA outperforms GRPO (24,000 rollouts) by 6% on average and by up to 20% on individual tasks (HotpotQA: +19%, HoVer: +13.66%, PUPA: +5.19%). GEPA matches GRPO's best validation score using only 243, 402, 330, 1143, 1179, and 306 total rollouts across six tasks, achieving up to 78x greater sample efficiency. When only training rollouts are counted (excluding validation), GEPA reaches optimal performance with 79 to 737 examples, and as few as 6 training rollouts on one task.

The sole exception is AIME-2025 with Qwen3-8B, where GRPO scores 38% vs. GEPA's 32%. This is the only benchmark where weight-space RL outperforms prompt-space optimization, and it marks a meaningful boundary: deep mathematical reasoning under strict output constraints may still require gradient-level adaptation.

### vs. Prompt Optimizers (MIPROv2, TextGrad, APO)

GEPA more than doubles MIPROv2's aggregate gains across all six benchmarks: +13.33% vs. +5.64% on GPT-4.1 Mini, and +9.62% vs. +2.61% on Qwen3-8B. GEPA achieves this with instruction-only optimization, overturning the prior consensus that few-shot example optimization dominates. GEPA prompts are up to 9.2x shorter than MIPROv2's, reducing inference cost and latency.

### Cross-model generalization

GEPA-optimized prompts transfer across model families. Prompts optimized on Qwen3-8B, when applied to GPT-4.1 Mini without modification, achieve +9.00% aggregate improvement, outperforming MIPROv2 (+5.64%), TextGrad (+6.11%), and Trace (+3.27%) that were all optimized directly on the target model. This is a strong practical signal: GEPA optimization can be performed on cheaper models and transferred to frontier deployments.

### Inference-time kernel optimization

As an inference-time search strategy for hardware kernel generation, GEPA raises mean vector utilization on AMD XDNA2 NPU kernels from 4.25% (unaided sequential refinement) to 30.52%, with individual kernels reaching 70%. On CUDA kernel generation (KernelBench), GEPA raises GPT-4o's near-zero fast@1 score to above 20%. These are early results on narrow platforms; generalization to general-purpose code optimization is unverified.

### Adversarial prompt discovery

With an inverted reward, GEPA discovers universal, task-preserving instruction-level perturbations that reduce GPT-5 Mini's pass@1 on AIME-2025 from 76% to 10%. Manual inspection shows the adversarial instruction caused the model to end most responses with a literal placeholder (`### <final answer>`), revealing brittle interaction between irrelevant distractors and strict formatting constraints in frontier models.

---

## Capabilities

- [[themes/in_context_and_meta_learning|Reflective prompt optimization]] achieving task adaptation that surpasses GRPO using up to 35x fewer rollouts, across six diverse benchmarks (maturity: demo)
- Cross-model prompt transfer: prompts optimized on weaker models outperform baselines optimized on the target model (maturity: demo)
- Instruction-only optimization now outperforms joint instruction-and-few-shot optimization, with lower generalization gaps and up to 9.2x shorter prompts (maturity: demo)
- Inference-time code search for hardware kernel generation, reaching 30.52% mean vector utilization on AMD NPU vs. 4.25% baseline (maturity: research only)
- Automated adversarial prompt discovery via inverted-reward evolution, enabling principled robustness evaluation of frontier models (maturity: demo)

---

## Limitations and Open Questions

**Hard ceiling from frozen weights.** GEPA operates exclusively in prompt space; it cannot update model weights and is therefore bounded by the capability envelope of the underlying model. It cannot acquire genuinely new knowledge or behaviors that the base model does not already possess.

**Mathematical reasoning gap.** On AIME-2025 with Qwen3-8B, GRPO scores 38% vs. GEPA's 32%. Deep mathematical reasoning under strict output constraints appears to be a regime where gradient-level weight adaptation still has a structural advantage over prompt evolution.

**Dependence on rich textual feedback.** GEPA's sample efficiency advantage is conditioned on evaluation traces that produce interpretable intermediate outputs: compiler errors, rubric explanations, code diagnostics. In purely numeric reward settings with no natural language structure, GEPA's key mechanism is compromised.

**Validation-set budget dominance.** The majority of GEPA's total rollout budget is consumed by validation-set scoring for candidate selection, not by learning. Training rollouts alone require only 79 to 737 examples. This suggests the selection mechanism is the primary cost driver and that dynamic or learned validation strategies could yield further efficiency gains.

**Merge instability across models.** The System-Aware Merge crossover improves GPT-4.1 Mini results but degrades Qwen3-8B performance with fixed hyperparameters. Optimal budget allocation between exploration and crossover is an open hyperparameter problem.

**Kernel generation scope.** Inference-time code search results cover only two narrow hardware platforms (AMD XDNA2, NVIDIA V100) and are explicitly flagged by the authors as preliminary. Generalization to broader code optimization tasks is uncharacterized.

---

## Implications

**Language as a training medium.** Natural language reflection over trajectories is more sample-efficient than scalar reward gradients for LLMs. This suggests that the interpretability of language is itself a form of trainable signal: prompt-space optimization may increasingly rival weight-space RL for real-world adaptation scenarios where rollouts are expensive and feedback is rich.

**Instruction-following quality shift.** The finding that instruction-only optimization now outperforms joint instruction-and-few-shot optimization signals a qualitative shift in LLM capabilities. Modern models' improved instruction-following and in-context self-reflection reduce the marginal value of example-based prompting. Few-shot augmentation may be approaching a point of diminishing returns for sufficiently capable base models.

**Accessible adaptation for closed-source models.** Because GEPA requires no gradient access, it opens practical adaptation pathways for the largest frontier models, which expose only inference endpoints. The cross-model transfer finding further suggests that expensive target-model rollouts may not even be necessary during optimization.

**Brittleness as a robustness signal.** The adversarial prompt discovery application surfaces a structural vulnerability in frontier models: irrelevant distractors co-occurring with strict formatting constraints can catastrophically degrade performance. GEPA's ability to discover these systematically, rather than through manual red-teaming, has direct implications for [[themes/post_training_methods|post-training evaluation]] and safety stress-testing.

---

## Related Themes

- [[themes/agent_systems|Agent Systems]]
- [[themes/in_context_and_meta_learning|In-Context and Meta-Learning]]
- [[themes/post_training_methods|Post-Training Methods]]
- [[themes/reinforcement_learning|Reinforcement Learning]]
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]

## Key Concepts

- [[entities/dspy|DSPy]]
- [[entities/grpo-group-relative-policy-optimization|GRPO (Group Relative Policy Optimization)]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/rlvr-reinforcement-learning-with-verifiable-rewards|RLVR (Reinforcement Learning with Verifiable Rewards)]]
- [[entities/textgrad|TextGrad]]
