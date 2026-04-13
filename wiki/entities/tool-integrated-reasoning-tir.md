---
type: entity
title: Tool-Integrated Reasoning (TIR)
entity_type: method
theme_ids:
- agent_systems
- chain_of_thought
- finetuning_and_distillation
- mathematical_and_formal_reasoning
- multi_agent_coordination
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- tool_use_and_agent_protocols
created: '2026-04-09'
updated: '2026-04-09'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 2.901227321117759e-05
staleness: 0.0
status: active
tags: []
---
# Tool-Integrated Reasoning (TIR)

Tool-Integrated Reasoning (TIR) is a reasoning paradigm that augments large language models with the ability to write, execute, and iterate on code during inference, enabling them to offload computation to external interpreters rather than relying solely on internal next-token prediction. Formalized as a trajectory of (reasoning, code, output) triples, TIR has emerged as one of the most productive directions in post-training methodology for mathematical and scientific reasoning, with recent RL-based approaches demonstrating that models can autonomously discover when and how to use tools without being explicitly taught to do so.

**Type:** method
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/chain_of_thought|Chain of Thought]], [[themes/finetuning_and_distillation|Finetuning and Distillation]], [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/multi_agent_coordination|Multi-Agent Coordination]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]

---

## Overview

The core insight behind TIR is that LLMs face a fundamental ceiling on symbolic and numerical manipulation — tasks where iterative, verifiable computation is necessary — when constrained to pure language generation. By interleaving natural language reasoning with executable code and feeding interpreter outputs back into the reasoning chain, TIR models can perform multi-step mathematical derivations, run experiments, and self-correct based on concrete execution feedback rather than hallucinated results.

The paradigm has been operationalized through two distinct training strategies: supervised fine-tuning on curated (reasoning, code, output) trajectories, and reinforcement learning directly from scalar rewards on final answer correctness. The RL-from-scratch approach is particularly notable because it allows models to develop tool-use behaviors emergently rather than imitating predetermined patterns — a qualitatively different regime that appears to yield stronger generalization.

---

## Key Findings

### Emergent Tool Adoption Under RL

ToRL: Scaling Tool-Integrated RL provides the clearest evidence that TIR behaviors can be induced without supervised imitation. Training with the GRPO algorithm (rollout batch size 128, 16 samples per problem, no KL loss, temperature 1.0) on a curated dataset of 28,740 Olympic-level mathematical problems, TORL models learn to incorporate code into their reasoning with striking speed: within the first 100 training steps, the proportion of responses containing code rose from 40% to 80%. The reward function is deliberately sparse — correct answers receive +1, incorrect answers −1, with an additional −0.5 penalty for non-executable code — yet this minimal signal is sufficient to drive rapid behavioral reorganization. The implication is that the capacity for tool use is latent in pre-trained models; RL serves as the mechanism that makes it habitual.

The performance results are striking in absolute terms. TORL-7B achieves 43.3% on AIME24, surpassing RL-without-tools baselines by 14 percentage points and the best prior TIR model by 17 points. TORL-1.5B reaches 48.5% average accuracy across mathematical benchmarks, outperforming both the instruction-tuned and TIR-tuned variants of the same base model (Qwen2.5-Math-1.5B-Instruct at 35.9% and Qwen2.5-Math-1.5B-Instruct-TIR at 41.3%). At the 7B scale, average benchmark accuracy reaches 62.1%, a 14.7% absolute gain over other open-source models on the same base.

### Scaling Through Self-Teaching

START: Self-taught Reasoner with Tools demonstrates a complementary approach: bootstrapping TIR capability through self-generated training data, allowing capability to scale without human-labeled trajectories. The gains over QwQ-32B-Preview are large and consistent across difficulty levels — +5.5% on GPQA (PhD-level science QA, reaching 63.6%), +3.8% on a further benchmark, +15.0% on AMC23 (reaching 95.0%), and +16.7% on AIME24 (reaching 66.7%). The breadth of improvement across both competition mathematics and graduate-level science suggests that the TIR paradigm generalizes across reasoning domains, not merely symbolic manipulation tasks where code execution provides the most obvious advantage.

### TIR in Agentic Multi-Step Settings

Chain-of-Agents: End-to-End Agent Foundation Models via Multi-Agent Distillation and Agentic RL extends TIR beyond closed mathematical domains into open-ended web agent benchmarks, situating it within a multi-agent distillation framework. The resulting Agent Foundation Model (AFM) at 32B parameters achieves 55.3% on GAIA (text-only), 11.1% on BrowseComp, and 18.0% on HLE — and notably reaches 59.8% on AIME2025, an absolute improvement of over 10.5% compared to previous best-performing TIR methods. This positions TIR not merely as a mathematical reasoning technique but as a component of a broader agentic architecture where tool use, long-horizon planning, and multi-agent coordination interact.

---

## Relationships and Connections

TIR sits at the intersection of several active research threads. Its connection to [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] is direct: the most performant TIR systems are now trained via process-level or outcome-level RL rather than behavioral cloning, and the TORL results suggest that RL-from-scratch may be more effective than building on SFT checkpoints. The relationship to [[themes/chain_of_thought|Chain of Thought]] is architectural — TIR can be understood as CoT augmented with executable verification steps, replacing the model's internal "scratchpad" with an external interpreter for computationally demanding substeps.

The extension into [[themes/agent_systems|Agent Systems]] (as seen in AFM) raises the question of whether TIR's benefits in closed mathematical settings transfer cleanly to open-ended, partially observable environments where execution feedback is noisier and task decomposition is itself part of the problem. The gains on GAIA and BrowseComp are promising but the absolute numbers remain low, suggesting the paradigm is not yet fully solved in agentic contexts.

The [[themes/finetuning_and_distillation|Finetuning and Distillation]] angle is also significant: START's self-teaching approach and AFM's multi-agent distillation both suggest that TIR capability can be propagated to smaller models without requiring human-annotated execution traces at scale, though the quality ceiling of self-generated data remains an open constraint.

---

## Limitations and Open Questions

Several tensions are underexplored in the current literature. The TORL results show rapid behavioral adaptation toward code use, but it is unclear how robustly the model distinguishes tasks where code execution genuinely helps from tasks where it is unnecessary overhead — over-reliance on external tools could increase latency without improving accuracy. The penalty for non-executable code (−0.5 in TORL's reward scheme) addresses syntactic failures but not semantic ones, where code runs successfully but computes the wrong thing.

The training data curation choices in TORL — filtering to 28,740 problems from an initial pool of 75,149, excluding proof-based and ambiguously verifiable problems — reveal a significant constraint: TIR as currently formalized requires problems with clear, checkable answers. This excludes large classes of scientific and engineering reasoning where correctness is not binary. How TIR should be extended to open-ended or multi-criteria tasks remains an open architectural question.

Finally, the AFM results on BrowseComp (11.1%) and HLE (18.0%) are substantially lower than the mathematical benchmarks, suggesting a capability gap when tool use must be integrated with web navigation, retrieval, and multi-turn coordination. Whether this gap reflects a fundamental limitation of the TIR trajectory formalism in non-mathematical settings, or simply a data and training scale issue, is not yet clear.

## Sources
