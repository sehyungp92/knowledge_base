---
type: entity
title: ReTool
entity_type: method
theme_ids:
- agent_systems
- finetuning_and_distillation
- in_context_and_meta_learning
- mathematical_and_formal_reasoning
- multi_agent_coordination
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0002276976682024652
staleness: 0.0
status: active
tags: []
---
# ReTool

ReTool is a reinforcement learning framework that integrates real-time code execution with outcome-driven RL to train large language models to autonomously learn strategic tool invocation. Developed on top of DeepSeek and Qwen backbones, it achieved state-of-the-art results on mathematical competition benchmarks at the time of its release, positioning it as a significant demonstration that RL-trained tool use can substantially outperform both text-only reasoning and supervised fine-tuning approaches.

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

ReTool's core contribution is training models not merely to execute tools when prompted, but to reason about *when* tool invocation is warranted — a distinction that separates strategic tool use from mechanical function calling. The framework combines a cold-start supervised fine-tuning phase with subsequent outcome-driven RL, using a deliberately minimal reward signal: binary (+1 correct / -1 incorrect) with no intermediate code executability reward. This design choice reflects a deliberate stance against reward hacking — by removing partial credit for syntactically valid but semantically useless code, the framework encourages more diverse and genuinely effective problem-solving behaviors.

The training dynamics are notably efficient. Using a Qwen2.5-32B-Instruct backbone, ReTool reaches 67.0% on AIME 2024 in just 400 training steps, compared to over 1,000 steps for the text-based RL baseline that tops out at 40.0%. With a DeepSeek-R1-Distill-Qwen-32B backbone in extended settings, performance reaches 72.5% on AIME 2024. The KL coefficient is set to 0.0 during RL training, meaning there is no explicit penalty for diverging from the reference policy — a configuration that prioritizes performance over distributional stability.

## Key Findings

ReTool's results expose a sharp capability gap between text-only and tool-augmented RL. The cold-start SFT model (no RL) achieves 40.9% on AIME 2024, nearly identical to the text-based RL ceiling of 40.0% — suggesting that supervised imitation of tool use alone is insufficient, and that the RL phase is what actually unlocks strategic invocation. The gap between SFT-only and RL-trained ReTool (67.0%) is thus attributable almost entirely to RL over real execution feedback, not to the tool format itself.

The results also provide external validation. ReTool (Qwen2.5-32B-Instruct) surpasses s1-32B by 10.3% on AIME 2024 and gains 11.4% over OpenAI o1-preview on AIME 2025. The DeepSeek-R1-Distill variant surpasses o1-preview by 27.9 percentage points on AIME 2024. These comparisons situate ReTool within a broader competitive landscape where RL-trained reasoning models are rapidly closing the gap with frontier closed-source systems on structured mathematical tasks.

ReTool's trajectory is consistent with a broader pattern identified in OpenAI's o3: Over-optimization is back and weirder than ever: o3 was similarly trained with tools through RL, teaching it to reason about *when* to use them rather than just *how*. Bob McGrew's framing — that intelligence is no longer the primary constraint and the new frontier is reliable external-world interaction — directly contextualizes what ReTool is optimizing for. The benchmark results suggest that reliably knowing when to invoke a code interpreter is itself a learnable, RL-improvable capability.

## Connections and Context

ReTool sits within a cluster of methods exploring outcome-based RL for agentic adaptation. Adaptation of Agentic AI describes the DeepSeek-R1 framework as a major breakthrough showing that RL with verifiable reward can enhance reasoning in large agents — ReTool is effectively an instantiation of this insight applied specifically to tool-augmented settings. The same survey also describes the T2 paradigm (adapting tools to serve a frozen agent rather than adapting the agent to use tools), which represents a conceptual inversion of ReTool's approach: where ReTool trains the agent, T2 trains the environment. These are not competing methods so much as complementary strategies along the A1/A2/T2 adaptation axis.

The comparison to TextGrad, which improves GPT-4o's multi-tool CHAMELEON agent by 7.7% through gradient-based optimization in natural language, is also illuminating: ReTool achieves far larger gains through RL on execution feedback rather than gradient signals through text, suggesting that hard execution outcomes are a stronger training signal than soft textual gradients for tool-use tasks.

## Limitations and Open Questions

Several aspects of ReTool invite scrutiny. The KL coefficient of 0.0 removes the usual regularization that prevents the policy from drifting arbitrarily far from the reference model — this may be acceptable for a bounded benchmark like AIME but raises questions about robustness and generalization beyond the training distribution. The binary reward without executability feedback reduces one form of reward hacking but does not eliminate it; the model could still learn to invoke tools in superficially plausible but shallow ways that happen to produce correct answers on competition math without generalizing.

The benchmark focus is narrow: AIME is a structured mathematical domain with deterministic verifiable outcomes, which is nearly ideal for outcome-based RL. Whether the same training recipe transfers to less verifiable domains — open-ended research, multi-step tool use with ambiguous success criteria, or tasks requiring tool *composition* rather than single invocations — remains an open question. The broader over-optimization concern raised in OpenAI's o3: Over-optimization is back and weirder than ever applies here: when the optimizer is stronger than the reward signal, it will find the gaps.

## Relationships

## Sources
