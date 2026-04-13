---
type: entity
title: Cold-Start SFT
entity_type: method
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- chain_of_thought
- knowledge_and_memory
- mathematical_and_formal_reasoning
- multimodal_models
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- tool_use_and_agent_protocols
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0005684761127246204
staleness: 0.0
status: active
tags: []
---
# Cold-Start SFT

Cold-Start SFT is a supervised fine-tuning initialization stage that bootstraps reinforcement learning by providing the policy with a structured starting point before reward-driven optimization begins. Rather than training from a raw base model, RL pipelines incorporating Cold-Start SFT first expose the model to teacher-generated demonstrations — typically augmented with explicit reasoning traces, retrieved skills, or programmatic strategies — so that the policy enters the RL phase already capable of coherent behavior. The initialized model then doubles as the reference policy for KL regularization during RL, anchoring the optimization against excessive distributional drift. This two-role design (warm start + KL anchor) makes Cold-Start SFT a load-bearing component in several recent agent and reasoning frameworks.

**Type:** method
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/chain_of_thought|chain_of_thought]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/multimodal_models|multimodal_models]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/vision_language_models|vision_language_models]]

## Overview

Cold-Start SFT addresses a practical failure mode in RL-from-scratch training: without a competent initialization, the policy may explore so chaotically early in training that reward signals are too sparse to learn from efficiently. By generating skill-augmented reasoning traces via a teacher model — demonstrations that show not just *what* to do but *how to retrieve, interpret, and apply relevant skills* — the SFT phase instills procedural scaffolding before reward gradients take over.

Two concrete instantiations illustrate the pattern. In SkillRL, Cold-Start SFT equips the agent with traces that already incorporate skill lookup and application logic; the resulting policy enters GRPO training with an initial skill library of 55 skills (12 general, 43 task-specific) and the capability to reason over them. In CodeVision, the SFT cold-start stage teaches the model to reason through visual problems via programmatic strategy traces before GRPO training refines this with a dense, multi-component reward (outcome reward + strategy-shaping process reward + constraint penalties).

## Key Findings

The downstream results from these frameworks suggest Cold-Start SFT provides genuine leverage rather than mere convenience. SkillRL with Qwen2.5-7B-Instruct, initialized via Cold-Start SFT, outperforms GPT-4o by 41.9% and Gemini-2.5-Pro by 29.6% on ALFWorld — a result explicitly attributed to effective skill learning compensating for model scale disadvantage. More directly, SkillRL achieves a 12.3% absolute improvement over vanilla GRPO on ALFWorld (77.6% → 89.9%), with the skill-augmentation mechanism — seeded by the SFT phase — as the distinguishing factor. The dynamic skill library grows from 55 to 100 skills during RL training, with the SFT-initialized policy providing the retrieval and reasoning competence needed to exploit newly evolved skills.

The CodeVision results tell a complementary story in the multimodal domain. CodeVision-7B achieves 73.4 on transformed OCRBench (+17.4 over the Qwen2.5-VL-7B base) and 60.1 on MVToolBench, nearly doubling Gemini 2.5 Pro's 32.6. The cold-start traces, which demonstrate programmatic thinking strategies for visual reasoning, appear to be what allows GRPO to find useful reward signal in a domain where base models are surprisingly brittle — simple rotation and flip operations alone reduce standard MLLM performance by up to 80%.

A related finding from Beyond the 80/20 Rule situates Cold-Start SFT within a broader theory of RL efficiency: only the top 20% highest-entropy "forking" tokens drive meaningful policy gradient updates, with full-gradient training on the remaining 80% providing comparable performance to selective updates on Qwen3-8B. This implies that what Cold-Start SFT actually contributes may be precisely the shaping of these high-entropy decision points — teaching the model *where* the hard choices are and giving it structured priors about how to resolve them, before RL refines those priors against reward.

The contrast with MemRL is instructive: updating only the memory bank via RL while keeping the policy frozen yields just 21.4% on ALFWorld, far below SkillRL's 89.9%. This suggests the SFT-initialized policy itself — not just the skill library — must be jointly trained for the system to generalize.

## Limitations and Open Questions

The dependency structure introduces a critical weakness: Cold-Start SFT inherits the teacher model's coverage gaps and systematic biases. If the teacher generates skill-augmented traces that systematically miss certain task types or retrieve skills inappropriately, the SFT model will enter RL with structured misinformation rather than structured ignorance — potentially harder to overcome than random initialization in those regimes.

It remains unclear how sensitive RL outcomes are to the quality and diversity of the SFT corpus versus the SFT training duration. The dual role of the SFT model as both initialization and KL anchor creates a tension: a more expressive initialization may be harder to constrain via KL regularization without either over-constraining exploration or allowing excessive drift. The optimal calibration of KL penalty relative to SFT corpus quality is not established.

There is also an unresolved question about task generalization. The SkillRL results demonstrate impressive in-distribution performance, but the skill library evolves from a manually seeded initial set. How Cold-Start SFT should be structured for genuinely open-ended task distributions — where the teacher cannot anticipate the relevant skill space — remains an open design problem. The recursive skill evolution mechanism partially addresses this, but the initialization still anchors what can be discovered.

## Relationships

Cold-Start SFT is architecturally upstream of [[themes/reinforcement_learning|RL fine-tuning]] and serves as the reference policy for [[themes/rl_theory_and_dynamics|KL regularization]]. It is closely related to [[themes/chain_of_thought|chain-of-thought distillation]] (teacher traces are a form of reasoning-trace supervision) and connects to [[themes/agent_memory_systems|agent memory systems]] through the skill library it initializes. The programmatic visual reasoning variant in CodeVision links it to [[themes/vision_language_models|vision-language models]] and [[themes/multimodal_models|multimodal reasoning]]. The entropy-token finding from Beyond the 80/20 Rule provides a theoretical lens for understanding *what* the SFT phase is actually teaching, connecting it to ongoing work on [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] dynamics.

## Sources
