---
type: entity
title: CodeAct
entity_type: method
theme_ids:
- agent_evaluation
- agent_self_evolution
- agent_systems
- ai_market_dynamics
- code_and_software_ai
- code_generation
- computer_use_and_gui_agents
- evaluation_and_benchmarks
- finetuning_and_distillation
- in_context_and_meta_learning
- long_context_and_attention
- model_architecture
- model_commoditization_and_open_source
- multi_agent_coordination
- post_training_methods
- reasoning_and_planning
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 5
sources_since_update: 0
update_count: 1
influence_score: 0.002899948259755925
staleness: 0.0
status: active
tags: []
---
# CodeAct

**Type:** method
**Themes:** [[themes/agent_evaluation|agent_evaluation]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

A code-execution agent that operates inside a ReAct loop. Unlike RLMs, CodeAct provides the user prompt directly to the LM context window rather than offloading it to a REPL variable, inheriting the LM's context window limitations.

## Key Findings

1. An RLM initializes a REPL programming environment in which the prompt P is set as the value of a variable, permitting the LLM to write code that peeks into and decomposes P. (from "Recursive Language Models")
2. There is a large performance gap between open-source and closed-source LLMs on CodeAct tasks: the best open-source model achieves 13.4% success rate while the best closed-source model (GPT-4-1106-prev (from "Executable Code Actions Elicit Better LLM Agents")
3. RLMs treat arbitrarily long user prompts as part of the external environment rather than feeding them directly into the neural network. (from "Recursive Language Models")
4. CodeAct achieves higher task success rates than alternative action formats in 12 out of 17 evaluated LLMs on M3ToolEval. (from "Executable Code Actions Elicit Better LLM Agents")
5. TextGrad improves GPT-4o's zero-shot code accuracy on LEETCODE-HARD from 26% to 36%, raises MMLU-Physics performance from 91.2% to 95.1%, and enhances the multi-tool agent CHAMELEON by 7.7% (from "Adaptation of Agentic AI")
6. The T2 approach (s3) achieves 58.9% average accuracy with only 2,400 training samples by training a lightweight 7B searcher subagent using frozen-generator feedback. (from "Adaptation of Agentic AI")
7. CodeAct achieves up to 20% higher success rate compared to JSON and text action alternatives across 17 evaluated LLMs. (from "Executable Code Actions Elicit Better LLM Agents")
8. On BrowseComp-Plus (1K), RLM(GPT-5) achieves 91.3% accuracy while the base GPT-5 model scores 0.0% due to context window limitations. (from "Recursive Language Models")
9. The T2 paradigm represents a conceptual inversion: rather than adapting the agent to use tools better, it adapts tools to better serve a fixed frozen agent, reframing the foundation model from optimiz (from "Adaptation of Agentic AI")
10. DeepSeek-R1 demonstrated that reinforcement learning with verifiable reward can effectively enhance the reasoning capabilities of large agents (from "Adaptation of Agentic AI")
11. DeepRetrieval achieves approximately 3x recall improvement (65.1% vs. 24.7%) using causal RL to optimize tool mechanics. (from "Adaptation of Agentic AI")
12. On OOLONG, RLM with GPT-5 and Qwen3-Coder outperform their base models by 28.4% and 33.3% respectively, even on tasks within the model's context window. (from "Recursive Language Models")
13. Recursive Language Models can successfully process inputs up to two orders of magnitude beyond model context windows. (from "Recursive Language Models")
14. In the T1 paradigm, tools are trained independently of the frozen agent as plug-and-play modules, covering retrievers, domain-specific models, and other pretrained components. (from "Adaptation of Agentic AI")
15. In the A2 paradigm, the agent is optimized using evaluations of its own outputs—final answers, plans, or reasoning traces—possibly after incorporating tool results. (from "Adaptation of Agentic AI")

## Relationships

## Limitations and Open Questions

## Sources
