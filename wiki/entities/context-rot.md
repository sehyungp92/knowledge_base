---
type: entity
title: Context rot
entity_type: theory
theme_ids:
- agent_memory_systems
- agent_systems
- ai_market_dynamics
- context_engineering
- frontier_lab_competition
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- reasoning_and_planning
- retrieval_augmented_generation
- software_engineering_agents
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0011358277492217687
staleness: 0.0
status: active
tags: []
---
# Context rot

> Context rot is the observed degradation in LLM output quality as the volume of tokens in the context window grows during a session. Coined on Hacker News by user Workaccount2 and later the subject of a technical report from Chroma, it represents one of the most practically consequential limitations of current transformer-based architectures — quietly undermining long-horizon tasks, multi-step agents, and retrieval pipelines that depend on large accumulated context.

**Type:** theory
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/context_engineering|context_engineering]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

Context rot names a simple but troubling empirical observation: LLM performance is not invariant to token count. As more tokens accumulate in the context window, models pay attention to less of them and reason less effectively — even when the theoretically relevant information is present. Chroma's technical report on "context rock" (a variant name used in the source) documents this in depth, framing it as a structural property of the attention mechanism rather than a quirk of specific models or prompts.

The significance of context rot extends well beyond long documents. It is a structural tax on any system that accumulates state over time — agentic loops, multi-turn conversations, tool-use scaffolds, and retrieval pipelines that concatenate retrieved chunks into a growing prompt. As these use cases have become central to how LLMs are deployed in 2025, context rot has moved from a footnote in evaluation methodology to an active engineering constraint.

## Why It Matters: Context Engineering as a Response

The practical response to context rot has crystallized under the label *context engineering* — the discipline of deciding what should be in the context window at each LLM generation step. As defined in Long Live Context Engineering, this involves both an inner loop (what belongs in context *this* generation) and an outer loop (how context should evolve across a session). Context Engineering for Agents frames it similarly: feeding a model "just the right context for the next step," a challenge especially acute in agentic settings where context accumulates unpredictably.

Context rot is what makes context engineering non-trivial. If attention were uniform across tokens, naive concatenation would suffice. Because it is not, every token added to the window is a potential source of noise that dilutes signal — making decisions about *what to omit* at least as important as decisions about what to include. This reframes RAG, summarization, and memory management not as retrieval problems but as attention economy problems.

## Architectural Workarounds: Recursive Language Models

The most technically ambitious response to context rot in the current literature comes from Recursive Language Models, which proposes bypassing the problem architecturally rather than managing it through prompt hygiene. The core insight is that arbitrarily long inputs should not be fed directly into the neural network; instead, an RLM initializes a REPL programming environment where the prompt is set as a variable, and the model writes code that decomposes and processes it incrementally.

The empirical results are striking. On BrowseComp-Plus (1K), RLM(GPT-5) achieves 91.3% accuracy while the base GPT-5 model scores 0.0% — a failure attributable directly to context window limitations. On OOLONG, RLM with GPT-5 and Qwen3-Coder outperform their base models by 28.4% and 33.3% respectively, *even on tasks within the model's nominal context window*, suggesting that context rot affects performance before the hard limit is reached. RLMs can successfully process inputs up to two orders of magnitude beyond model context windows, outperforming base models and common long-context scaffolds by up to 2x at comparable cost. A small-scale RLM (Qwen3-8B post-trained on only 1,000 samples) improves over its base by a median of 28.3% across four long-context tasks — evidence that the recursive decomposition strategy transfers across model scales.

## Open Questions and Limitations

The RLM approach reframes context rot as an engineering problem with a tractable solution, but several questions remain open. The REPL-based decomposition assumes tasks can be meaningfully broken into programmatically addressable subproblems — which may not hold for highly implicit or relational reasoning tasks where the relevant structure is only apparent from the full input. The approach also inherits the limitations of code generation: errors in decomposition or intermediate computation can compound in ways that are harder to diagnose than a simple long-context failure.

More fundamentally, context rot points to a limitation that context engineering can mitigate but not eliminate: transformer attention is not a scalable mechanism for arbitrary-length state. The field is effectively in a regime where the practical context limit — the length at which attention quality meaningfully degrades — is substantially shorter than the nominal context window. Benchmarks that report performance at headline context lengths may overstate real-world capability if they do not account for this degradation profile.

## Connections

Context rot intersects with several live threads in the broader AI landscape. The rise of reasoning models (see 2025: The Year in LLMs) increases per-query token budgets dramatically through chain-of-thought, making context rot more acute for extended reasoning traces. The context engineering discipline is partly a response to this: as models think longer, managing the accumulated scratchpad becomes as important as the reasoning itself. Meanwhile, the RLM work sits at the intersection of [[themes/test_time_compute_scaling|test_time_compute_scaling]] and [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], treating recursive decomposition as a form of structured compute investment rather than raw context extension.

The phenomenon also has quiet implications for [[themes/ai_market_dynamics|ai_market_dynamics]]: as context rot becomes better understood, it may shift competitive advantage away from raw context length (a headline spec) toward quality of attention and context management — a harder-to-measure but more practically significant capability.

## Key Findings

## Limitations and Open Questions

## Relationships

## Sources
