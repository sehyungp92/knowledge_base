---
type: entity
title: MEM1
entity_type: method
theme_ids:
- agent_evaluation
- agent_memory_systems
- agent_self_evolution
- agent_systems
- context_engineering
- evaluation_and_benchmarks
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.001185426126928551
staleness: 0.0
status: active
tags: []
---
# MEM1

> MEM1 is a reinforcement learning-trained method for long-horizon agents that replaces the conventional full-context prompt with a fixed-length internal state, enabling sequential task processing at constant memory cost. Rather than appending every past turn to the context window, the agent learns to compress relevant information into a structured `<IS></IS>` tag that overwrites itself each step, making both memory usage and inference time bounded regardless of task length.

**Type:** method
**Themes:** [[themes/agent_evaluation|agent_evaluation]], [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/context_engineering|context_engineering]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

The core problem MEM1 addresses is a well-known scaling pathology in transformer-based agents. Standard LLMs incur O(N²) compute cost (or O(N) with KV caching) and O(N) memory as context length grows, and most deployed systems simply append all past turns unconditionally, regardless of relevance. This leads to unbounded memory growth, rising computational costs, and eventually degraded reasoning as the context bloats past the model's effective attention range. The tension is sharpened by a fundamental mismatch: the context window is finite, but the information relevant to long-horizon tasks is not.

Prior mitigation strategies either truncate context (losing information) or introduce external memory modules such as summarizers or retrievers. The latter approach carries its own liability: these modules are trained separately and cannot be co-optimized with the agent's policy, creating a structural misalignment between what the memory system retains and what the agent actually needs.

MEM1 addresses both failure modes through a unified approach. The agent is trained end-to-end with reinforcement learning to maintain a single internal state element, structured using XML-style tags: `<IS>` for internal state and reasoning, `<query>` for environment queries, `<answer>` for responses, and `<info>` for external observations. At any given turn, the agent retains at most two `<IS>` elements, two `<query>` elements, and one `<info>` element. The internal state is not stored cumulatively; it is replaced, forcing the model to learn what is worth carrying forward and what can be discarded. The memory compression and reasoning behaviors emerge jointly from the same RL objective, avoiding the optimization gap of separate systems.

## Performance and Efficiency

The empirical results are striking on both the performance and efficiency axes. On a 16-objective multi-hop QA task, MEM1-7B improves task performance 3.5× while simultaneously reducing memory usage 3.7× compared to Qwen2.5-14B-Instruct, a model nearly twice its size. In absolute terms, MEM1 requires only 27.1% of the peak tokens and 29.3% of the total inference time of that baseline on the same task. The scaling behavior is the most diagnostic result: as the number of objectives increases, peak token usage for all baseline methods grows nearly linearly, while MEM1 maintains an almost constant peak token count. This is precisely the property that conventional full-context prompting cannot provide.

On the WebShop benchmark, MEM1-WebShop achieves a 2.8× improvement in peak token usage, 1.9× in dependency length, and 1.5× in inference time compared to AgentLM-7B. Its average final reward of 70.87 surpasses AgentLM-13B at 70.80, a model with twice the parameter count. The parameter efficiency gains here are notable, suggesting the RL training internalizes memory management in a way that partially substitutes for raw model capacity.

## Limitations and Open Questions

MEM1's current formulation carries meaningful constraints. Most critically, it assumes access to environments with well-defined and verifiable rewards. This holds for domains like QA, math, and web navigation, but breaks down for open-ended or creative tasks where reward signals are ambiguous, delayed, or noisy. The RL training loop cannot function without a reliable reward surface.

There is also the broader question of what the internal state actually encodes and whether the compression generalizes across task types without domain-specific retraining. The agent is trained to compress within the specific reward structure it was optimized against; it is not obvious that the compression policy transfers gracefully to qualitatively different task distributions.

More conceptually, MEM1 represents one point in a design space that the memory systems literature frames around three operators: formation (converting observations into memory candidates), evolution (integrating and consolidating candidates over time), and retrieval (reconstructing relevant state on demand). MEM1 collapses formation and evolution into a single in-context RL-trained operation and dispenses with explicit retrieval entirely. This is elegant but may not scale to tasks requiring recall of specific long-ago observations that cannot be carried in a bounded state.

## Relationships

MEM1 sits at the intersection of several active research threads. It is a direct response to the [[themes/long_context_and_attention|long context]] scaling problem and addresses the same efficiency concern catalogued in Toward Efficient Agents, which formalizes agent cost as a sum over token generation, tool calls, memory operations, and retries rather than token generation alone. The internal-state compression approach contrasts with retrieval-augmented memory systems covered in [[themes/retrieval_augmented_generation|RAG literature]], where external stores are queried rather than in-context state being overwritten. The RL training methodology connects to [[themes/rl_for_llm_reasoning|RL for LLM reasoning]], where policy gradient methods shape model behavior around verifiable outcome signals. The structured XML tagging convention situates MEM1 within broader [[themes/tool_use_and_agent_protocols|agent protocol]] design, where explicit format scaffolding guides model behavior during complex multi-step tasks.

The Memory in the Age of AI Agents survey provides useful framing: MEM1 is an example of a system where memory formation and evolution are co-trained with the agent policy rather than modularized, a design choice with clear efficiency advantages and equally clear generalization risks.

## Key Findings

## Sources
