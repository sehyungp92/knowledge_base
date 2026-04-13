---
type: entity
title: τ-Bench
entity_type: dataset
theme_ids:
- agent_evaluation
- agent_systems
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- finetuning_and_distillation
- multi_agent_coordination
- post_training_methods
- reasoning_and_planning
- synthetic_data_generation
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0011118530553775926
staleness: 0.0
status: active
tags: []
---
# τ-Bench

τ-Bench (tau-bench) is a benchmark for evaluating large language models on realistic, multi-turn tool use in customer service settings. Unlike static function-calling benchmarks, it embeds models in simulated user conversations where they must adhere to domain-specific policies, navigate ambiguous requests, and make precise database modifications — reflecting the messy, sequential nature of real agentic work. Its two domains, airline and retail, have become a standard proving ground for agentic reasoning techniques, particularly those involving structured scratchpad methods.

**Type:** dataset
**Themes:** [[themes/agent_evaluation|agent_evaluation]], [[themes/agent_systems|agent_systems]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

τ-Bench is structured around two domains — **airline** and **retail** — each requiring the model to maintain coherent multi-turn dialogue with a simulated user while invoking the correct tools, respecting business rules, and correctly modifying a backing database. Tasks are evaluated using pass^k metrics, where pass^1 measures single-run success and pass^k (for k > 1) measures consistency across repeated trials — a demanding criterion that penalises models that occasionally succeed but cannot reliably do so.

This pass^k framing is a deliberate design choice: it surfaces the difference between models that get lucky on isolated trajectories and those that have genuinely internalised the reasoning required. The airline domain is significantly harder than retail, and the gap between pass^1 and pass^5 scores across all tested methods exposes how fragile most agentic behaviours remain under repeated evaluation.

## Key Findings

### The 'Think' Tool as a Reasoning Scaffold

The clearest experimental signal on τ-Bench comes from The "think" tool: Enabling Claude to stop and think, which used τ-Bench as a primary testbed. The core finding is striking: simply giving Claude a no-op `think` tool — one that appends reasoning to an internal log without retrieving information or modifying any external state — produced a **54% relative improvement** on the airline domain pass^1 metric (0.570 vs. 0.370 baseline). The effect compounds at higher k: pass^5 in the airline domain rose from 0.100 (both baseline and unprompted think tool) to 0.340 when the think tool was paired with an optimised prompt. This is not a marginal gain — it represents a qualitative shift in consistency.

The retail domain shows a more modest but still positive effect: the think tool alone (without additional prompting) lifted pass^1 from 0.783 to 0.812. The airline/retail asymmetry is informative — it suggests the think tool's value scales with task complexity and the degree to which policy adherence requires deliberate multi-step reasoning.

Importantly, the think tool is distinct from extended thinking. Extended thinking concerns what a model does before generating any output; the think tool is an explicit, callable action within a trajectory that creates a structured reasoning moment during the task. This distinction matters for τ-Bench specifically, where the benefit arises from mid-trajectory reflection rather than pre-generation chain-of-thought.

### Placement in the Broader Evaluation Landscape

τ-Bench occupies a specific niche relative to adjacent benchmarks. ACEBench takes a complementary approach: 4,538 APIs across 8 major domains in Chinese and English, evaluated via AST parsing against ground truth — a higher-breadth, lower-depth design that enables LLM-free evaluation. τ-Bench trades breadth for realism, prioritising the longitudinal coherence of a conversation over the coverage of API types.

ARE and Gaia2 push further along the realism axis by introducing asynchronous, time-driven environments where state changes independently of the agent — a setting τ-Bench does not attempt. In ARE, environment time passes regardless of agent action, and random or scheduled events continuously update state. τ-Bench's simulated user is comparatively static, which makes it tractable as a controlled testbed but limits its fidelity to real-world deployment conditions.

## Open Questions and Limitations

Several limitations of τ-Bench are implied by how it is used and discussed:

- **Consistency ceiling.** Even the best-performing configuration (think tool + optimised prompt) achieves only pass^5 of 0.340 in the airline domain. The majority of runs still fail, and pass^k curves decay steeply. This raises the question of whether τ-Bench is measuring a genuine reasoning capability or a sensitivity to prompt formulation.

- **Static user simulation.** Unlike ARE environments, τ-Bench's simulated users do not evolve asynchronously. Real customer service involves dynamic, sometimes contradictory user behaviour that the benchmark abstracts away.

- **Domain narrowness.** Two domains is a thin basis for generalising about tool-use capability. The airline/retail gap already shows domain sensitivity; it is unclear how findings transfer outside these task types.

- **Optimised prompt dependence.** The difference between the unprompted think tool (pass^5 = 0.100) and the prompted version (pass^5 = 0.340) in the airline domain is larger than the difference between the baseline and the unprompted think tool. This suggests the benchmark is sensitive to prompting choices in ways that may not reflect underlying model capability.

## Relationships

τ-Bench is most directly compared to ACEBench (breadth-first tool-use evaluation) and ARE/Gaia2 (dynamic, asynchronous environments). It shares the tool-use and policy-adherence framing with ACEBench but differs fundamentally in evaluation philosophy — conversation coherence over API coverage. Its relationship to SWE-bench is indirect: both serve as testbeds for the think tool, but SWE-bench evaluates code generation rather than customer service, and the think tool's 1.6% improvement there is substantially smaller than its effect on τ-Bench's airline domain, reinforcing that the benefit scales with task structure and policy complexity.

## Limitations and Open Questions

## Sources
