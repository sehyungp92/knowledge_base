---
type: source
title: OpenAI o1 - the biggest black box of all. Let’s break it open.
source_id: 01KJVHZDJPDF3HWHB7Q6Y3J5NP
source_type: video
authors: []
published_at: '2024-09-28 00:00:00'
theme_ids:
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# OpenAI o1 - the biggest black box of all. Let's break it open.

> This source provides a detailed technical reconstruction of how OpenAI's o1 model was trained, arguing that the key leap from GPT-4 to o1 is an additional reinforcement learning stage that teaches the model to navigate a tree of thoughts using process and outcome reward models, a rumored QAR algorithm, and active learning to manage annotation cost. It situates o1 within the dual-axis scaling paradigm, showing how inference-time compute extends model capability beyond what training-time scaling alone can achieve.

**Authors:** (unlisted)
**Published:** 2024-09-28
**Type:** video

---

## Context and Framing

The source opens with a direct contrast between GPT-4 and o1 post-training pipelines. GPT-4's post-training consists of fine-tuning, instruct tuning, and [[themes/reinforcement_learning|RLHF]]. o1 includes all three of these plus an additional RL stage explicitly targeting reasoning, using the rumored QAR algorithm to navigate a tree of thoughts. This framing anchors the entire analysis: o1 is not a qualitatively different architecture, but a GPT-4 class model with a structurally richer post-training regime.

---

## The Cognitive Leap: System 1 to System 2

The source introduces a psychological lens that cuts through the technical detail. GPT-4 models are characterized as doing **System 1 thinking**: fast, instinctual, low-effort, prioritizing coherency over correctness. This is why they hallucinate. o1 models are doing **System 2 thinking**: slower, more deliberate, effortful, prioritizing correctness over coherency.

This is not just a metaphor. It reflects a structural difference in how the model generates outputs: GPT-4 follows a single chain of thought that may not be causally connected to its final answer, while o1 constructs a **tree of thoughts**, exploring multiple solution paths simultaneously, connecting chains across different levels, and selecting the best final answer through learned search behavior.

The distinction matters for understanding where each model breaks down. GPT-4's failure mode is confabulation (plausible but incorrect). o1's failure mode is computational cost and scope limitation: it can only reason through text, and its reasoning is currently characterized as "Level 2 of a potential Level 5."

---

## How o1 Was Trained

### The Generator and Outcome Reward Model

Training begins with the generator: a GPT-4 model prompted to produce multiple step-by-step solutions to mathematics problems. Solutions with correct final answers are filtered out and used to fine-tune the policy model on next-step prediction (given steps 1-3, predict step 4). The **outcome reward model (ORM)** evaluates whether the final step contains a correct answer. Because math problems have binary correctness, the ORM requires no additional human labeling.

### The Process Reward Model (PRM) and Phase 1 Dense Labeling

The ORM alone is insufficient for credit assignment across long reasoning chains. A **process reward model (PRM)** is needed to evaluate whether intermediate steps are correct. This requires human annotation at a granularity that makes the ORM look trivial.

In Phase 1, human labelers annotate every step and every completion (alternative expression of a step) in every solution as positive (correct step), negative (incorrect), or neutral (neither, unhelpful to progress). This "dense labeling" is expensive, slow, and not scalable. The source is explicit about this: the cost of the Phase 1 PRM is a significant constraint on the entire approach.

### Phase 2 Active Learning

Phase 2 reduces annotation burden through **active learning selection**: filtering for solutions that are most likely to fool the current PRM, specifically solutions that have a correct intermediate reasoning chain but an incorrect final answer. These adversarial edge cases are where the PRM is weakest, so labeling them is maximally informative per annotation dollar. The Phase 2 PRM trained on sparse but targeted labels outperforms a larger Phase 1 model trained on dense but undifferentiated data.

### The QAR Algorithm

The RL algorithm driving the full framework is the rumored **QAR algorithm**, understood to combine Q-learning (value estimation), A* pathfinding (heuristic search), and Monte Carlo Tree Search (MCTS, for lookahead, backtracking, and self-evaluation). This combination enables the model to navigate its tree of thoughts as a genuine search problem rather than a greedy walk. Critically, no official publication on QAR exists; the characterization is reconstructed from indirect evidence.

---

## Scaling and the Dual-Axis Paradigm

The source makes an important structural claim about [[themes/scaling_laws|scaling laws]]. Traditional neural scaling law analysis shows diminishing returns on training compute: each additional order of magnitude of training produces smaller accuracy gains. o1 breaks this pattern not by discovering a new training-time scaling regime, but by adding a second axis.

With [[themes/test_time_compute_scaling|inference-time compute]] scaling, the same trained model can achieve linear accuracy improvements on a logarithmic compute axis simply by spending more time navigating the tree. The longer o1 deliberates, the more likely it is to find the correct answer. This means a model trained to a fixed checkpoint can continue improving in capability simply by being given more inference budget, without any retraining.

The source notes a transparency gap in OpenAI's published scaling plots: the relationship between training-time efficiency and inference-time efficiency is not disclosed, making it impossible to assess whether test-time scaling represents a genuine new capability axis or primarily a way to amortize underinvestment in training.

