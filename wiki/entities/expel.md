---
type: entity
title: ExpeL
entity_type: method
theme_ids:
- agent_evaluation
- agent_memory_systems
- agent_self_evolution
- agent_systems
- context_engineering
- evaluation_and_benchmarks
- knowledge_and_memory
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0006269904673380636
staleness: 0.0
status: active
tags: []
---
# ExpeL

ExpeL (Experience Pool Learning) is a prompt-based method for enabling LLM agents to learn from accumulated experience without modifying model parameters. Rather than fine-tuning weights, ExpeL maintains an external experience pool — a structured store of past trajectories, successes, and failures — which is retrieved at inference time to guide agent behavior. Its significance lies in demonstrating that meaningful behavioral adaptation is achievable purely through in-context learning, positioning it as an accessible baseline in the growing landscape of experience-driven agent systems.

**Type:** method
**Themes:** [[themes/agent_evaluation|Agent Evaluation]], [[themes/agent_memory_systems|Agent Memory Systems]], [[themes/agent_self_evolution|Agent Self-Evolution]], [[themes/agent_systems|Agent Systems]], [[themes/context_engineering|Context Engineering]], [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]], [[themes/knowledge_and_memory|Knowledge and Memory]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]

## Overview

ExpeL occupies a specific niche in the agent memory taxonomy: it is an instance of *experiential memory*, the class of memory mechanisms that "incrementally enhance problem-solving via task execution," as distinct from factual memory (which records knowledge from interactions) or working memory (which manages transient state). More precisely, it operates at the *token level* — storing past experience as persistent, discrete, externally accessible text that can be retrieved and injected into the agent's context window. This places ExpeL squarely within the retrieval-augmented paradigm: no gradient descent, no latent compression, just structured retrieval of prior experience at decision time.

The core tension ExpeL navigates is fundamental to all token-level memory systems: an LLM's context window is finite while the amount of potentially relevant experience is effectively unbounded. This constraint motivates the experience pool design — a curated, retrievable store rather than a raw log — but it also means ExpeL must make lossy decisions about what to retain, how to index it, and how much to surface per query.

## Competitive Landscape and Limitations

ExpeL's prompt-only approach has been surpassed by methods that combine experience with parameter updates. SkillRL, for instance, evolves an explicit skill library through reinforcement learning: starting from 55 skills (12 general, 43 task-specific), the library grows to 100 by end of training as the agent recursively abstracts reusable behaviors. On ALFWorld, SkillRL with Qwen2.5-7B-Instruct exceeds GPT-4o by 41.9% and Gemini-2.5-Pro by 29.6%, and achieves 89.9% success on ALFWorld and 72.7% on WebShop — margins that represent a decisive step beyond prompt-based baselines like ExpeL. The implication is direct: when parametric update is available, experience encoded in weights generalizes more robustly than experience retrieved into context.

The retrieval problem is a recurring structural weakness across experience-based systems. Memp, a closely related procedural memory approach, is limited to vector-similarity search with manually crafted keys, with BM25 and other potentially more precise retrieval methods unincorporated. ExpeL faces the same class of limitation — vector retrieval can surface superficially similar experiences while missing structurally relevant ones, and there is no established solution to this precision gap.

A second structural constraint is the dependency on explicit reward signals. Memp cannot judge task success in real-world settings where benchmark-supplied rewards are sparse or absent — and ExpeL, which relies on identifying successful vs. failed trajectories to populate its experience pool, carries the same implicit dependency. Without a reliable success signal, the experience pool degrades: failures may be stored as positive examples, or the pool may simply fail to grow.

Agent cost is a further consideration. Unlike pure LLMs whose cost is dominated by token generation, agents incur overhead from tools, memory retrieval, and retries. ExpeL's retrieval step adds latency and token cost on every query, which compounds at scale. An efficient agent is defined not as a smaller model but as a system that maximizes task success while minimizing resource consumption across memory, tool usage, and planning — a framing under which ExpeL's per-query retrieval overhead is a non-trivial liability.

## Open Questions

The core open question for ExpeL and its successors is whether token-level experiential memory can close the gap with parametric approaches, or whether parameter updates are structurally necessary for robust generalization. Related questions include: how should experience pools handle conflicting or contradictory past trajectories? Can retrieval be made precise enough to surface structurally relevant experience rather than surface-similar text? And how does the experience pool remain useful as the distribution of tasks shifts — does accumulated experience become stale or misleading over time?

More broadly, systems like MIRIX that retrieve from multiple memory databases and concatenate results suggest that comprehensive memory access may be preferable to selective retrieval — but at the cost of context bloat. ExpeL's selective pool design is a deliberate bet against comprehensiveness; whether that bet pays off depends heavily on retrieval quality that current vector-similarity methods do not reliably deliver.

## Related Sources

- SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning
- Toward Efficient Agents: Memory, Tool Learning, and Planning
- Memory in the Age of AI Agents
- Memp: Exploring Agent Procedural Memory

## Key Findings

## Limitations and Open Questions

## Relationships

## Sources
