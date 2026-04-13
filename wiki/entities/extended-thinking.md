---
type: entity
title: extended thinking
entity_type: method
theme_ids:
- agent_systems
- ai_software_engineering
- chain_of_thought
- code_and_software_ai
- code_generation
- interpretability
- mechanistic_interpretability
- reasoning_and_planning
- software_engineering_agents
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.000547216781662528
staleness: 0.0
status: active
tags: []
---
# Extended Thinking

Extended thinking is a Claude capability that enables deep pre-response reasoning — a distinct internal deliberation phase that occurs before Claude begins generating its visible output. Unlike the `think` tool, which allows mid-response pauses during tool-use workflows, extended thinking operates as a front-loaded reasoning budget, making it best suited for tasks like coding, mathematics, physics, and non-agentic problem-solving where the full problem scope is known upfront. Its introduction with Claude 3.7 Sonnet marked a significant step in test-time compute scaling as a practical, deployed capability.

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_software_engineering|ai_software_engineering]], [[themes/chain_of_thought|chain_of_thought]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/interpretability|interpretability]], [[themes/mechanistic_interpretability|mechanistic_interpretability]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

Extended thinking grants developers fine-grained control over how long a model deliberates before responding. Through a configurable "thinking budget," operators can dial the compute devoted to a problem, trading latency and cost for reasoning depth. Crucially, this does not involve a separate model or strategy — the same underlying model simply allocates more effort before producing output, a distinction that matters for understanding what the capability actually is versus marketing framing.

The visible thought trace surfaced through extended thinking is explicitly a research preview. It was not subjected to Claude's standard character training, which means users encounter thinking that reads as more detached and less personal than Claude's default outputs — a deliberate architectural choice that reveals reasoning in a rawer form but raises questions about how much the visible trace reflects actual internal computation versus a post-hoc reconstruction.

## Scaling Dimensions

Extended thinking sits at the intersection of two scaling axes: **sequential** and **parallel**. The sequential axis — allocating a larger thinking budget to a single problem — is what shipped in Claude 3.7 Sonnet. The parallel axis — sampling multiple independent thought processes and selecting the best without knowing the answer ahead of time — remains a research direction and is not available in the deployed model. The combination of these approaches produces striking benchmark results: using 256 independent samples, a learned scoring model, and a maximum 64k-token thinking budget, Claude 3.7 Sonnet achieved **84.8% on GPQA**, a demanding expert-level science benchmark. This result demonstrates the ceiling of what parallel test-time compute can extract from the model, even though production deployments do not yet offer this regime.

## Agentic Synergies

Extended thinking intersects with agentic capability through what the Claude's extended thinking documentation calls "action scaling" — the ability to iteratively call functions, respond to environmental changes, and sustain progress on open-ended tasks across many turns. Claude 3.7 Sonnet can allocate more turns, time, and compute to computer use tasks than its predecessor, and this was demonstrated concretely through a Pokémon Red experiment: equipped with basic memory, screen pixel input, and function calls, the model sustained tens of thousands of interactions beyond its native context window, successfully defeating three Gym Leaders — a test of long-horizon coherence as much as raw capability.

## Safety Implications

The deployment of extended thinking raised immediate safety-relevant questions, particularly around agentic and computer use contexts. Prompt injection — where malicious content in the environment hijacks the model's reasoning — was a focus: defenses combining new training, system prompt instructions, and a classifier achieved **88% attack prevention** (up from 74%) at a **0.5% false-positive rate**. This remains an arms-race problem, not a solved one.

On CBRN-related risk, controlled studies found that model-assisted participants showed measurable uplift over unassisted ones — a meaningful finding. However, expert red-teamers observed that the frequency of critical failures across all attempts was high enough to prevent successful end-to-end task completion. The interpretation matters: this finding provides neither reassurance (uplift was real) nor alarm (no attempt fully succeeded), and its trajectory as models improve is an open question.

## Limitations and Open Questions

The most significant limitation is what extended thinking currently *cannot* do well: **tool-use scenarios**. The capability is explicitly positioned as distinct from the `think` tool precisely because the front-loaded reasoning model does not adapt well to interleaved tool calls where new information arrives mid-task. This creates an architectural tension in agentic workflows — the deepest reasoning happens before action, but real tasks require reasoning that responds to action outcomes.

The visible thought process also carries an interpretability caveat: because it lacks character training, it should not be read as a window into how Claude "really" thinks across all contexts. It is a research artifact, not a ground truth. This matters for the broader [[themes/mechanistic_interpretability|mechanistic interpretability]] agenda — chain-of-thought traces that differ in register from the model's trained persona complicate what conclusions can be drawn from them.

Parallel test-time compute scaling — arguably the more powerful axis — remains unavailable in production. The 84.8% GPQA result exists in a compute regime that no deployed system currently offers users, meaning the headline capability and the shipped capability are meaningfully different.

Finally, competitors like Kimi K2 represent a deliberate counter-positioning: explicitly a "reflex-grade model without long thinking," optimized for latency over reasoning depth. This signals a coming architectural divergence between thinking and non-thinking models, and the right tradeoff remains an open empirical and product question.

## Source Connections

Primary coverage in Claude's extended thinking; complementary context in The "think" tool: Enabling Claude to stop and think and Claude Code: Anthropic's CLI Agent.

## Key Findings

## Relationships

## Sources
