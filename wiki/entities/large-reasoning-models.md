---
type: entity
title: Large Reasoning Models
entity_type: entity
theme_ids:
- agent_systems
- chain_of_thought
- knowledge_and_memory
- mathematical_and_formal_reasoning
- multi_agent_coordination
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00013115322307186543
staleness: 0.0
status: active
tags: []
---
# Large Reasoning Models

> Large Reasoning Models (LRMs) are a class of LLMs trained through supervised fine-tuning and reinforcement learning with verifiable rewards, distinguished by their capacity for extended chain-of-thought deliberation before producing answers. They represent a qualitative shift from standard instruction-tuned models: rather than pattern-matching to a response, they allocate test-time compute to iterative self-critique, uncertainty resolution, and multi-step planning. Their significance lies in demonstrating that reasoning quality scales with deliberation depth, not just parameter count, and in opening new frontiers for augmentation with retrieval, tool use, and multi-agent coordination.

**Type:** entity
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/chain_of_thought|Chain of Thought]], [[themes/knowledge_and_memory|Knowledge and Memory]], [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/multi_agent_coordination|Multi-Agent Coordination]], [[themes/policy_optimization|Policy Optimization]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/rl_theory_and_dynamics|RL Theory and Dynamics]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]

---

## Overview

Large Reasoning Models emerged from applying reinforcement learning with verifiable rewards to language models, a trajectory with deep roots in game-playing AI. The landmark results of AlphaGo and AlphaZero demonstrated that agents learning exclusively through self-play and reward feedback could surpass world champions in Go, chess, shogi, and Stratego, establishing the foundational proof that RL-shaped deliberation produces qualitatively superior reasoning under structured feedback. LRMs operationalize this insight for language: the model learns, via outcome-supervised RL, to extend its reasoning chain until it converges on verifiable correctness. GRPO, a key training algorithm in this space, is a critic-free modification of PPO that replaces the generalized advantage estimator with group-relative normalization, reducing variance and accelerating training without requiring a separate value model.

The defining behavioral signature of LRMs is their extended, often self-correcting internal monologue. QwQ-32B-Preview, a prominent open-weight example with 32 billion parameters, consistently outperforms larger instruction-tuned models such as Qwen2.5-72B and Llama3.3-70B on complex reasoning benchmarks in direct settings. This inversion of the parameter-count hierarchy, smaller reasoning model beating larger standard model, is one of the more striking empirical findings in recent AI research and is attributed directly to the effectiveness of the o1-style long chain-of-thought training regime.

Current capabilities are classified as **narrow production** maturity: LRMs show measurable, reliable advantage over standard LLMs on medium-to-high complexity reasoning tasks (math, code, multi-hop QA, scientific reasoning), but their strengths are concentrated in structured, verifiable domains rather than open-ended or socially grounded tasks.

---

## Key Findings

### Strengths and Performance Profile

The performance advantages of LRMs are substantial and well-documented. On five challenging reasoning benchmarks, Search-o1 (built on QwQ-32B-Preview) exceeds the reactive agent baseline RAgent-QwQ-32B by 4.7% and vanilla QwQ-32B by 3.1% on average, while outperforming non-reasoning models Qwen2.5-32B and Llama3.3-70B by 44.7% and 39.3% respectively. On multi-hop QA tasks, the gains from combining LRM reasoning with structured retrieval are even larger: Search-o1 exceeds the naive RAG baseline RAG-QwQ-32B by 29.6% on exact match.

At the frontier, Search-o1 surpasses human expert performance on the GPQA extended set overall (57.9 vs. the human expert baseline), including in physics (68.7 vs. 57.9 for human specialists) and biology (69.5 vs. 68.9). These are not narrow benchmark wins; GPQA is specifically designed to require graduate-level domain expertise, making these results a meaningful signal about the upper range of LRM capability in formal scientific reasoning.

### The Uncertainty Problem

