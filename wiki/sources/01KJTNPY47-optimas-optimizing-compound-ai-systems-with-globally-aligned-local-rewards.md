---
type: source
title: 'Optimas: Optimizing Compound AI Systems with Globally Aligned Local Rewards'
source_id: 01KJTNPY47KBG455VZ4FCZC9FR
source_type: paper
authors:
- Shirley Wu
- Parth Sarthi
- Shiyu Zhao
- Aaron Lee
- Herumb Shandilya
- Adrian Mladenic Grobelnik
- Nurendra Choudhary
- Eddie Huang
- Karthik Subbian
- Linjun Zhang
- Diyi Yang
- James Zou
- Jure Leskovec
published_at: '2025-07-03 00:00:00'
theme_ids:
- agent_systems
- multi_agent_coordination
- policy_optimization
- reinforcement_learning
- reward_modeling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Optimas: Optimizing Compound AI Systems with Globally Aligned Local Rewards

**Authors:** Shirley Wu, Parth Sarthi, Shiyu Zhao, Aaron Lee, Herumb Shandilya, Adrian Mladenic Grobelnik, Nurendra Choudhary, Eddie Huang, Karthik Subbian, Linjun Zhang, Diyi Yang, James Zou, Jure Leskovec
**Published:** 2025-07-03 00:00:00
**Type:** paper

## Analysis

# Optimas: Optimizing Compound AI Systems with Globally Aligned Local Rewards
2025-07-03 00:00:00 · paper · Shirley Wu, Parth Sarthi, Shiyu Zhao, Aaron Lee, Herumb Shandilya et al. (13 total)
https://arxiv.org/pdf/2507.03041

---

### Motivation & Prior Limitations
- Compound AI systems — integrating LLMs, tools, retrievers, and ML models as directed acyclic graphs — are increasingly deployed for complex tasks, but end-to-end optimization is fundamentally blocked by their non-differentiable structure and the heterogeneity of configuration types (prompts, hyperparameters, model weights, model selection).
  - Gradient-based optimization cannot be applied across the pipeline because the components are non-differentiable.
  - Prior methods (DSPy, TextGrad, OPRO) optimize only a single configuration type in isolation, missing cross-component bottlenecks — a perfectly tuned prompt cannot compensate for a poorly chosen model, and upstream components lack visibility into what inputs are effective for downstream ones.
  - Achieving a global reward signal requires running the entire compound system for every candidate configuration, making joint search extremely data-inefficient.
- Cascading failures are a structural risk: a single upstream misinterpretation (e.g., LLM misreading a query) propagates corrupted inputs through all downstream components, degrading final outputs in ways that per-component optimization cannot detect or correct.

---

### Proposed Approach
- OPTIMAS introduces one Local Reward Function (LRF) per component, each satisfying a local–global alignment property: a component's local reward must correlate with the expected global system reward, so independently maximizing local rewards reliably improves global performance.
  - LRFs are implemented as a shared LLM backbone with separate linear projection heads per component, encoding concatenated component input/output pairs into scalar reward values — a multitask neural network design that keeps memory costs manageable across many components.
  - Alignment is defined formally: if the LRF ranks output y⁺ above y⁻ for component Cₖ, then the expected global reward (estimated via Monte Carlo sampling over downstream stochasticity) must also be higher for y⁺. LRFs are trained with a pairwise log-sigmoid ranking loss over preference datasets constructed by sampling two candidate outputs per component and running the downstream system to label the winner.
  - Because system configurations change during optimization, LRFs can drift out of alignment. OPTIMAS uses a two-stage adaptation: offline initial training on the starting configuration, then lightweight online adaptation via mini-batches of fresh preference data and a replay buffer, avoiding full retraining after each update.
- Local optimization is decoupled by configuration type: OPRO-style metric-guided search for prompts, PPO (with the LRF as the critic) for trainable model parameters, and probability-weighted sampling for discrete/continuous hyperparameters and model selection. A new configuration is only accepted if it improves global reward on a small validation set, preventing cascading errors from bad local updates.

---

### Results & Capabilities
- OPTIMAS outperforms all baselines across five real-world compound systems with an average relative improvement of 11.92%, and is the only method that improves performance on all five tasks.
  - Baselines include DSPy, TextGrad, OPRO, and LLMSelector; DSPy improves on multi-hop QA (HotpotQA) but degrades performance on product recommendation, illustrating the instability of single-type optimization methods.
  - The five evaluated systems span: behavior-driven product recommendation (Amazon), medical analysis (PubMed), semi-structured knowledge base retrieval (STaRK), general multi-hop RAG (HotpotQA), and self-verified code generation (BigCodeBench) — covering heterogeneous configuration types including prompts, model parameters, model selection, hyperparameters, and probability vectors.
- OPTIMAS achieves higher data efficiency than baselines by performing local optimization with LRFs rather than running the full compound system for every candidate configuration, reducing the number of required end-to-end system executions.
- The framework provides formal convergence guarantees under mild conditions, distinguishing it from all prior baselines (DSPy, TextGrad, OPRO, LLMSelector) which offer no such guarantee.

---

