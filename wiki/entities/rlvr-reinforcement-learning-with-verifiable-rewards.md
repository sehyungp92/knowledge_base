---
type: entity
title: RLVR (Reinforcement Learning with Verifiable Rewards)
entity_type: method
theme_ids:
- adaptive_computation
- agent_self_evolution
- agent_systems
- ai_market_dynamics
- alignment_and_safety
- chain_of_thought
- finetuning_and_distillation
- frontier_lab_competition
- hallucination_and_reliability
- in_context_and_meta_learning
- latent_reasoning
- mathematical_and_formal_reasoning
- model_architecture
- multi_agent_coordination
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 7
sources_since_update: 0
update_count: 1
influence_score: 0.0026028201192343885
staleness: 0.0
status: active
tags: []
---
# RLVR (Reinforcement Learning with Verifiable Rewards)

Reinforcement Learning with Verifiable Rewards (RLVR) is the dominant post-training paradigm for instilling domain-specific reasoning skills in large language models, particularly mathematical and formal reasoning. Rather than relying on human preference labels, RLVR trains models against outcome signals that can be verified automatically: a math answer is correct or it isn't, code passes tests or it doesn't. This verifiability closes the reward-hacking loop that plagued earlier RL-from-human-feedback approaches, and the paradigm has become central to how frontier labs produce reasoning-capable models. Its significance lies not just in demonstrated performance gains but in the theoretical questions it has reopened about what RL actually teaches a model, and in the practical challenge of scaling it beyond the domains where verification is cheap.

**Type:** method
**Themes:** [[themes/adaptive_computation|Adaptive Computation]], [[themes/agent_self_evolution|Agent Self-Evolution]], [[themes/agent_systems|Agent Systems]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/alignment_and_safety|Alignment and Safety]], [[themes/chain_of_thought|Chain of Thought]], [[themes/finetuning_and_distillation|Finetuning and Distillation]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/hallucination_and_reliability|Hallucination and Reliability]], [[themes/in_context_and_meta_learning|In-Context and Meta-Learning]], [[themes/latent_reasoning|Latent Reasoning]], [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/model_architecture|Model Architecture]], [[themes/multi_agent_coordination|Multi-Agent Coordination]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/rl_theory_and_dynamics|RL Theory and Dynamics]], [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]

## Overview

RLVR is the current paradigm of training LLMs using reinforcement learning on verifiable outcome signals, applied during mid-training to instil domain-specific skills. The core idea is simple: generate candidate responses, check them against a ground-truth verifier, and use the resulting binary or scalar signal to update policy weights via an algorithm such as GRPO. Because the reward signal is externally grounded rather than learned, it avoids the distributional instability of reward model overoptimization that undermines RLHF at scale. The paradigm achieved widespread adoption after DeepSeek-R1 demonstrated that a relatively compact model trained primarily via RLVR could match or exceed much larger supervised baselines on mathematical benchmarks, catalyzing a wave of replication and extension work across frontier labs and academia.

## What RLVR Actually Teaches

The mechanism behind RLVR's gains is still contested. The most straightforward interpretation is that RL reinforces correct reasoning traces and suppresses incorrect ones, gradually shaping chain-of-thought behavior toward more reliable paths. A more skeptical reading is that the model is primarily learning to search more broadly at inference time, with the RL signal acting as a curriculum rather than instilling genuinely new capabilities. The distinction matters for generalization: if RLVR is primarily a search curriculum, gains should be narrow and domain-specific; if it is shaping internal reasoning structure, gains should transfer. Evidence from RLVE is relevant here. Training jointly across 400 diverse verifiable environments produces a 3.37% absolute average gain within approximately 1,100 H100 GPU hours, while continued RLVR training on the original narrow distribution yields only 0.49% with more than three times the compute. Expanding the collection of training environments consistently improves performance on held-out out-of-distribution tasks across all model types tested, which suggests the policy is learning something that transfers, not merely fitting a narrow verifier.

## Scaling Constraints and the Environment Bottleneck

The central practical limitation of RLVR is the availability of verifiable environments. Mathematical problem sets and code execution environments are the canonical cases because verification is deterministic and cheap. Outside those domains, verification either requires expensive human annotation, a learned reward model (reintroducing the instability RLVR was designed to avoid), or domain-specific infrastructure that may not exist. The cost of constructing high-quality training distributions is substantial: DeepMath-103K required roughly $138,000 USD and 127,000 GPU hours to build. The RLVE approach of constructing adaptive verifiable environments aims to reduce this cost substantially, but the fundamental constraint remains that verifiability is a prerequisite, not something the method can bootstrap around.

Compute efficiency is a related concern. GRPO, the most widely used RLVR algorithm, is rollout-intensive: obtaining a meaningful gradient update requires generating many candidate responses per prompt. This is tractable for math and coding with fast verifiers, but becomes expensive when environments require longer episodes, external tool calls, or slower verification pipelines. The rollout cost also scales poorly with response length, which matters as RLVR is increasingly applied to long chain-of-thought settings.