A revealing limitation surfaces in the LRM reasoning trace itself. During complex reasoning on GPQA diamond problems, QwQ-32B-Preview uses the uncertain word "perhaps" an average of over 30 times per reasoning process. This is not a stylistic quirk: it reflects a fundamental tension in the LRM paradigm. Extended deliberation gives the model more time to surface uncertainty and explore alternatives, but it also means the model is generating many hedged, partially-committed intermediate states rather than confidently traversing a search tree. The uncertainty accumulates visibly, and in knowledge-intensive scientific domains, some of it is genuine: the model lacks the factual grounding to resolve the ambiguity, regardless of how long it reasons.

This is the core motivation for agentic augmentation of LRMs. The Search-o1 framework addresses this by integrating retrieval mid-reasoning: the model can emit search queries during its chain-of-thought, trigger external web retrieval (via Bing Web Search API, top-10 documents, with Jina Reader for content fetching), and inject retrieved knowledge through a dedicated **Reason-in-Documents module**. Crucially, this module analyzes retrieved documents independently from the main reasoning chain, producing concise refined knowledge for injection rather than flooding the reasoning context with raw document text. The agentic retrieval mechanism can be triggered multiple times within a single reasoning session, allowing the model to iteratively resolve successive knowledge gaps as they emerge during deliberation.

### Architecture and Augmentation

The Search-o1 architecture illustrates the direction in which LRM research is moving: toward modular, tool-augmented reasoning agents rather than monolithic end-to-end models. The backbone LRM generates the extended reasoning trace and determines when retrieval is needed; the retrieval subsystem fetches external evidence; the Reason-in-Documents module bridges raw retrieved content and the reasoning chain. This separation of concerns matters because naively inserting document text into an extended reasoning chain risks disrupting its coherence or overwhelming its context. The module-based approach keeps the reasoning chain structurally intact while enriching it with grounded evidence.

The performance ceiling of the Search-o1 architecture is not uniform across domains. While it surpasses human domain specialists in physics and biology, it trails chemists in chemistry (40.7 vs. 72.6 for domain specialists), a gap large enough to suggest that chemistry reasoning may require more domain-specific structure than general agentic retrieval provides.

---

## Limitations and Open Questions

The uncertainty-accumulation finding raises a question that the field has not yet answered: does extended deliberation help or hurt on tasks where the model's parametric knowledge is genuinely insufficient? The Search-o1 results suggest retrieval can partially compensate, but the chemistry gap indicates that retrieval alone is not always sufficient. It remains unclear whether this is a failure of retrieval quality, of the reasoning model's ability to integrate retrieved chemistry knowledge, or of the task structure itself.

A second open question concerns the training stability of RL for reasoning. GRPO's group-relative normalization reduces variance compared to PPO, but the theoretical properties of RL training on open-ended reasoning chains (where reward signals are sparser and less structured than in games like Go) remain less well understood than in the game-playing lineage.

The human-expert comparison on GPQA also deserves scrutiny. Outperforming the average human expert in a domain is not the same as matching the domain frontier. GPQA expert performance is itself a heterogeneous sample, and the 68.7% in physics, while impressive, leaves substantial headroom before it would constitute true expert-level scientific reasoning in the sense of generating novel insight or detecting errors in cutting-edge research.

---

## Relationships

LRMs are the primary beneficiary of [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] research, with GRPO and related algorithms from [[themes/policy_optimization|Policy Optimization]] being the main training mechanisms. Their extended chain-of-thought is the instantiation of [[themes/chain_of_thought|Chain of Thought]] at scale, and their deployment in agentic settings connects them to [[themes/agent_systems|Agent Systems]], [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]], and [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]]. The Search-o1 framework in particular sits at the intersection of LRM reasoning and RAG, representing a hybrid paradigm distinct from both pure retrieval systems and pure parametric reasoners.

The intellectual lineage from AlphaGo and AlphaZero to contemporary LRMs is not merely historical: it establishes that [[themes/reinforcement_learning|Reinforcement Learning]] via self-play and reward feedback can produce qualitatively different reasoning behaviors than supervised learning alone, a principle that now generalizes from games to language.

Source references: Search-o1: Agentic Search-Enhanced Large Reasoning Models, A Survey of Reinforcement Learning for Large Reasoning Models, Unlocking the Power of Multi-Agent LLM for Reasoning

## Sources