---

## Capabilities

| Capability | Maturity | Notes |
|---|---|---|
| Tree-of-thought reasoning | Demo | Multi-path exploration via learned search over solution trees |
| System 2 test-time reasoning | Demo | Prioritizes correctness; spends deliberate inference compute |
| Inference-time compute scaling | Demo | Linear accuracy on logarithmic compute; extends trained model performance |
| Process reward models via process supervision | Narrow production | Human-annotated step-level labels enable intermediate credit assignment |
| Active learning for PRM annotation | Narrow production | Sparse targeted labeling reduces annotation burden while improving coverage |
| Dual-axis scaling | Demo | Training-time + inference-time compute combine to break diminishing returns |

See also: [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/reward_modeling|Reward Modeling]], [[themes/reasoning_and_planning|Reasoning and Planning]].

---

## Limitations and Open Questions

The source's technical depth makes its acknowledged constraints particularly credible.

**Modality constraint.** o1 is text-only. It cannot perform reasoning over visual inputs, despite GPT-4 being multimodal. The official o model roadmap hints at future vision capabilities, but at the time of publication this is a significant capability gap against competing multimodal reasoning systems.

**Reasoning is incomplete.** The source characterizes o1's reasoning as "Level 2 of a potential Level 5." Even within its domain of strength, the model will not always arrive at correct answers. System 2 thinking is probabilistically better, not infallible.

**Verifiability constraint.** The entire RL training pipeline, from the ORM to the QAR search algorithm, is designed for domains with objectively verifiable final answers. The source demonstrates the technique only on mathematics. Whether the framework extends to open-ended domains (writing, analysis, creative tasks) is not addressed and is structurally non-trivial: without binary correctness, the ORM cannot function, and the PRM labeling problem becomes far harder to define. This is the most significant architectural limitation discussed, as it bounds the scope of reasoning capabilities that can be acquired through this method.

**PRM annotation cost.** Phase 1 dense labeling is prohibitively expensive at scale. Phase 2 active learning mitigates this but does not eliminate it: human annotation of intermediate reasoning steps remains a bottleneck on expanding the technique to new domains or problem types.

**PRM adversarial vulnerability.** Process reward models can be fooled by high-quality intermediate steps that lead to wrong final answers. The active learning phase is designed precisely to address this, but it is a fundamental limitation of reward modeling: the reward model is itself a learned approximation and inherits its own failure modes.

**Transparency gaps.** The QAR algorithm has no official publication. The training-inference compute efficiency tradeoff is not disclosed. The source is reconstructing the training recipe from public signals, not verified documentation. Claims about QAR specifically should be treated as informed speculation.

See also: [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/pretraining_and_scaling|Pretraining and Scaling]].

---

## Key Bottleneck

The **verifiability constraint** is the load-bearing limitation in the entire framework. RL training for reasoning requires objectively verifiable final answers; this makes the approach directly applicable to mathematics, formal logic, and code, and structurally blocked for open-ended generation tasks. Resolving this bottleneck, likely requiring learned or LLM-judged reward models for open-ended domains, is a prerequisite for extending System 2 reasoning to the majority of tasks where language models are actually deployed. The source places this on a 3-5 year horizon.

> "the outcome reward model is relatively straightforward since a final answer is either correct or incorrect for a math problem so for here you don't require any additional labelling"

---

## Breakthroughs

**Test-time compute scaling breaks diminishing returns** (paradigm-shifting). The demonstration that inference-time compute adds a second scaling axis, achieving linear accuracy gains on logarithmic compute budgets, is a structural change to how capability improvements can be obtained. It decouples model performance from training cost.

**Process reward models via process supervision** (major). Human-annotated step-level labels provide dense intermediate reward signals for long-horizon reasoning chains, enabling credit assignment where sparse outcome signals fail.

**Tree-of-thought reasoning via RL** (major). RL training with QAR enables models to learn genuine search behavior over solution spaces rather than greedy token prediction.

**Active learning reduces PRM annotation burden** (notable). Filtering for adversarial edge cases enables sparse, targeted labeling that is both cheaper and more informative than dense uniform annotation.

---

## Themes

- [[themes/pretraining_and_scaling|Pretraining and Scaling]]
- [[themes/reasoning_and_planning|Reasoning and Planning]]
- [[themes/reinforcement_learning|Reinforcement Learning]]
- [[themes/reward_modeling|Reward Modeling]]
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]
- [[themes/scaling_laws|Scaling Laws]]
- [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Key Concepts

- [[entities/chain-of-thought|Chain of Thought]]
- [[entities/neural-scaling-laws|Neural Scaling Laws]]
- [[entities/outcome-reward-model|Outcome Reward Model]]
- [[entities/prm800k|PRM800K]]
- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
- [[entities/reinforcement-learning-from-human-feedback|Reinforcement Learning from Human Feedback]]
- [[entities/system-1-thinking|System 1 thinking]]
- [[entities/test-time-compute|Test-time compute]]
- [[entities/o1|o1]]
- [[entities/test-time-compute|test-time compute]]
