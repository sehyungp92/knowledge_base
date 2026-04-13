---
type: entity
title: Task Success Rate
entity_type: metric
theme_ids:
- agent_evaluation
- agent_memory_systems
- agent_self_evolution
- agent_systems
- chain_of_thought
- computer_use_and_gui_agents
- evaluation_and_benchmarks
- knowledge_and_memory
- multimodal_models
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- test_time_compute_scaling
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.00031262601854497213
staleness: 0.0
status: active
tags: []
---
# Task Success Rate

Task success rate is the dominant evaluation metric for agentic AI systems, measuring the proportion of tasks an agent completes successfully end-to-end. Its prevalence across benchmarks like WebVoyager, ALFWorld, and Points24 reflects a field-wide consensus that ultimate task completion — not intermediate process quality — is the ground truth signal for agent capability. As agents move from controlled environments to open-ended real-world deployments, the metric has become both more informative and more contested: what counts as "success" on a live website with dynamic content, floating ads, and shifting layouts is considerably harder to adjudicate than on a static simulation.

**Type:** metric
**Themes:** [[themes/agent_evaluation|agent_evaluation]], [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/chain_of_thought|chain_of_thought]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/multimodal_models|multimodal_models]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/vision_language_models|vision_language_models]]

## Overview

Task success rate quantifies what fraction of assigned tasks an agent fully resolves — from initial instruction to terminal state — without human intervention. It originated as a straightforward pass/fail signal in embodied and game environments, but has migrated into web navigation, GUI interaction, and multi-step reasoning benchmarks as the canonical measure of agentic competence. Its appeal is its directness: unlike token-level or step-level metrics, it captures whether the agent actually did the thing it was asked to do. Its weakness is its binary collapse of complex trajectories and its dependence on how "success" is defined and verified — a definition that becomes significantly harder to operationalize outside of simulated environments.

## Key Findings

The most detailed empirical picture of task success rate as a metric comes from WebVoyager, which achieves a 59.1% task success rate on its own benchmark — substantially above GPT-4 (All Tools) at 30.8% and text-only WebVoyager at 40.1%. This gap between multimodal and text-only agents is consistent: all three LMM backbones tested (GPT-4V, Claude-3-Opus, GPT-4o) significantly outperform the text-only baseline, establishing that visual perception is load-bearing for real-web task completion, not merely additive. Transferring to the SeeAct online test set, WebVoyager reaches 30% success versus the best SeeAct autonomous agent's 26% — a modest but consistent advantage that suggests the architectural choices generalise.

What the raw success rate obscures, however, is the structure of failure. On WebVoyager, failures decompose as: navigation stuck (step budget exhausted) at 44.4%, visual grounding issues at 24.8%, and hallucination at 21.8%. These failure modes are not interchangeable — they respond to different interventions. Step budget failures suggest planning or efficiency problems; visual grounding failures point to perceptual limitations in current LMMs, compounded by the fact that most open-source models downsample to 224×224 or 336×336 pixels, rendering fine-grained web text unrecognizable. Hallucination failures reflect a different pathology: the agent confabulates page content rather than grounding its actions in what is actually visible. Together, these three modes account for over 90% of failures, meaning that improving task success rate substantially requires simultaneous progress on at least two distinct capability axes.

The evaluation of task success rate is itself a methodological challenge. Human annotation is the gold standard but expensive and inconsistent — inter-annotator agreement on WebVoyager reaches kappa=0.70. GPT-4V as an automatic evaluator matches this when given the full agent trajectory (kappa=0.70, 85.3% agreement with human judgment), and GPT-4o marginally exceeds it (kappa=0.72). Claude-3-Opus lags at kappa=0.6, making it a less reliable automatic judge. This hierarchy matters: the choice of evaluator can shift reported success rates, and the field has not converged on a standard. The 85.3% human agreement for GPT-4V-based evaluation is encouraging but means roughly one in seven task outcomes is disputed — a non-trivial source of noise when comparing systems at the margin.

Design choices around context management interact with task success rate in underappreciated ways. WebVoyager's context clipping strategy — retaining only the three most recent observations while keeping the full history of thoughts and actions — reflects an empirical finding that accumulating web page observations degrades rather than improves performance. This is a specific instance of a broader pattern seen in Agent Workflow Memory and other memory-augmented agent work: more context is not always better, and the structure of what is retained shapes trajectory quality as much as raw model capability.

## Limitations and Open Questions

The benchmark-level task success rates reported across the literature are difficult to compare directly. Benchmarks differ in task difficulty distribution, step budget, action space, website dynamism, and evaluation protocol — all of which influence the headline number independently of agent capability. The 643-task WebVoyager benchmark reports 99.68% pairwise task similarity below 0.6, which is a reasonable diversity signal, but diversity within a benchmark does not guarantee coverage of the failure modes that matter most in deployment.

The metric is also silent on trajectory quality. An agent that completes a task via an unnecessarily long or fragile sequence of actions scores identically to one that completes it efficiently and robustly. As agent systems are increasingly evaluated on cost, latency, and reliability — not just completion — task success rate alone is insufficient. The field is beginning to supplement it with step efficiency, interaction count, and failure mode breakdowns, but no composite metric has achieved consensus.

Finally, the open-web setting exposes a fundamental measurement problem: websites change. A task that was completable at evaluation time may become impossible due to interface updates, paywalls, or content removal. This temporal instability means that benchmark scores have a shelf life, and longitudinal comparisons are unreliable without re-evaluation on frozen snapshots — a practice that is rarely followed.

## Related Entities

- [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]] — the broader methodological context within which task success rate operates
- [[themes/computer_use_and_gui_agents|Computer Use and GUI Agents]] — the primary deployment context generating the richest task success rate data
- [[themes/agent_evaluation|Agent Evaluation]] — the subfield developing richer metrics to complement or replace simple pass/fail scoring
- [[themes/reasoning_and_planning|Reasoning and Planning]] — step budget exhaustion as the dominant failure mode implicates planning quality directly

## Relationships

## Sources
