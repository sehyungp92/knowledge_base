---
type: entity
title: METR
entity_type: entity
theme_ids:
- agent_evaluation
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- benchmark_design
- evaluation_and_benchmarks
- frontier_lab_competition
- multi_agent_coordination
- pretraining_and_scaling
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- scaling_laws
- startup_and_investment
- startup_formation_and_gtm
- tool_use_and_agent_protocols
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.000869409116259248
staleness: 0.0
status: active
tags: []
---
# METR

**Type:** entity
**Themes:** [[themes/agent_evaluation|agent_evaluation]], [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/benchmark_design|benchmark_design]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/scaling_laws|scaling_laws]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Overview

An organization whose sole purpose is to study AI capabilities, known for the study 'Measuring AI Ability to Complete Long Tasks' which tracks the length of software engineering tasks AI can autonomously complete.

## Key Findings

1. o3 was trained with tools through reinforcement learning, teaching it not just how to use tools but to reason about when to use them. (from "OpenAI's o3: Over-optimization is back and weirder than ever")
2. A 100-step workflow at 99% per-step reliability completes successfully only ~37% of the time, meaning it fails more often than it succeeds (from "What it takes to build AI agents that actually work - Foundation Capital")
3. Bob McGrew, former Chief Research Officer at OpenAI, stated that intelligence is no longer the primary constraint and the new frontier is reliable interaction with the external world. (from "OpenAI's o3: Over-optimization is back and weirder than ever")
4. At 90% per-step accuracy, a 10-step task succeeds only 35% of the time; at 99%, those same 10 steps succeed 90% of the time (from "What it takes to build AI agents that actually work - Foundation Capital")
5. At 99.9% per-step reliability, 100 steps succeed ~90% of the time, making long-horizon automation viable (from "What it takes to build AI agents that actually work - Foundation Capital")
6. Over-optimization occurs when the optimizer is stronger than the environment or reward function it uses to learn, causing it to find bugs or lapses in the training context and produce unusual or negat (from "OpenAI's o3: Over-optimization is back and weirder than ever")
7. METR found that o3 is the model that can operate independently for the longest duration in agentic tasks, but also has a propensity to hack their scores. (from "OpenAI's o3: Over-optimization is back and weirder than ever")
8. GDPval evaluation tasks were sourced from industry professionals with an average of 14 years of experience, with 30 tasks per occupation totalling 1320 tasks. (from "Failing to Understand the Exponential, Again")
9. ReTool, combining real-time code execution with outcome-driven RL, enables a 32B model to reach 72.5% accuracy on AIME, surpassing text-only baselines. (from "OpenAI's o3: Over-optimization is back and weirder than ever")
10. Over-optimization in RLHF caused models to repeat random tokens and gibberish because the training signal was mismatched from the true objective. (from "OpenAI's o3: Over-optimization is back and weirder than ever")
11. LOOP, a memory-efficient PPO variant, trains a 32B-parameter LLM as an interactive digital agent in AppWorld, outperforming the larger OpenAI o1 baseline by 9 percentage points. (from "OpenAI's o3: Over-optimization is back and weirder than ever")
12. Over-optimization in classical RL prevented agents from generalizing to new tasks and applied pressure on reward design. (from "OpenAI's o3: Over-optimization is back and weirder than ever")
13. GDPval uses blinded comparison of human and model-generated solutions for grading, allowing both clear preferences and ties. (from "Failing to Understand the Exponential, Again")
14. o3 has been designed for multi-step tool use to be used on any query where it's relevant, including searching autonomously without user-triggered toggles. (from "OpenAI's o3: Over-optimization is back and weirder than ever")
15. GRPO fine-tuning of Qwen2.5-7B-Instruct on just 100 examples raises BFCL multi-step tool-use accuracy from 55% to 78%. (from "OpenAI's o3: Over-optimization is back and weirder than ever")

## Capabilities

- Coding agents can reason across codebases, tickets, telemetry, and architectural graphs — learning from patterns of failure and resolution to continuously improve incident response (maturity: narrow_production)
- Production feedback loops enabling continuous model improvement from labeled failures without service interruption — nightly fine-tune jobs from human-override telemetry improving recall metrics measu (maturity: narrow_production)
- In-context learning naturally emerges in large Transformer models as a non-parametric solution to a regression objective on tokens, enabling zero- and few-shot adaptation without parameter updates (maturity: broad_production)
- Deep parsing of heterogeneous document content (charts, chemical formulas, geometric figures, natural images) via a single unified model with prompt-controlled output (maturity: demo)
- Horizon length for software and coding AI agents has been doubling every 7 months, as measured by METR research group (maturity: narrow_production)

## Known Limitations

- No reliability, accuracy, or failure rate metrics are provided for any of the named AI service companies — conspicuous absence of quality evidence for production deployments (severity: significant, trajectory: unclear)
- GLM-4.5 underperforms Claude-4-Sonnet on holistic agentic coding despite leading on tool calling success rate — winning metric does not translate to overall agent quality (severity: minor, trajectory: improving)
- Explicit-representation world models (geometric scaffolds) are computationally heavier and constrained in environment richness and variety — trading long-horizon consistency for throughput and scene d (severity: minor, trajectory: improving)
- Dynamic scene handling demonstrated only qualitatively — TUM-dynamics is used for camera pose evaluation but no dedicated dynamic object reconstruction metrics are reported, leaving dynamic scene qual (severity: minor, trajectory: unclear)
- Geometry parsing is far from solved — described as 'extremely challenging with a long way to go' due to complex interdependencies between line segments (severity: significant, trajectory: unclear)

## Relationships

## Limitations and Open Questions

## Sources
