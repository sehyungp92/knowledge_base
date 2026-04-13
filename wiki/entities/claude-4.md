---
type: entity
title: Claude 4
entity_type: entity
theme_ids:
- adaptive_computation
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- ai_pricing_and_business_models
- chain_of_thought
- frontier_lab_competition
- knowledge_and_memory
- model_architecture
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
- scaling_laws
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-09'
updated: '2026-04-09'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 6.986149045614628e-05
staleness: 0.0
status: active
tags: []
---
# Claude 4

> Claude 4 is Anthropic's flagship model family, characterized by a "softer touch" on search and compute relative to more aggressive reasoning competitors: consistently faster to return answers while maintaining strong performance on agentic and function-calling benchmarks. It represents one pole of the emerging reasoning model spectrum, in which labs are now forced to make explicit architectural bets about the tradeoff between depth of inference-time computation and response latency.

**Type:** entity
**Themes:** [[themes/adaptive_computation|Adaptive Computation]], [[themes/agent_systems|Agent Systems]], [[themes/ai_business_and_economics|AI Business and Economics]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/ai_pricing_and_business_models|AI Pricing and Business Models]], [[themes/chain_of_thought|Chain of Thought]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/knowledge_and_memory|Knowledge and Memory]], [[themes/model_architecture|Model Architecture]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/scaling_laws|Scaling Laws]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]

## Overview

Claude 4 arrives in a landscape that has fundamentally reoriented around inference-time scaling. The key insight from Thinking, Searching, and Acting is that chains of thought were the technological step-change that made search and multi-step execution qualitatively functional, not just incrementally better. Claude 4 is built on these three now-standard primitives (thinking, searching, acting), but its design philosophy positions it toward speed and consistency rather than maximal depth-first search over reasoning paths.

The family includes at least two tiers: Sonnet and Opus. Opus achieves a SWE-Terminal-Bench score of 37.5%, leading a field that includes o3 (30.2%), GPT-4.1 (30.3%), Gemini 2.5 Pro (25.3%), and Claude 4 Sonnet itself (35.5%), indicating meaningful within-family differentiation. On agentic benchmarks, Claude 4 Sonnet ties with the Opus tier on TAU-bench Retail (79.7) and Airline (60.4), while leading all compared models on BFCL v3 full (77.8) for function calling. The BFCL result is particularly notable: it suggests that Anthropic has invested heavily in tool-use reliability, which aligns with Claude 4's positioning in agentic deployment contexts.

Contextually, Claude 4 is entering a competitive environment where the rules of scaling are being rewritten. Thinking, Searching, and Acting documents that both OpenAI's acknowledgment that GPT-4.5 was not a frontier model and Gemini's decision not to release an Ultra-class model reflect the same underlying dynamic: diminishing returns from pure parameter scaling. This is the environment Claude 4 was designed for, one where inference-time compute, search integration, and agentic coordination matter more than raw pretraining scale.

GPT-5, described in GPT-5 and the arc of progress, deploys a fundamentally different architectural philosophy: a unified system with a real-time router continuously trained on user behavior, model-switching signals, and preference rates, selecting between a fast model and a deep reasoning model per query. Claude 4 represents a contrasting bet: a single family with tiered capability, letting users and developers select the appropriate tier rather than automating that selection at the routing layer. Whether automated routing or explicit tiering wins as the dominant UX is an open competitive question.

## Key Findings

The broader reasoning model context matters for understanding where Claude 4 fits. Early criticism that reasoning models "won't generalize" has been empirically falsified; the inference-time scaling paradigm has proven durable across domains. Claude 4 benefits from this validated foundation, but also inherits the challenge that all closed reasoning model developers face: the inability to generalize across many deployment environments the way open models must. Thinking, Searching, and Acting draws a sharp distinction here: closed models like Claude 4 control the full stack from training search integration to serving, while open models must generalize across heterogeneous retrieval systems and deployment tooling. This is a structural advantage for Anthropic, particularly in agentic settings where tool-use reliability depends on tight integration between reasoning and action.

Search integration transforms the nature of hallucination for reasoning models. Whereas pre-search LLMs produced blatantly incorrect content, search-augmented models like Claude 4 now fail differently: hallucinations manifest as missing context rather than fabricated facts. This is a qualitative improvement in failure mode, but it also shifts where trust calibration must happen, from "is this true?" toward "is this complete?"

The multi-step agentic setting is where Claude 4 is most directly benchmarked. Some ideas for what comes next frames the core complexity of LLM-based agents: they involve many model calls, sometimes with multiple models and multiple prompt configurations, meaning reliability compounds across steps. Claude 4's strong BFCL v3 score (77.8) and competitive TAU-bench results suggest it handles this compound reliability challenge well relative to peers.

Open-source competition is also directly relevant context. An open-source MoE model has achieved 65.8 on SWE-bench Verified and ranked above Claude 4 on LMSYS Arena (ranked #1 open-source, #5 overall), demonstrating that the performance gap between open and closed frontier models is narrowing in agentic software engineering. This puts pressure on Claude 4's value proposition, particularly in cost-sensitive deployment contexts.

## Capabilities

- **Function calling reliability**: Leading BFCL v3 full score of 77.8, outperforming all compared models on tool-use benchmarks (maturity: narrow_production)
- **Terminal-based agentic software engineering**: SWE-Terminal-Bench score of 37.5% (Opus) and 35.5% (Sonnet), outperforming o3, GPT-4.1, and Gemini 2.5 Pro (maturity: narrow_production)
- **Retail and airline agentic task completion**: TAU-bench Retail 79.7 and Airline 60.4, competitive with top closed models (maturity: narrow_production)
- **Multi-turn tool-calling**: Competitive across Tau2-bench and ACEBench, outperforming GPT-4.1 and Gemini 2.5 Flash on multi-turn dialogue with tool use (maturity: narrow_production)

## Known Limitations

The most structurally significant limitation is cost. Claude 4 Opus was excluded from SWE-bench Multilingual evaluation due to inference cost, creating systematic gaps in comparative benchmarking. This is more than a logistical inconvenience: it means that the Opus tier's true cross-lingual capability profile is unknown, and the exclusion may be creating a false impression that open-source models have closed the gap more than they actually have (or vice versa). As frontier model inference costs rise with deeper reasoning traces, this problem is likely to worsen, making reproducible evaluation increasingly uneven across labs and researchers with different resource access.

The "softer touch" design philosophy also implies a capability ceiling in tasks that specifically reward extended deliberation. Models like o3 that invest more compute per query may outperform Claude 4 on problems where the correct answer genuinely requires exhaustive search over a large reasoning tree, even if Claude 4 is faster and more cost-efficient on the median task. The tradeoff is rational from a deployment economics standpoint, but it leaves a performance gap at the extreme end of reasoning depth that may matter for hard science and mathematics problems.

## Relationships

Claude 4 is Anthropic's direct competitive response to GPT-5's adaptive routing architecture. The two represent distinct bets on how inference-time compute should be allocated and who should control that allocation. Claude 4 is positioned within the three-primitive framework (thinking, searching, acting) described in Thinking, Searching, and Acting, sitting at the faster/lighter end of the reasoning compute spectrum relative to o3. Open-source MoE models surpassing Claude 4 on LMSYS Arena represent a growing competitive pressure from below. The function-calling and agentic infrastructure ecosystem described in Some ideas for what comes next is the deployment environment Claude 4 is most optimized for.

## Limitations and Open Questions

## Sources
