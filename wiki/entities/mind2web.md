---
type: entity
title: Mind2Web
entity_type: dataset
theme_ids:
- agent_evaluation
- agent_memory_systems
- agent_self_evolution
- agent_systems
- computer_use_and_gui_agents
- evaluation_and_benchmarks
- knowledge_and_memory
- multimodal_models
- reasoning_and_planning
- test_time_compute_scaling
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00017122173752196876
staleness: 0.0
status: active
tags: []
---
# Mind2Web

> Mind2Web is a benchmark dataset designed to evaluate the generalization of web agents across diverse, real-world web tasks. Unlike narrow, single-domain evaluations, it stresses agents with three increasingly difficult splits — cross-task, cross-website, and cross-domain — making it one of the most rigorous early measures of whether a web agent can operate outside its training distribution. Its multi-dimensional metrics (element accuracy, action F1, step success rate, task success rate) expose failure modes at both the action and task level, establishing it as a foundational reference point in the study of GUI and web-based agents.

**Type:** dataset
**Themes:** [[themes/agent_evaluation|agent_evaluation]], [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/multimodal_models|multimodal_models]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/vision_language_models|vision_language_models]]

## Overview

Mind2Web evaluates generalist web agents on versatile, open-ended web operations across three held-out splits: cross-task (new tasks on seen websites), cross-website (seen task types on unseen websites), and cross-domain (entirely unseen website categories). This hierarchy of generalization pressures is its defining structural contribution — it distinguishes between agents that have memorized site-specific patterns and those that have learned transferable web navigation skills.

Its metric suite is deliberately layered. Element accuracy (EA) and action F1 probe low-level grounding — can the agent correctly identify and interact with the right UI element? Step success rate (SSR) and task success rate (SR) measure whether those atomic actions compose into coherent, goal-achieving trajectories. The gap between EA/SSR and SR is a diagnostic signal: high element accuracy with low task success reveals planning or recovery failures rather than perception failures.

## What Evidence from Related Systems Reveals

The claims associated with Mind2Web in this library arrive primarily through WebVoyager, and they collectively illuminate the challenges Mind2Web was designed to surface.

**Perception is a bottleneck, not a solved problem.** WebVoyager finds that most open-source LMMs are effectively disqualified from web navigation because they downsample images to 224×224 or 336×336 pixels — resolutions at which standard web fonts become unrecognizable. This is precisely the kind of fine-grained visual grounding that Mind2Web's element accuracy metric probes, and it explains why visual grounding issues account for 24.8% of WebVoyager failures even in a high-resolution setting. The benchmark's EA metric thus functions as a proxy for whether a model can actually see the web page, not just reason about it abstractly.

**Navigation failure dominates over reasoning failure.** The most common failure mode in WebVoyager (44.4% of failures) is the agent exhausting its step budget without completing the task — what the authors call "navigation stuck." This points to a limitation that metrics like SR expose but don't diagnose: agents can know what to do at each step yet still fail to reach the goal because they lack effective recovery strategies or horizon-aware planning. Mind2Web's SSR/SR gap makes this structurally visible.

**Hallucination is a persistent secondary failure.** At 21.8% of failures, hallucination — agents acting on perceived page content that isn't there — is the second-largest failure category. This matters for interpreting Mind2Web results: high EA on a benchmark may reflect agents that are overly conservative or rely on text rather than visual grounding, masking hallucination tendencies that only emerge in real web environments.

**Multimodal backbones outperform text-only baselines, but not by transformative margins.** WebVoyager's comparison shows all three LMM backbones (GPT-4V, Claude-3-Opus, GPT-4o) significantly outperform text-only settings, and WebVoyager itself achieves 59.1% task success versus 40.1% for text-only WebVoyager and 30.8% for GPT-4 (All Tools). The gap is real, but the absolute numbers remain modest — over 40% of tasks fail even for the best configuration, reinforcing that Mind2Web-style benchmarks are not yet saturated.

**Memory and workflow structure matter as much as raw model capability.** Sources like Agent Workflow Memory and ReasoningBank cite Mind2Web as a proving ground for agents that learn reusable procedural patterns across tasks. The implication is that Mind2Web's cross-task split is particularly sensitive to whether an agent can retrieve and adapt prior action sequences — a capability that raw LMM benchmarks don't test. Agents with structured workflow memory show meaningful gains, suggesting the benchmark rewards system-level design, not just model scale.

## Evaluation Reliability

WebVoyager's automatic evaluation using GPT-4V achieves 85.3% agreement with human judgment (κ = 0.70), matching inter-human annotator agreement. GPT-4o is marginally more reliable (κ = 0.72), while Claude-3-Opus is less so (κ = 0.60). This matters for interpreting Mind2Web results at scale: automated evaluation is viable, but evaluator choice introduces measurable variance in reported numbers, and comparisons across papers using different evaluators should be treated cautiously.

## Open Questions

Mind2Web operates on static snapshots or controlled environments; it does not expose agents to live websites with floating ads, dynamic content, or constant structural updates the way WebVoyager does. This raises the question of whether strong Mind2Web performance predicts real-world robustness, or whether the benchmark's controlled conditions systematically underestimate deployment difficulty.

The three-split generalization hierarchy also assumes that cross-domain is strictly harder than cross-website, which is harder than cross-task. In practice, some domains may be more homogeneous than some individual websites, and the ordering may not hold uniformly. A more granular difficulty taxonomy — perhaps based on visual complexity, action depth, or required world knowledge — would sharpen what the benchmark actually measures.

Finally, as agents with explicit memory systems (workflow memory, reasoning traces) accumulate advantages on cross-task splits, Mind2Web risks becoming a benchmark of memory architecture rather than web navigation capability. Future evaluation designs may need to control for task overlap in agent memory to isolate generalization from retrieval.

## Key Findings

## Limitations and Open Questions

## Relationships

## Sources
