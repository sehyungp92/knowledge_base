---
type: source
title: Simulating Environments with Reasoning Models for Agent Training
source_id: 01KJTBNSX33FH26FS2TKMTZKF3
source_type: paper
authors:
- Yuetai Li
- Huseyin A Inan
- Xiang Yue
- Wei-Ning Chen
- Lukas Wutschitz
- Janardhan Kulkarni
- Radha Poovendran
- Robert Sim
- Saravan Rajmohan
published_at: '2025-11-03 00:00:00'
theme_ids:
- agent_systems
- post_training_methods
- reinforcement_learning
- rl_for_llm_reasoning
- synthetic_data_generation
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 15
tags: []
---
# Simulating Environments with Reasoning Models for Agent Training

**Authors:** Yuetai Li, Huseyin A Inan, Xiang Yue, Wei-Ning Chen, Lukas Wutschitz, Janardhan Kulkarni, Radha Poovendran, Robert Sim, Saravan Rajmohan
**Published:** 2025-11-03 00:00:00
**Type:** paper

## Analysis

# Simulating Environments with Reasoning Models for Agent Training
2025-11-03 · paper · Yuetai Li, Huseyin A Inan, Xiang Yue, Wei-Ning Chen, Lukas Wutschitz et al. (9 total)
https://arxiv.org/pdf/2511.01824

---

### Motivation & Prior Limitations
LLM agents trained in "complex-task/simple-environment" settings (math olympiads, coding contests) fail to generalize to "simple-task/complex-environment" settings, where individual reasoning steps are easy but robustness across diverse tools, schemas, and edge cases is required.
- Building real agentic environments for training data generation is heavy, brittle, and environment-specific — each new domain demands custom API implementations, tool interface definitions, and execution infrastructure, which tightly couples trajectory generation to a specific environment and limits scalability.
  - Existing synthesis pipelines (e.g., ToolBench, AgentTuning, xLAM-2) all require real environment execution or explicit API implementations, making broad coverage across diverse agent scenarios impractical.
- For RL-based agent training, the same per-environment engineering burden is compounded: each scenario requires a separate setup with dedicated reward functions, tool interfaces, and environment state management, preventing unified agent RL across diverse tasks.

---

### Proposed Approach
The paper proposes that LLMs can act as environment simulators — using their world modeling capabilities to generate coherent state transitions, tool outputs, and error messages without access to real environments — and builds two training frameworks on top of this capability.

- **Simia-SFT** is an end-to-end agent trajectory synthesis pipeline that amplifies small seed sets into large, diverse SFT datasets in an environment-agnostic manner through four stages: (1) LLM-based pre-filtering of seeds across completeness, logic, and format dimensions; (2) prompt design that injects tool specifications, policy rules, output formats, and one reference trajectory as an exemplar; (3) LLM trajectory simulation at temperature 1.0 across multiple passes to promote diversity; and (4) rule-based post-processing to repair malformed JSON, validate tool call references, normalize tool-calling format (Hermes XML / JSON), and align system prompts to the target deployment environment.
  - This differs fundamentally from prior distillation approaches by expanding task distributions and enforcing structural fidelity absent from raw synthesizer outputs, while remaining environment-agnostic — no real environment is ever executed.
  - GPT-5 and o4-mini are used as synthesizers; from seed sets of ~5k trajectories the pipeline generates up to 90k training trajectories per domain.

- **Simia-RL** enables RL training by replacing real environments with an LLM simulator (o4-mini) that provides both environment feedback (simulated tool outputs, error messages) and reward signals (binary: 1 for success, 0 for failure), enabling GRPO-based policy optimization across multi-turn agentic interactions in a unified framework.
  - The simulator is given the full tool usage specification, expected feedback formats, interaction history, and one reference sample trajectory in its prompt — it must reason to construct plausible environment state and tool responses without real data access.
  - RL training runs for 64 GRPO steps using RAGEN on VeRL, applied after SFT initialization, making this an SFT-then-RL sequential pipeline.

---

### Results & Capabilities
Fine-tuning open models on Simia-generated trajectories yields substantial benchmark gains across three distinct agentic evaluation suites, with the 32B model surpassing GPT-4o and xLAM-2-70B on τ²-Bench despite training entirely on simulated data.

- On τ²-Bench (Airline, Retail), Simia-Tau (Qwen2.5-32B) achieves 58.9% average, surpassing GPT-4o (54.2%) and xLAM-2-70B (56.3%), and approaching o4-mini (63.2%); Simia-Tau (Qwen3-8B) achieves 49.3% average, outperforming the much larger Qwen2.5-32B-Instruct baseline (36.9%) and xLAM-2-8B (44.7%).
  - On the Passˆk robustness metric (requiring all k retries to succeed), Simia-Tau models maintain their advantage over xLAM-2 across k=1,2,3 on both Airline and Retail domains, indicating the gains are not due to lucky single-shot variance.

- On OfficeBench (2-app, 3-app cross-application workflows), Simia-OB (Qwen2.5-7B) achieves 42.6% average vs. 19.2% for the base Qwen2.5-7B-Instruct; Simia-OB-RL (Qwen2.5-7B) achieves 49.6%, demonstrating that RL on simulated environments yields additional gains over SFT alone.
  - Simia models trained on simulated office workflows generalize to the harder 3-app compositional setting despite seed data containing only 1-app tasks, showing that LLM-simulated training confers genuine compositional transfer.