### Implications
- The local-global alignment principle offers a general credit assignment mechanism for non-differentiable compound systems, analogous in spirit to process reward models in chain-of-thought reasoning — but applicable across heterogeneous, modular pipelines rather than sequential token generation.
- By enabling PPO training of individual LLM components using LRFs as critics, OPTIMAS opens a path to RLHF-style fine-tuning within multi-component systems where the reward signal originates from downstream global task performance rather than human annotation, which is directly relevant to alignment of agents embedded in larger pipelines.
- The DAG-based formalism and adaptive LRF mechanism could generalize to agentic systems where components are tools or sub-agents, potentially providing a framework for reward shaping and credit assignment in multi-agent and autonomous agent pipelines.
- The preference-data-driven alignment mechanism — labeling component outputs by running downstream Monte Carlo rollouts — is structurally similar to MCTS-based process reward modeling, suggesting cross-fertilization potential between compound system optimization and tree-search-based reasoning reward research.

---

### Remaining Limitations & Next Steps
- The paper evaluates five systems, but all are relatively structured pipelines with fixed or semi-fixed DAG topologies; it is unclear how OPTIMAS performs in highly dynamic agentic settings where the graph structure changes substantially at inference time.
  - Dynamic planni

## Key Claims

1. OPTIMAS outperforms strong baselines by an average relative improvement of 11.92% across five real-world compound AI systems.
2. OPTIMAS is the only evaluated method that improves performance across all five compound AI tasks, while methods like DSPy improve some tasks but degrade others.
3. Compound AI systems are highly sensitive to individual component failures, which cause cascading failures in final results.
4. Previous compound AI optimization methods fail to capture critical bottlenecks because they optimize specific configurations (prompts, model selection) in isolation rather than jointly.
5. Individually well-optimized components in a compound system may still collaborate suboptimally because upstream components lack visibility into what inputs are effective for downstream components.
6. The non-differentiable nature of compound AI system configurations prevents the use of gradient-based end-to-end optimization.
7. OPTIMAS maintains one Local Reward Function (LRF) per component, where each LRF satisfies a local-global alignment property such that maximizing the local reward correlates with improving global syste
8. OPTIMAS implements all LRFs using a shared LLM backbone with separate linear projection heads per component, concatenating component input and output as the encoding input.
9. OPTIMAS trains LRFs using a pairwise log-sigmoid ranking loss over preference data, where candidate outputs are labeled by their relative expected global reward.
10. Preference data for LRF training is constructed by sampling two candidate outputs for a component (e.g., via higher-temperature decoding) and estimating their expected global reward via Monte Carlo sa

## Capabilities

- Compound AI systems with heterogeneous configuration types (prompts, hyperparameters, model weights, model selection) can be jointly optimized end-to-end using locally-aligned reward functions, achieving average 11.92% relative improvement over strong baselines across 5 real-world systems
- A single shared LLM backbone with separate linear projection heads can serve as a scalable multi-task reward model for all components of a compound AI system simultaneously, enabling data-efficient per-component reward estimation without separate model instantiation
- Local reward functions for compound system components can be adapted incrementally using mini-batch preference data as configurations evolve, avoiding full retraining while maintaining local-global reward alignment

## Limitations

- Compound AI systems are fundamentally non-differentiable, preventing gradient-based end-to-end optimization across configurations that span heterogeneous types (discrete prompts, categorical model selection, continuous weights, numerical hyperparameters)
- Individual component optimization in compound AI systems fails to account for inter-component dependencies: even a perfectly optimized upstream component may generate outputs poorly suited to downstream components, producing globally suboptimal performance despite locally good metrics
- Single-component errors in compound AI pipelines cascade multiplicatively: an LLM misinterpreting a query at step 1 corrupts all subsequent tool calls and retrieval steps, producing unreliable outputs regardless of individual downstream component quality
- Running the full compound AI system during configuration optimization is cost-prohibitive, making naive search over compound configurations impractical — especially for systems with many components and large configuration spaces
- Existing compound system optimization methods (DSPy, TextGrad, OPRO, LLMSelector) can actively degrade performance on some task types while improving others — no prior method consistently improves across diverse compound system architectures
- Local reward functions trained under one system configuration become distributionally misaligned as configurations evolve during optimization — both upstream and downstream component updates corrupt previously valid LRF predictions
- OPTIMAS and the compound system optimization paradigm require a user-defined, quantitative global reward function — silently excluding open-ended, creative, or subjective compound AI tasks where no ground truth metric exists
- OPTIMAS requires constructing an offline preference dataset per component before optimization begins — for novel compound systems this initial data collection involves full system runs, adding a significant deployment barrier before any optimization benefit is realized
- Compound AI systems with dynamic planning (adaptive edge connections per input instance) add distribution shift complexity that LRFs must handle — the theoretical convergence guarantees assume mild conditions that may not hold for highly dynamic routing graphs

## Bottlenecks

- No principled, unified method exists for jointly optimizing heterogeneous configuration types (discrete prompts, categorical model selection, continuous hyperparameters, model weights) across components of compound AI systems — each type requires a separate optimization strategy with no cross-compon
- Credit assignment across compound AI pipeline components — determining which component's configuration contributed to a global reward change — is intractable without intermediate proxy reward models, forcing costly full-system evaluation per configuration candidate
- Cascading failure propagation in compound AI pipelines — where upstream component errors systematically corrupt all downstream processing — blocks reliable production deployment of complex multi-component systems without joint optimization of inter-component error handling

## Breakthroughs

- OPTIMAS demonstrates that compound AI systems with heterogeneous configurations can be jointly and data-efficiently optimized using locally-aligned reward functions with provable convergence — the first method achieving consistent improvement across all compound system types tested

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]

## Key Concepts

- [[entities/bigcodebench|BigCodeBench]]
- [[entities/dspy|DSPy]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
- [[entities/textgrad|TextGrad]]