## The Prompt Optimization Challenge

An important result from GEPA complicates the standard framing of RLVR as the natural default for adapting LLMs to new tasks. GEPA, a reflective prompt evolution method that optimizes only the instruction prompt while leaving model weights fixed, outperforms GRPO by 6% on average and by up to 20% across six benchmarks, while using up to 35 times fewer rollouts. On four benchmarks evaluated with Qwen3-8B, GEPA matches GRPO's best validation score after between 243 and 1,179 rollouts, versus GRPO's 24,000. For IFBench specifically, GEPA finds optimal prompts after 678 rollouts achieving 38.61%, outperforming GRPO's 35.88% at 24,000 rollouts.

These results do not refute RLVR's value but they do narrow the scope of tasks where weight-updating RL is the right tool. GEPA's Pareto-based candidate selection yields +12.44% aggregate improvement versus +6.05% for greedy selection and +5.11% for beam search, and GEPA-optimized prompts transfer across model families: prompts optimized on the weaker Qwen3-8B achieve +9.00% improvement when applied to GPT-4.1 Mini without modification. The implication is that for many practical adaptation scenarios, the question is not how to run RLVR efficiently but whether RLVR is the right intervention at all. When task performance is primarily limited by instruction framing rather than weight-level capability gaps, prompt evolution is cheaper and often more effective.

## Extending RLVR to Non-Verifiable Domains

A significant frontier is extending the RLVR paradigm to domains where rewards are uncertain rather than binary. Beyond Binary Rewards addresses this by training models to reason about their own uncertainty as part of the reward signal, turning calibration into a verifiable property. This is a natural extension of the RLVR philosophy: if you can define a measurable outcome criterion, you can train against it. The broader challenge is that most interesting cognitive tasks, including open-ended writing, strategic reasoning, and cross-domain synthesis, resist reduction to a scalar outcome. This is not a temporary engineering problem but a fundamental constraint on where the paradigm applies.

RLMT (Reinforcement Learning with Model-rewarded Thinking), introduced in Language Models that Think, Chat Better, extends the approach to conversational settings by training models to generate long chain-of-thought reasoning before final answers using online RL with preference-based model rewards rather than hard verifiers. This loosens the verifiability constraint but partially reintroduces the reward model instability that RLVR was designed to circumvent. It demonstrates that the RLVR paradigm is being stretched toward less verifiable domains, with corresponding tradeoffs in training stability and interpretability of what the reward signal is measuring.

## Relationship to Chain-of-Thought and Latent Reasoning

RLVR has become the primary mechanism by which long chain-of-thought behavior is elicited and reinforced. The connection to [[themes/latent_reasoning|latent reasoning]] is direct: architectures that perform multiple forward passes before producing outputs, such as looped language models investigated in Scaling Latent Reasoning via Looped Language Models, are natural targets for RLVR because their multi-step computation can be treated as an internal rollout. The interaction with [[themes/adaptive_computation|adaptive computation]] is similarly tight: RLVR training naturally produces models that allocate more computation to harder problems, since longer chains-of-thought are rewarded when they produce correct answers. Whether this emergent compute allocation is principled or brittle under distribution shift is an open question.

## Open Questions

The core unresolved issues cluster around three areas. First, generalization: does RLVR instil transferable reasoning structure or narrow domain-fitting? The RLVE multi-environment results suggest genuine transfer is possible, but the mechanism is not understood. Second, the boundary with prompt optimization: as GEPA results show, for many adaptation tasks RLVR is not the most efficient intervention, and it is not yet clear how to predict in advance which regime a given task falls into. Third, extension beyond verifiable domains: the paradigm's defining strength is also its primary constraint, and the field has not yet converged on a principled approach to applying RL training to tasks where outcome quality is inherently ambiguous.

## Relationships

RLVR is the foundational method underlying most [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] work and intersects directly with [[themes/policy_optimization|policy optimization]] through algorithms like GRPO. Its application to chain-of-thought elicitation connects it to [[themes/chain_of_thought|chain of thought]] and [[themes/latent_reasoning|latent reasoning]] research. The environment construction problem links it to [[themes/reward_modeling|reward modeling]], particularly in non-verifiable domains. Its role in producing frontier reasoning models makes it central to [[themes/frontier_lab_competition|frontier lab competition]] dynamics. GEPA (GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning) provides the sharpest empirical challenge to its default status as the go-to adaptation method. RLVE (RLVE: Scaling Up Reinforcement Learning for Language Models with Adaptive Verifiable Environments) represents the most systematic attempt to address its scaling constraints through environment diversification. RLMT (Language Models that Think, Chat Better) represents its extension toward conversational and preference-based settings.

## Key Findings

## Limitations and Open Questions

## Sources