- The combined Simia-Tau-RL (Qwen3-8B, SFT + RL) achieves 51.0% on τ²-Bench, modestly improving over SFT-only Simia-Tau at 49.3%, suggesting RL on simulated environments contributes consistent but incremental gains on top of a strong SFT foundation.

- Simia-SFT generalizes across model families (Qwen2.5/3, Llama 3.1/3.2) and scales across sizes from 1.5B to 32B, with all fine-tuned variants substantially outperforming their untuned base models.

---

### Implications
The central implication is that environment engineering — traditionally a bottleneck for scaling agent training — can be replaced by LLM-based simulation, reframing the problem as prompt-and-schema design rather than software infrastructure.

- For **synthetic data generation**, this demonstrates a viable path to generating hundreds of thousands of high-quality agentic trajectories from seed sets of only ~100–5000 examples, without any real execution, dramatically lowering the marginal cost of covering new agent domains.

- For **model-based RL and world models**, this work empirically validates that LLMs contain sufficient implicit world knowledge to serve as environment simulators for policy optimization —

## Key Claims

1. LLMs can simulate realistic environment feedback without access to actual testbed data or APIs, exploiting their world modeling abilities.
2. Building bespoke environments for agent training is heavy, brittle, and limits progress.
3. A 32B model fine-tuned on Simia-simulated trajectories (based on Qwen2.5-32B-Instruct) surpasses GPT-4o and xLAM-2-70B on τ²-Bench.
4. An 8B model fine-tuned on Simia-simulated trajectories (based on Qwen3-8B) outperforms Qwen2.5-32B-Instruct on τ²-Airline and Retail benchmarks.
5. Sequential SFT followed by RL on simulated environments yields slightly additional gains over SFT alone on both τ²-Bench and OfficeBench.
6. LLM trajectory simulation with temperature adjustment and multiple generation passes promotes diversity, enabling scalable training data creation without real environment execution.
7. Simia-SFT expands ~5k APIGen-MT seed trajectories into 90k synthetic training trajectories.
8. Simia-SFT expands 76 OfficeBench seed tasks with o4-mini trajectories into 30k synthetic samples targeting multi-app settings.
9. GPT-5 and o4-mini are used as trajectory synthesizers in Simia-SFT experiments at temperature 1.0.
10. o4-mini is used as the LLM environment simulator for Simia-RL experiments, computing rewards by assessing whether tasks are successfully completed based on the trajectory.

## Capabilities

- LLMs can simulate realistic environment feedback — including coherent state transitions, tool invocations, and simulated error messages — without access to actual testbed data or APIs, enabling environment-agnostic agent training data synthesis from small seed sets
- Small seed sets (76–5,000 trajectories) can be amplified 20–600× into diverse multi-turn agent training trajectories via LLM simulation, covering new task formulations, reasoning strategies, and action sequences without executing real environments
- RL agent training can be performed entirely within LLM-simulated environments — the simulator generates both environment feedback and reward signals — without deploying any real environment implementations or reset mechanisms
- Open-source 32B model fine-tuned entirely on simulated trajectories surpasses GPT-4o and a specialist 70B model (xLAM-2-70B) on realistic multi-turn tool-use benchmarks; an 8B model fine-tuned the same way outperforms the untuned 32B baseline

## Limitations

- LLM agents remain brittle in simple-task/complex-environment settings — tasks where individual reasoning steps are trivial but success requires robustness across diverse tools, schemas, and edge cases (vending machines, office workflows, household tasks)
- RL training on LLM-simulated environments yields only marginal gains over SFT alone — the additional policy optimization signal from simulated rewards provides 1–2 percentage point lift at best, suggesting the RL signal is weak relative to the supervised signal
- Simulated environment quality is hard-bounded by the semantic correctness of the synthesizer model — simulation fidelity cannot exceed the frontier model's domain world knowledge, propagating any model errors directly into training data
- Open models trained on simulated data exhibit a sharp performance cliff at compositional complexity: Qwen2.5-7B drops from 57.8% (2-app OfficeBench) to 27.3% (3-app), and Llama-3.1-8B drops from 64.9% to 12.7% — multi-application coordination reveals a hard capability boundary
- Scalable LLM environment simulation requires expensive frontier models (GPT-5, o4-mini) as synthesizers with 60,000-token context windows, making the approach costly and dependent on proprietary API access for the training data generation phase
- Traditional agent RL training requires per-environment engineering — custom tool interfaces, reward functions, and reset mechanisms — which scales poorly across diverse real-world domains and blocks coverage of the long tail of practical agent use cases
- A substantial performance gap persists between simulated-data-trained open models and frontier proprietary models: Simia-Tau 32B achieves 58.9 average on τ²-Bench vs GPT-5 at 67.6, and open models trail dramatically on Retail tasks (61.7 vs 77.2)
- The synthesis pipeline requires valid, curated seed trajectories and applies pre-filtering that discards incomplete or logically inconsistent seeds — the approach degrades silently when seed data is noisy, sparse, or domain-mismatched

## Bottlenecks

- Building bespoke training environments for agent RL is heavy, brittle, and environment-specific — each new domain requires dedicated tool interfaces, reward functions, and reset mechanisms, blocking scalable RL training across diverse real-world task domains

## Breakthroughs

- LLMs can replace hand-engineered environment implementations for both SFT data synthesis and RL training of agents — the Simia framework shows that a single frontier LLM simulator can generate coherent state transitions, tool feedback, and reward signals across arbitrary domains, reframing environme

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/synthetic_data_generation|synthetic_data_generation]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/grpo|GRPO]]
- [[entities/passk-metric|pass^k metric]]
- [[entities/verl|veRL]]
