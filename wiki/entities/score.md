---
type: entity
title: SCoRe
entity_type: method
theme_ids:
- agent_systems
- chain_of_thought
- finetuning_and_distillation
- in_context_and_meta_learning
- multi_agent_coordination
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0010936679327234764
staleness: 0.0
status: active
tags: []
---
# SCoRe

SCoRe (Self-Correction via Reinforcement Learning) is a two-stage multi-turn online RL method that trains language models to genuinely self-correct their own outputs using only self-generated data — no oracle feedback, no external verifier at test time. Introduced at ICLR 2025 and demonstrated on Gemini 1.0 Pro and 1.5 Flash, SCoRe is notable for being the first approach to achieve a significantly positive intrinsic self-correction delta, resolving a longstanding finding that LLMs cannot reliably improve their answers through self-reflection alone.

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

The central problem SCoRe addresses is well-established: intrinsic self-correction — where a model revises its answer using only its own judgment, without ground-truth feedback — has consistently failed in modern LLMs. Prior attempts using supervised fine-tuning on offline correction traces proved insufficient, as the model would either collapse to producing the correct answer directly on the first attempt (eliminating the need for correction) or fail to learn meaningful revision behavior.

SCoRe solves this through a deliberate two-stage online RL training procedure. **Stage I** fine-tunes the model to produce high-reward second attempts while keeping the first-attempt distribution anchored close to the base model via KL divergence regularization. This decoupling is critical: it prevents the model from learning to "cheat" by front-loading all effort into attempt one, which would make Stage II degenerate. **Stage II** then jointly optimizes both attempts using a shaped reward that explicitly rewards *self-correction progress* — improvement from attempt one to attempt two — rather than just final correctness. This biases the model toward genuine revision rather than independent re-solving.

The result is a single model that, at test time, produces a first response and then meaningfully critiques and improves it without any external signal. Because training runs entirely on self-generated rollouts, SCoRe avoids dependence on human-curated correction demonstrations.

## Key Findings

SCoRe's empirical results are striking precisely because they contradict the prior consensus. On MATH, SCoRe achieves a **4.4% intrinsic self-correction delta** (Δ(t1,t2)) with Gemini 1.0 Pro — described by the authors as the first significantly positive delta ever recorded in this setting. Against the base Gemini 1.5 Flash model, SCoRe improves Δ(t1,t2) by **15.6%** and Accuracy@t2 by **23.0%** on MATH, and by **9.1%** on HumanEval. Generalization is particularly notable: SCoRe trained only on MBPP achieves a **12.2% intrinsic self-correction delta on HumanEval**, roughly 9% higher than the base model — suggesting the correction behavior transfers across coding distributions rather than being narrowly benchmark-fitted.

These results reframe self-correction not as an emergent property of scale or prompting, but as a learnable behavior that requires careful reward design and training dynamics to acquire. The failure of SFT baselines indicates that the signal is too sparse or too easily gamed by naive approaches.

## Connections to Broader Frameworks

SCoRe sits at the intersection of several active research directions. The Optimizing Test-Time Compute via Meta Reinforcement Fine-Tuning paper formalizes test-time compute optimization as a meta-RL problem — a framing that directly encompasses multi-turn self-correction as a special case. That work's progress dense reward bonus (quantifying improvement in the likelihood of eventual success per output block) is conceptually related to SCoRe's Stage II reward shaping, which rewards incremental correction progress rather than terminal outcomes. Both approaches share the insight that dense, trajectory-aware reward signals are necessary to learn useful iterative behaviors.

The Adaptation of Agentic AI source introduces a complementary inversion: rather than adapting the agent to use tools better, adapting tools to serve a fixed frozen agent. SCoRe sits at the opposite end — it adapts the model itself to produce and consume its own corrections — but both approaches acknowledge the same underlying problem: multi-step agentic behavior is difficult to instill through single-turn supervision.

## Limitations and Open Questions

The most significant constraint on interpreting SCoRe's results is **scope**. Evaluations are on mathematical reasoning (MATH) and code (HumanEval, MBPP) — domains with ground-truth verifiable outcomes and relatively clean reward signals. Whether the self-correction gains transfer to open-ended reasoning, factual claims, or domains without clear correctness criteria is unknown.

The KL regularization in Stage I introduces a tradeoff: keeping the first-attempt distribution close to the base model prevents collapse but may also cap how much the model can improve its initial response. The interaction between Stage I anchor strength and Stage II correction quality is likely sensitive to hyperparameter choices not fully explored in the paper.

More fundamentally, SCoRe's self-correction operates within a **single model's hypothesis space**. If the base model's first attempt reflects a systematic misunderstanding, the correction mechanism trained on that model's own outputs may lack the perspective needed to escape the error. This is structurally distinct from multi-model critique systems, where a separate model provides an independent view. SCoRe is computationally cheaper and avoids coordination overhead, but pays for this with potential blind spots that are invisible from within the model's own distribution.

The relationship between SCoRe's approach and test-time compute scaling also merits scrutiny. SCoRe demonstrates that *trained* multi-turn revision is far more effective than *prompted* self-reflection — but it requires substantial RL training compute to achieve this. Whether the inference-time cost of generating two attempts is competitive with alternative test-time compute strategies (e.g., best-of-N, tree search) at matched total compute remains an open empirical question.

## Related Entities

- Training Language Models to Self-Correct via Reinforcement Learning — primary source
- Optimizing Test-Time Compute via Meta Reinforcement Fine-Tuning — formalizes the meta-RL framing that contextualizes SCoRe
- Adaptation of Agentic AI — contrasting paradigm (tool adaptation vs. model adaptation)
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] — parent research direction
- [[themes/test_time_compute_scaling|Test-Time Compute Scaling]] — broader context for multi-attempt inference

## Relationships

## Sources
